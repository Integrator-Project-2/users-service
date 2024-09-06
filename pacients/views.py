from rest_framework.decorators import action
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets, status, permissions
from .serializers import PacientSerializer
from pacients.models import Pacient
from rest_framework.decorators import action

class PacientViewSet(viewsets.ModelViewSet):
    queryset = Pacient.objects.all()
    serializer_class = PacientSerializer

    def destroy(self, request, *args, **kwargs):
        return Response({"message": "Delete method not allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    @action(detail=False, methods=['post'], url_path='search-by-ids')
    def search_by_ids(self, request):
        patient_ids = request.data.get('patient_ids', [])
        
        print("pegando patient_ids: ", patient_ids)
        
        if not patient_ids:
            return Response({"error": "No patient IDs provided."}, status=status.HTTP_400_BAD_REQUEST)
        
        patients = Pacient.objects.filter(id__in=patient_ids)
        
        if not patients.exists():
            return Response({"error": "No patients found with the provided IDs."}, status=status.HTTP_404_NOT_FOUND)

        serializer = PacientSerializer(patients, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['post'], url_path='search-by-cpf')
    def search_by_cpf(self, request):
        cpf = request.data.get('cpf')
        if cpf is None:
            return Response({"error": "CPF is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            pacient = Pacient.objects.get(cpf=cpf)
            serializer = PacientSerializer(pacient) 
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Pacient.DoesNotExist:
            return Response({"error": "Pacient not found"}, status=status.HTTP_404_NOT_FOUND)