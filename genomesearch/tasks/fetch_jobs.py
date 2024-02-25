from django_celery_results.models import TaskResult


def get_jobs():
    """
    Get all celery align_to_all jobs from the database, and return a list of dictionaries with
    relevant data for each job. This shows the overall status of the parent task, without 
    returning each subtask status.
    """
    tasks = TaskResult.objects.filter(task_name="genomesearch.tasks.align.align_to_all")
    decoded_tasks = []
    for task in tasks:
        decoded_tasks.append({
            "id": task.id,
            "status": task.status,
            "result": task.result,
            "date_done": task.date_done
        })
    return decoded_tasks

def get_job_status(job_id: str):
    """
    Get the status of a celery job from the database by job UUID, 
    and return the status. Useful for checking if a job is finished or not.
    """
    task = TaskResult.objects.get(task_id=job_id)
    return task.status
