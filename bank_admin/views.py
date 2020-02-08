from rest_framework import generics
from rest_framework.permissions import *
from rest_framework.response import Response
from rest_framework import status

from .serializers import CreateAdminSerializer

from .models import Admin
from operation.permission import IsSuperUser


class CreateAdmin(generics.CreateAPIView):
    queryset = Admin.objects.all()
    serializer_class = CreateAdminSerializer
    permission_classes = [IsSuperUser]


class AccountAdmin(generics.ListAPIView):
    serializer_class = CreateAdminSerializer
    permission_classes = [IsSuperUser]

    def get_queryset(self):
        return Admin.objects.all().filter(admin__username=self.request.user)


class DetailAdmin(generics.RetrieveDestroyAPIView):
    queryset = Admin.objects.all()
    serializer_class = CreateAdminSerializer
    permission_classes = [IsSuperUser]

    def get_object(self):
        return Admin.objects.get(admin__username=self.request.user)

    def delete(self, request, *args, **kwargs):
        admin = self.get_object()
        admin.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
