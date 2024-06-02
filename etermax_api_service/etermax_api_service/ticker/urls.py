"""
URL configuration for the ticker app.

This module sets up the URL routes for the ticker-related views.
"""

from django.urls import path

from ticker.views import AveragePriceView, TickerListView

# Define URL patterns for the ticker app
urlpatterns = [
    path('average-price/', AveragePriceView.as_view(), name="average-price"),
    path('ticker-list/', TickerListView.as_view(), name='ticker-list')
]
