from celery import shared_task

from ticker.ticker import BuenbitTicker


@shared_task
def fetch_and_set_buenbit_data():
    """
    Celery task to fetch ticker data from Buenbit API and store it in the cache.

    This task uses the BuenbitTicker class to fetch the latest ticker data
    and store it in the Redis cache.
    """
    BuenbitTicker().set_ticker()
