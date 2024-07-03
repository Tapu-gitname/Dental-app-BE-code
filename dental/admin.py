from django.contrib import admin
from dental.models import Patient, Treatment

# Register your models here.

class PatientAdmin(admin.ModelAdmin):
    list_display=('name', 'phone_number', 'treatment')
    search_fields=('name',)

admin.site.register(Patient, PatientAdmin)
