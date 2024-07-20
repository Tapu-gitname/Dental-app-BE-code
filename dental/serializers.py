from rest_framework import serializers
from dental.models import *

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model=Patient
        fields="__all__"

class DentalTreatmentSerializer(serializers.ModelSerializer):
    class Meta:
        model=DentalTreatment
        fields="__all__"

class TreatmentSerializer(serializers.ModelSerializer):
    # patient = serializers.PrimaryKeyRelatedField(queryset=Patient.objects.all())

    class Meta:
        model=Treatment
        fields="__all__"