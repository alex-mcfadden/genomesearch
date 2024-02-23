"""
https://docs.celeryq.dev/en/stable/django/first-steps-with-django.html
"""
import os

from celery import Celery
from django.conf import settings
from time import sleep
from celery.result import allow_join_result
from genome_finder.constants import GENOMES
from celery import group

from Bio import SeqIO
from Bio.Seq import Seq
from Bio.Align import PairwiseAligner

# this code copied from manage.py
# set the default Django settings module for the 'celery' app.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'genomesearch.settings')

# you can change the name here
app = Celery("genome_finder")

# read config from Django settings, the CELERY namespace would make celery
# config keys has `CELERY` prefix
app.config_from_object('django.conf:settings', namespace='CELERY')

# discover and load tasks.py from from all registered Django apps
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

@app.task
def align_to_all(sequence: str):
    subtasks = [align.s(sequence, genome_name).set(queue='subtask_queue') for genome_name in GENOMES]
    group_results = group(subtasks).apply_async()
    with allow_join_result():
        for i, result in enumerate(group_results.join()):
            if result:
                for result in group_results: # don't search anywhere else after alignment is found
                    app.control.revoke(result.task_id, terminate=True)
                return group_results[i].result
    return {"sequence": sequence, "error": "No alignment found"}


@app.task
def align(sequence: str, genome_name: str):
    nucleotide_sequence = Seq(sequence)
    genome = SeqIO.read(os.path.join(os.getcwd(), f"genome_finder/genomes/{genome_name}.gb"), "genbank")
    aligner = PairwiseAligner()
    aligner.mode = 'local'
    aligner.open_gap_score = -30 
    aligner.extend_gap_score = -10
    aligner.mismatch_score = -1
    aligner.match_score = 1

    for feature in genome.features:
        if feature.type == "CDS":
            gene_name = feature.qualifiers.get("gene", [""])[0]
            gene_sequence = feature.extract(genome.seq)
            alignments = aligner.align(nucleotide_sequence, gene_sequence)
            if alignments: # return only top found alignment
                score = alignments[0].score
                if score > len(nucleotide_sequence) * 0.95:
                    indices = alignments[0].indices
                    return {
                        "input_sequence": sequence,
                        "genome": genome_name,
                        "gene_name": gene_name,
                        "startbp_sample": int(indices[0][0]) + 1,
                        "endbp_sample": int(indices[0][-1]) + 1,
                        "startbp_genome": int(indices[1][0]) + feature.location.start + 1,
                        "endbp_genome": int(indices[1][-1]) + feature.location.start + 1,
                        "score": float(alignments[0].score)
                    }


def get_jobs():
    from django_celery_results.models import TaskResult
    tasks = TaskResult.objects.filter(task_name="genomesearch.celery.align_to_all")
    decoded_tasks = []
    for task in tasks:
        decoded_tasks.append({
            "id": task.id,
            "status": task.status,
            "result": task.result,
            "date_done": task.date_done
        })

    return decoded_tasks

def get_job_status(job_id):
    from django_celery_results.models import TaskResult
    task = TaskResult.objects.get(id=job_id)
    return task.status