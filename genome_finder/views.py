from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response
import json

from genomesearch.celery import align_to_all, get_jobs as celery_get_jobs
task_ids = []

@api_view(['POST'])
def align(request):
    data = json.loads(request.body)
    sequence = data.get("sequence")
    task = align_to_all.delay(sequence.upper())
    return Response({"task_id": task.id,
                     "status": task.status,
                     "result": task.result,
                     "date_done": task.date_done})

@api_view(['GET'])
def get_jobs(request):
    tasks = celery_get_jobs()
    return Response(tasks)