import shlex
import subprocess
import sys

from django.core.management.base import BaseCommand
from django.utils import autoreload


def restart_celery():
    celery_worker_cmd = "celery -A genomesearch worker"
    cmd = f'pkill -f "{celery_worker_cmd}"'
    if sys.platform == "win32":
        cmd = "taskkill /f /t /im celery.exe"

    subprocess.call(shlex.split(cmd))
    subprocess.Popen(shlex.split(f"{celery_worker_cmd} -n worker1@%h --loglevel=info -Q celery"))
    subprocess.Popen(shlex.split(f"{celery_worker_cmd} -n worker2@%h --loglevel=info -Q subtask_queue"))


class Command(BaseCommand):
    def handle(self, *args, **options):
        print("Starting celery worker with autoreload...")
        autoreload.run_with_reloader(restart_celery)