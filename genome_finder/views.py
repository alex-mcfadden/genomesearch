from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
import json

from genomesearch.tasks.fetch_jobs import get_jobs, get_job_status 
from genomesearch.tasks.align import align_to_all

task_ids = []

@api_view(['POST'])
def align_view(request: Request):
    """
    Endpoint to align a sequence against all genomes in the database, 
    returning information on the first close match. Validates data for DNA
    characters, and returns a task ID for the celery job. Returns a 400 error
    if no sequence is provided, or if the sequence contains invalid characters.
    
    Args:
        request: Request object with JSON body containing a "sequence" key.
    
    Returns:
        Response object with a JSON body containing the task ID, status,
        result, and date_done of the celery job.
    """
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
def get_jobs_view(request: Request):
    """
    Endpoint to get all celery jobs. See the celery_get_jobs 
    docstring for more detail.

    Args:
        request: Request object with no body. The request is not used.
    Returns:   
        Response object with a JSON body containing the task IDs, statuses,
        results, and date_dones of the celery jobs.

    """
    tasks = get_jobs()
    return Response(tasks)

@api_view(['GET'])
def get_job_status_view(request: Request):
    """
    Endpoint to get the status of a celery job. Validates the job_id
    and returns a 400 error if no job_id is provided, or if the job_id
    does not correspond to a celery job.

    Args:
        request: Request object with a query parameter "job_id".
    Returns:
        Response object with a JSON body containing the status of the job.
    
    """
    job_id = request.query_params.get("job_id")
    if not job_id:
        return Response({"error": "No job_id provided"}, status=400)
    from django_celery_results.models import TaskResult
    return Response(get_job_status(job_id))