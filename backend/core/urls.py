from django.urls import path
from core.views import AccidentListView

urlpatterns = [
    path("show/list/", AccidentListView.as_view(), name="showlist")
]