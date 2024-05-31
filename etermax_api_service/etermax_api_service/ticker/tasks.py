from celery import shared_task

from ticker.ticker import BuenbitTicker


@shared_task
def fetch_and_set_buenbit_data():
    BuenbitTicker().set_ticker()
