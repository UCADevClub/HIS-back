from django.urls import path
from .views import TreatmentByAppointmentView, TreatmentCreateView, TreatmentDetailView, TreatmentReferralUpdateView, TreatmentUpdateView

app_name = 'treatment'

urlpatterns = [
    path('create/', TreatmentCreateView.as_view(), name='treatment-create'),
    path('detail/<int:pk>', TreatmentDetailView.as_view(), name='treatment-detail'),
    path('update/<int:pk>', TreatmentUpdateView.as_view(), name='treatment-update'),
    path('update/referral/<int:pk>/', TreatmentReferralUpdateView.as_view(), name='treatment-referral-update'),
    path('by-appointment/', TreatmentByAppointmentView.as_view(), name='treatment-by-appointment'),
]
