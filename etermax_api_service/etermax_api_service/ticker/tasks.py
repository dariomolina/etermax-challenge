from celery import shared_task
from .ticker import RecurrentTicker


@shared_task
def fetch_and_set_buenbit_data():
    RecurrentTicker().set_ticker()
