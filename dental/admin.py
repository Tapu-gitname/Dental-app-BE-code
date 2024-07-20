from django.contrib import admin
from dental.models import *

# Register your models here.

class PatientAdmin(admin.ModelAdmin):
    list_display=('id', 'name', 'phone', 'treatment')
    search_fields=('name',)

class DentalTreatmentAdmin(admin.ModelAdmin):
    list_display=('id', 'name')

class TreatmentAdmin(admin.ModelAdmin):
    list_display=('patient_name', 'treatment_cost', 'remaining_amount', 'amount_paid', 'created_at')

    def patient_name(self, obj):
        return obj.patient.name
    # created_at.short

admin.site.register(Patient, PatientAdmin)
admin.site.register(DentalTreatment, DentalTreatmentAdmin)
admin.site.register(Treatment, TreatmentAdmin)
