from django.urls import path
from .views import AccidentListView, SingleRecordView

urlpatterns = [
    path("records/", AccidentListView.as_view(), name="showlist"),
    path("record/<int:id>/", SingleRecordView.as_view(), name="singlerecord"),
]
