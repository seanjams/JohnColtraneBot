from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.background import BackgroundScheduler
from flask_apscheduler import APScheduler
from pytz import utc

from config import DATABASE_URL

# initialize scheduler
scheduler_config = {
    "jobstores":{
        'default': SQLAlchemyJobStore(url=DATABASE_URL)
    },
    "executors":{
        'default': ThreadPoolExecutor(20),
        'processpool': ProcessPoolExecutor(5)
    },
    "job_defaults":{
        'coalesce': False,
        'max_instances': 3
    },
    "timezone": utc,
}
scheduler = APScheduler(
    scheduler=BackgroundScheduler(**scheduler_config)
)

# Common args for scheduler.add_job
every_five_minutes = {
    "trigger": "interval",
    "minutes": 5,
    "misfire_grace_time": 900,
}

# example:
#   scheduler.add_job(
#     id="print_hello",
#     func=print_hello,
#     **every_five_minutes
#   )
