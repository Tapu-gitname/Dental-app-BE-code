from rest_framework import serializers
from dental.models import Patient

class PatientSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model=Patient
        fields="__all__"