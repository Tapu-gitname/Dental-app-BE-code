from django.db import models
from decimal import Decimal

# Create your models here.

class Patient(models.Model):
    SEX_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    name = models.CharField(max_length=100, null=False, blank=False)
    address = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=15, null=False, blank=False, default='')
    age = models.IntegerField(null=True, blank=True)
    sex = models.CharField(max_length=1, choices=SEX_CHOICES, null=True, blank=True)
    treatment = models.TextField(max_length=100, null=True, blank=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    # def __str__(self):
    #     return {self.name} - {self.phone_number}


class Treatment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='treatments')
    treatment_cost = models.DecimalField(max_digits=10, decimal_places=2)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    remaining_amount = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Payment Received Date')
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Ensure treatment_cost is assigned from patient's cost if not set
        if self.treatment_cost is None:
            self.treatment_cost = self.patient.cost
        
        # Ensure Decimal type calculations for precision
        if self.remaining_amount is None:
            self.remaining_amount = Decimal(self.treatment_cost) - Decimal(self.amount_paid)
        
        super().save(*args, **kwargs)



    # def __str__(self):
    #     return self.patient

class DentalTreatment(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)


class PatientHistory(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    payment_recieve_date = models.DateTimeField(auto_now_add=True)

