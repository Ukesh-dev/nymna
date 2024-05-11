from django.urls import path
from .views import *

urlpatterns = [
    path("detect/", DetectAnamolyView.as_view(), name="showlist"),
    path("player/<folder>", PlayerView.as_view(), name="player")
]