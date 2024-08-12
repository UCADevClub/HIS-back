from django.urls import path
from .views import TreatmentCreateView, TreatmentDetailView, TreatmentUpdateView

app_name = 'treatment'

urlpatterns = [
    path('create/', TreatmentCreateView.as_view(), name='treatment-create'),
    path('detail/<int:pk>', TreatmentDetailView.as_view(), name='treatment-detail'),
    path('update/<int:pk>', TreatmentUpdateView.as_view(), name='treatment-update'),
]
