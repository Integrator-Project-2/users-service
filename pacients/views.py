from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets, status
from .serializers import PacientSerializer
from pacients.models import Pacient

class PacientViewSet(viewsets.ModelViewSet):
    queryset = Pacient.objects.all()
    serializer_class = PacientSerializer

    def destroy(self, request, *args, **kwargs):
        return Response({"message": "Delete method not allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)