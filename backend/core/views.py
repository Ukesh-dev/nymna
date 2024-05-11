import os.path

from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from core.models import Report
from backend.settings import BASE_DIR

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.core.paginator import Paginator, EmptyPage
from django.forms.models import model_to_dict
from .onesignal import OneSignalNotification

import cv2
import asyncio
import time
from django.http import StreamingHttpResponse, HttpResponse, HttpResponseNotFound
from django.views.decorators import gzip


@method_decorator(csrf_exempt, name="dispatch")
class SingleRecordView(View):
    def get(self, request, *args, **kwargs):
        """
        Retrieves a single report by its id.

        Args:
        request: The HTTP request object.
        *args: Additional positional arguments.
        **kwargs: Additional keyword arguments.

        Returns:
        A JSON response containing the requested report data if successful,
        or an error message and HTTP status code 500 if the id is invalid or the record doesn't exist.

        Raises:
        ValueError: If the id is not provided in the URL.

        Example:
        GET /api/reports/1/
        """

        id = kwargs.pop('id', None)
        if not id:
            return JsonResponse({
                "success": False,
                "message": "Invalid Params"
            }, status=500)

        report = Report.objects.filter(id=id).first()
        if not report:
            return JsonResponse({
                "success": False,
                "message": "Record doesn't exists"
            }, status=500)

        report_data = model_to_dict(report)
        if report.video:
            report_data["video"] = f"http://127.0.0.1:8000/static/{report.video}"

        return JsonResponse({
            "success": True,
            "data": report_data
        })


# Create your views here.
@method_decorator(csrf_exempt, name="dispatch")
class AccidentListView(View):

    def get(self, request, *args, **kwargs):
        """
        Retrieves a list of reports with pagination.

        Args:
        request: The HTTP request object.
        *args: Additional positional arguments.
        **kwargs: Additional keyword arguments.

        Returns:
        A JSON response containing a list of reports with pagination information.

        Example:
        GET /api/reports/paged/1
        """

        current_page = kwargs.pop('page', 1)

        total_pages = 1
        output = []
        all_reports = Report.objects.all()
        total_count = all_reports.count()
        if total_count > 0:
            try:
                paginator = Paginator(all_reports, 10)
                total_pages = paginator.num_pages
                reports = paginator.page(current_page)

                for report in reports:
                    report_data = model_to_dict(report)
                    if report.video:
                        report_data["video"] = f"http://127.0.0.1:8000/static/{report.video}"

                    output.append(
                        report_data
                    )
            except EmptyPage:
                pass

        return JsonResponse({
            "success": True,
            "data": output,
            "current": current_page,
            "total": total_pages,
            "counts": total_count
        })

    def post(self, request, *args, **kwargs):
        """
        Saves a new report to the database and sends a notification.

        Args:
        request: The HTTP request object.
        *args: Additional positional arguments.
        **kwargs: Additional keyword arguments.

        Returns:
        A JSON response containing a success message if the record is saved successfully,
        or an error message and HTTP status code 500 if an exception occurs.

        Example:
        POST /api/reports/
        """
        try:
            source = request.POST.get("source", None)
            confidence = request.POST.get("confidence", 0)
            status = request.POST.get("status", "minor")
            timestamp_end = request.POST.get("timestamp_end", 0)
            timestamp_start = request.POST.get("timestamp_start", 0)
            video = request.POST.get("video", None)

            if not source:
                raise Exception("Source not found")

            if not confidence:
                raise Exception("Confidence not found")

            if not status:
                raise Exception("Status not found")

            if not timestamp_end or not timestamp_start:
                raise Exception("Timestamp not found")

            report = Report(
                source=source,
                confidence=confidence,
                status=status,
                timestamp_start=timestamp_start,
                timestamp_end=timestamp_end,
                video=video
            )
            report.clean_fields()
            report.save()

            channel_layer = get_channel_layer()
            report_data = model_to_dict(report)
            if report.video:
                report_data["video"] = f"http://127.0.0.1:8000/static/{report.video}"

            OneSignalNotification.send({
                "title": "Incident Alert!!!",
                "message": "There has been an incident",
                "data": report_data
            })

            async_to_sync(channel_layer.group_send)(
                "notification",
                {
                    'type': 'send_notification',
                    'notification': {
                        "type": "new_alert",
                        "data": [
                            report_data
                        ]
                    }
                }
            )

            return JsonResponse({
                "success": True,
                "message": "Record saved successfully"
            })
        except Exception as e:
            return JsonResponse({
                "success": False,
                "error": str(e)
            }, status=500)


class AnalyzeView(View):
    def post(self, request, *args, **kwargs):
        try:
            video_link = kwargs.get('video_link', None)
            if not video_link:
                raise Exception("Please provide video link")

            return JsonResponse({
                "success": True,
                "message": "Analyzed successfully"
            })
        except Exception as e:
            return JsonResponse({
                "success": True,
                "message": str(e)
            }, status=500)


# @gzip.gzip_page
def stream_video(request):
    video_path = os.path.join(BASE_DIR, 'static', 'video.mp4')  # Adjust the path
    with open(video_path, 'rb') as f:
        video_data = f.read(1024)  # Read video data in chunks
        while video_data:
            yield video_data
            video_data = f.read(1024)
    return HttpResponseNotFound()


class StreamVideoView(View):

    async def stream_video(self):
        video_path = os.path.join(BASE_DIR, "static", "video.mp4")
        cap = cv2.VideoCapture(video_path)

        while True:
            success, frame = cap.read()
            if not success:
                break

            # Convert the frame to JPEG format
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            await asyncio.sleep(0.09)

    async def get(self, request, *args, **kwargs):
        return StreamingHttpResponse(self.stream_video(), content_type='multipart/x-mixed-replace; boundary=frame')


class PredictVideoView(View):
    def get(self, request, *args, **kwargs):
        input_url = request.GET.get("url", None)
        if not input_url:
            raise Exception("Predict URL is undefined")
        return JsonResponse({
            "success": True,
            "path": input_url
        })

