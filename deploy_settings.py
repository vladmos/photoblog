"""
Deployment dependent settings
"""

# Celery

BROKER_HOST = '127.0.0.1'
BROKER_BACKEND = 'redis'
REDIS_PORT = 6379
REDIS_HOST = '127.0.0.1'
BROKER_USER = ''
BROKER_PASSWORD = ''
BROKER_VHOST = '0'
REDIS_DB = 0
REDIS_CONNECT_RETRY = True
CELERY_SEND_EVENTS = True
CELERY_RESULT_BACKEND = 'redis'
CELERY_TASK_RESULT_EXPIRES =  10
CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'

# Google oAuth

OAUTH_CONSUMER_KEY = 'photoblog.fulc.ru'
