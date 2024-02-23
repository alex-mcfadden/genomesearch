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
    if not sequence:
        return Response({"error": "No sequence provided"}, status=400)
    if not all([base in "ACGTatcg" for base in sequence]):
        return Response({"error": "Invalid sequence"}, status=400)
    task = align_to_all.delay(sequence.upper())
    return Response({"task_id": task.id,
                     "status": task.status,
                     "result": task.result,
                     "date_done": task.date_done})

@api_view(['GET'])
def get_jobs(request):
    tasks = celery_get_jobs()
    return Response(tasks)

@api_view(['GET'])
def get_job_status(request):
    job_id = request.query_params.get("job_id")
    if not job_id:
        return Response({"error": "No job_id provided"}, status=400)
    from django_celery_results.models import TaskResult
    task = TaskResult.objects.get(id=job_id)
    if not task:
        return Response({"error": f"No job with ID {job_id}"}, status=400)
    return Response({"status": task.status})