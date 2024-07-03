from django.urls import path,include
from . import views
from rest_framework import routers
from dental.views import PatientViewSet

router = routers.DefaultRouter()
router.register(r'patients', PatientViewSet)
# router.register(r'patients', PatientViewSet)

urlpatterns = [
    # path("", views.index, name="index"),
    path('',include(router.urls))
]