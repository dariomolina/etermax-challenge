from django.urls import path, include
from rest_framework import routers

from ticker.views import AveragePriceView, TickerListView

router = routers.DefaultRouter()


urlpatterns = [
    path('average-price/', AveragePriceView.as_view()),
    path('ticker-list/', TickerListView.as_view())
]
