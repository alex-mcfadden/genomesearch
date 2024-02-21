from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from genome_finder.constants import GENOMES
import json

from genomesearch.celery import align as celery_align, get_job as celery_get_job

task_ids = []

@api_view(['POST'])
def align(request):
    data = json.loads(request.body)
    sequence = data.get("sequence")
    for genome_name in GENOMES:
        task = celery_align.delay(sequence, genome_name)
    task_ids.append(task.id)
    return Response({'jobId': task.id,
                     'status': task.status})

@api_view(['GET'])
def get_jobs(request):
    task_detail = [celery_get_job(task_id) for task_id in task_ids]
    return Response(task_detail)