from django.urls import path
from .views import TreatmentListView, TreatmentView, TreatmentDetailView, TreatmentUpdateView

app_name = 'treatment'

urlpatterns = [
    path('treatment/', TreatmentView.as_view(), name='treatment-create'),
    path('treatment-detail/<int:pk>', TreatmentDetailView.as_view(), name='treatment-detail'),
    path('update/<int:pk>', TreatmentUpdateView.as_view(), name='treatment-update'),
    path('treatments/<int:patient_id>/', TreatmentListView.as_view(), name='treatment-list'),
]
