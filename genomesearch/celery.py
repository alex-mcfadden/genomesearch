"""
https://docs.celeryq.dev/en/stable/django/first-steps-with-django.html
"""
import os

from celery import Celery
from django.conf import settings

from celery.result import allow_join_result
from genome_finder.constants import GENOMES
from celery import group

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


@app.task
def align(sequence: str, genome_name: str):
    return sequence, genome_name

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