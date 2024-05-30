from django.urls import path, include
from rest_framework import routers

from ticker.views import TickerView

router = routers.DefaultRouter()


urlpatterns = [
    path('ticker/', TickerView.as_view()),
]
