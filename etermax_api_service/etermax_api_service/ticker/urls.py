"""
URL configuration for the ticker app.

This module sets up the URL routes for the ticker-related views.
"""

from django.urls import path

from ticker.views import (
    TickerAveragePriceView,
    TickerListView,
    TickerPriceView
)

# Define URL patterns for the ticker app
urlpatterns = [
    path('ticker-average-price/', TickerAveragePriceView.as_view(), name="average-price"),
    path('ticker-list/', TickerListView.as_view(), name='ticker-list'),
    path('ticker-price/', TickerPriceView.as_view(), name='ticker-price')
]
