from django.shortcuts import render
from django.views import View
from django.http import JsonResponse

# Create your views here.
class AccidentListView(View):
    def get(self, request, *args, **kwargs):
        return JsonResponse({
            "success" : True,
            "post" : False
        })
    
    def post(self, request, *args, **kwargs):
        return JsonResponse({
            "success" : True,
            "post" : True
        })