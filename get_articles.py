# Demonstrates article maintenance using APScheduler rather than Celery and RabbitMQ

from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
from news.tasks import article_maintenance
import os

scheduler = BlockingScheduler()
scheduler.add_job(article_maintenance, 'interval', seconds=20*60)
scheduler.start()
