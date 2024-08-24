from django.urls import path,include
from . import views
from rest_framework import routers
from dental.views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'patients', PatientViewSet, basename='patient')
# router.register(r'patients', PatientViewSet)

urlpatterns = [
    path('',include(router.urls)),
    path('get_all_treatments/', get_all_treatments, name='get_all_treatments'),
    path('update_fee/', update_fee),
    path('gross_revenue/', date_range_revenue),
    path('get_remaining_amount', get_remaining_amount)
]
# urlpatterns = router.urls