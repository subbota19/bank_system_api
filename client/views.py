from django.shortcuts import get_object_or_404

from rest_framework import generics, mixins
from .serializers import CreateClientSerializer, DetailClientSerializer
from .models import Client
from rest_framework.response import Response
from rest_framework.permissions import *
from rest_framework import status


class CreateClient(generics.CreateAPIView):
    queryset = Client.objects.all()
    serializer_class = CreateClientSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({"detail": "incorrectly date"}, status=status.HTTP_400_BAD_REQUEST)


class AccountClient(generics.ListAPIView):
    serializer_class = CreateClientSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Client.objects.all().filter(user__username=self.request.user)


class DetailClient(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DetailClientSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return get_object_or_404(Client.objects.filter(user__username=self.request.user))
