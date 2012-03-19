from celery.task import task
from celery.registry import TaskRegistry

from routine import fetch_albums

@task(name='picasa.async.async_fetch_albums')
def async_fetch_albums():
    fetch_albums()
