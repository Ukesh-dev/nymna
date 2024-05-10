from django.urls import path
from core.views import AccidentListView

urlpatterns = [
    path("records/", AccidentListView.as_view(), name="showlist")
]