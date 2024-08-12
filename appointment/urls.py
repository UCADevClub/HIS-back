from django.urls import path
from .views import (
    AppointmentCreateView,
    AppointmentListView, 
    AppointmentPaymentStatusUpdateView,
    AppointmentStatusUpdateView,
    AppointmentDetailView
    )

app_name = 'appointment'

urlpatterns = [
    path('create/', AppointmentCreateView.as_view(), name='appointment-create'),
    path('<int:pk>/update-status/', AppointmentStatusUpdateView.as_view(), name='appointment-update-status'),
    path('<int:pk>/update-payment-status/', AppointmentPaymentStatusUpdateView.as_view(), name='appointment-update-payment-status'),
    path('<int:pk>/', AppointmentDetailView.as_view(), name='appointment-detail'),
    path('doctor/<doctor_id>/today/', AppointmentListView.as_view(), name='appointment-detail'),
]