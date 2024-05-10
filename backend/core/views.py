from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from core.models import Report
from django.core.paginator import Paginator

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

# Create your views here.
@method_decorator(csrf_exempt, name="dispatch")
class AccidentListView(View):
    def get(self, request, *args, **kwargs):
        current_page = request.GET.get('page', 1)

        all_reports = Report.objects.all()
        
        paginator = Paginator(all_reports, 10)
        reports = paginator.page(current_page)

        output = []
        for report in reports:
            output.append({
                "source" : report.source,
                "location" : report.location,
                "confidence" : report.confidence,
                "status" : report.status,
                "timestamp" : report.timestamp
            })

        return JsonResponse({
            "success" : True,
            "data" : output,
            "current" : current_page,
            "total" : paginator.num_pages
        })
    
    def post(self, request, *args, **kwargs):
        try:
            source = request.POST.get("source", None)
            location = request.POST.get("location", None)
            confidence = request.POST.get("confidence", 0)
            status = request.POST.get("status", "minor")
            timestamp = request.POST.get("timestamp", 0)

            if not source:
                raise Exception("Source not found")
            
            if not location:
                raise Exception("Location not found")

            if not confidence:
                raise Exception("Confidence not found")
            
            if not status:
                raise Exception("Status not found")
            
            if not timestamp:
                raise Exception("Timestamp not found")
            
            report = Report(
                source=source,
                location=location,
                confidence=confidence,
                status=status,
                timestamp=timestamp,
            )
            report.clean_fields()
            report.save()

            return JsonResponse({
                "success" : True,
                "message" : "Record saved successfully"
            })
        except Exception as e:
            return JsonResponse({
                "success" : False,
                "error" : str(e)
            }, status=500)