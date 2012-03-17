from celery.task import task

from routine import fetch_albums

@task
def async_fetch_albums():
    fetch_albums()