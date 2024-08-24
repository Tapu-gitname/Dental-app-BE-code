from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.decorators import action, api_view
from dental.models import *
from dental.serializers import *
from rest_framework.response import Response
from rest_framework import status
from decimal import Decimal
from datetime import date, datetime, time
from django.db.models import Sum

# Create your views here.
# def index(request):
#     return HttpResponse("Hello World. You are at Dental app")

class PatientViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = Patient.objects.all()
        serializer = PatientSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        serializer = PatientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, pk=None):
        queryset = Patient.objects.all()
        try:
            patient = queryset.get(id = pk)
        except Patient.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = PatientSerializer(patient)
        return Response(serializer.data)
    
    def update(self, request, pk=None):
        patient= get_object_or_404(Patient, pk=pk)
        serializer = PatientSerializer(patient, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        patient = get_object_or_404(Patient, pk=pk)
        patient.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
@api_view(['GET'])
def get_all_treatments(request):
    queryset = DentalTreatment.objects.all()
    serializer = DentalTreatmentSerializer(queryset, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_remaining_amount(request):
    # Extract patient_id from query parameters
    patient_id = request.query_params.get('patient_id')
    
    if not patient_id:
        return Response({"error": "patient_id is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    # Fetch the remaining amount, ordering by id in descending order, and get the first result
    remaining_amount = Treatment.objects.filter(patient_id=patient_id).order_by('-id').values_list('remaining_amount', flat=True).first()
    print('remaining amount is ====>', remaining_amount)
    
    if remaining_amount is None:
        return Response({"error": "Treatment not found for the given patient_id"}, status=status.HTTP_404_NOT_FOUND)
    
    # Return the remaining amount as JSON
    return Response({"remaining_amount": remaining_amount}, status=status.HTTP_200_OK)

@api_view(['POST'])
def update_fee(request):
    try:
        patient = Patient.objects.get(id=request.data.get('patient'))
        treatment_cost = patient.cost
        amount_paid = request.data.get('amount_paid')


        # Fetch remaining amount from the latest treatment or set to treatment cost if no previous treatment exists
        try:
            remaining_amount = Treatment.objects.filter(patient=patient).order_by('-created_at').values_list('remaining_amount', flat=True).first()

            if remaining_amount is None:
                remaining_amount = treatment_cost
            if remaining_amount == 0:
                return Response({'msg': 'Patient have already paid all the fee'})
            
            if remaining_amount > treatment_cost :
                return Response({'msg': "patient's remaining fees exceeds Toatal treatment cost"})
            
        except Treatment.DoesNotExist:
            remaining_amount = treatment_cost

        # Calculate new remaining amount
        remaining_amount = Decimal(remaining_amount) - Decimal(amount_paid)

        # Create and save the Treatment instance
        treatment = Treatment(
            patient=patient,
            treatment_cost=treatment_cost,
            amount_paid=amount_paid,
            remaining_amount=remaining_amount
        )
        treatment.save()

        # Return the serialized response
        response_serializer = TreatmentSerializer(treatment)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

    except Patient.DoesNotExist:
        return Response({'error': 'Patient not found.'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        print("Exception occurred: ", e)
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
def date_range_revenue(request):
    def daily_revenue():
        now = datetime.now()
        start_date = datetime.combine(now.date(), time.min)
        end_date = datetime.now()

        today_amount_paid = Treatment.objects.filter(
        created_at__range=(start_date, end_date)
        ).aggregate(total_paid=Sum('amount_paid'))['total_paid']
        
        if today_amount_paid is None:
            today_amount_paid = 0

        return today_amount_paid
    
    def monthly_revenue():
        now = datetime.now()
        start_date = datetime(now.year, now.month, 1)
        end_date = now

        monthly_amount_paid = Treatment.objects.filter(
        created_at__range=(start_date, end_date)
        ).aggregate(total_paid=Sum('amount_paid'))['total_paid']

        if monthly_amount_paid is None:
            monthly_amount_paid = 0
    
        return monthly_amount_paid
    
    def yearly_revenue():
        now = datetime.now()
        start_date = datetime(now.year, 1, 1)
        end_date = now

        yearly_amount_paid = Treatment.objects.filter(
        created_at__range=(start_date, end_date)
        ).aggregate(total_paid=Sum('amount_paid'))['total_paid']

        if yearly_amount_paid is None:
            yearly_amount_paid = 0

        return yearly_amount_paid
    
    return Response({
        'daily_revenue': daily_revenue(),
        'monthly_revenue': monthly_revenue(),
        'yearly_revenue': yearly_revenue()
    }, status=status.HTTP_200_OK)




