from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from core.models import Report
from django.core.paginator import Paginator

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


class SingleRecordView(View):
    def get(self, request, *args, **kwargs):
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

        return JsonResponse({
            "success": True,
            "data": {
                "source": report.source,
                "confidence": report.confidence,
                "status": report.status,
                "timestamp_start": report.timestamp_start,
                "timestamp_end": report.timestamp_end
            }
        })


# Create your views here.
@method_decorator(csrf_exempt, name="dispatch")
class AccidentListView(View):

    def get(self, request, *args, **kwargs):
        current_page = request.GET.get('page', 1)

        total_pages = 1
        output = []
        all_reports = Report.objects.all()
        if all_reports.count() > 0:
            paginator = Paginator(all_reports, 10)
            total_pages = paginator.num_pages
            reports = paginator.page(current_page)

            for report in reports:
                output.append({
                    "source": report.source,
                    "confidence": report.confidence,
                    "status": report.status,
                    "timestamp_start": report.timestamp_start,
                    "timestamp_end": report.timestamp_end
                })

        return JsonResponse({
            "success": True,
            "data": output,
            "current": current_page,
            "total": total_pages
        })

    def post(self, request, *args, **kwargs):
        try:
            source = request.POST.get("source", None)
            confidence = request.POST.get("confidence", 0)
            status = request.POST.get("status", "minor")
            timestamp_end = request.POST.get("timestamp_end", 0)
            timestamp_start = request.POST.get("timestamp_start", 0)

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
                timestamp_end=timestamp_end
            )
            report.clean_fields()
            report.save()

            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                "notification",
                {
                    'type': 'send_notification',
                    'notification': {
                        "type": "new_alert",
                        "data": {
                            "id": report.id,
                            "source": source,
                            "confidence": confidence,
                            "status": status,
                            "timestamp_start": report.timestamp_start,
                            "timestamp_end": report.timestamp_end
                        }
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
