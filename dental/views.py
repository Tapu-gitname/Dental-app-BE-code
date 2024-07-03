from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.decorators import action
from dental.models import Patient
from dental.serializers import PatientSerializer

# Create your views here.
# def index(request):
#     return HttpResponse("Hello World. You are at Dental app")

class PatientViewSet(viewsets.ModelViewSet):
    queryset= Patient.objects.all()
    serializer_class=PatientSerializer