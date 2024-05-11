from django.urls import path
from .views import *

urlpatterns = [
    path("reports/", AccidentListView.as_view(), name="showlist"),
    path("reports/paged/<int:page>/", AccidentListView.as_view(), name="showlistpage"),
    path("report/<int:id>/", SingleRecordView.as_view(), name="singlerecord"),
    path("analyze/", AnalyzeView.as_view(), name="analyze"),
    path("video/<str:video_type>", StreamVideoView.as_view(), name="video")
]