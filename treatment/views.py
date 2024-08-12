from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Treatment
from .serializers import TreatmentCreateSerializer, TreatmentSerializer, TreatmentUpdateSerializer

class TreatmentCreateView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = TreatmentCreateSerializer(data=request.data)
        if serializer.is_valid():
            treatment = serializer.save()
            response_serializer = TreatmentCreateSerializer(treatment)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TreatmentDetailView(APIView):
    
    def get_object(self, pk):
        try:
            return Treatment.objects.get(pk=pk)
        except Treatment.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        treatment = self.get_object(pk)
        serializer = TreatmentSerializer(treatment)
        return Response(serializer.data)


class TreatmentUpdateView(APIView):

    def get_object(self, pk):
        try:
            return Treatment.objects.get(pk=pk)
        except Treatment.DoesNotExist:
            raise Http404

    def patch(self, request, pk, format=None):
        treatment = self.get_object(pk)
        serializer = TreatmentUpdateSerializer(treatment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)