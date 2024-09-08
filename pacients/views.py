from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets, status, permissions
from .serializers import PacientSerializer
from pacients.models import Pacient
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny


class PacientViewSet(viewsets.ModelViewSet):
    queryset = Pacient.objects.all()
    serializer_class = PacientSerializer
    permission_classes = [AllowAny] 

    @action(detail=True, methods=['post'])
    def update_token(self, request, pk=None):
        patient = self.get_object()
        token = request.data.get('expo_push_token')
        if token:
            patient.expo_push_token = token
            patient.save()
            return Response({"status": "Token atualizado com sucesso"})
        else:
            return Response({"error": "Token não fornecido"}, status=400)
        
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        return Response({"message": "Delete method not allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)