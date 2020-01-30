from rest_framework import generics
from rest_framework.exceptions import NotFound
from bank_admin.models import Admin, Bank
from .serializers import *
from rest_framework.permissions import *
from .permission import IsSuperUser, IsSimpleUser
from rest_framework.response import Response
from rest_framework import status


class OperationList(generics.ListAPIView):
    serializer_class = OperationSerializer
    permission_classes = [IsSuperUser]

    def get_queryset(self):
        try:
            admin = Admin.objects.get(admin__username=self.request.user)
        except ObjectDoesNotExist:
            raise NotFound("You don't have admin account")
        all_operation = Operation.objects.all().filter(bank_fk__name=admin.bank_fk.name)
        client = self.request.query_params.get('client', None)
        destination = self.request.query_params.get('destination', None)

        if client is not None:
            all_operation = all_operation.filter(client_fk__user__username=client)
        if destination is not None:
            all_operation = all_operation.filter(destination_fk__user__username=destination)

        return all_operation


class DetailOperation(generics.RetrieveDestroyAPIView):
    serializer_class = DetailOperationSerializer
    permission_classes = [IsSuperUser]

    def get_queryset(self):
        admin = Admin.objects.get(admin__username=self.request.user)
        return Operation.objects.all().filter(bank_fk__name=admin.bank_fk.name)


class CreateOperation(generics.CreateAPIView):
    queryset = Operation.objects.all()
    permission_classes = [IsAuthenticated, IsSimpleUser]
    serializer_class = CreateOperationSerializer

    def post(self, request, *args, **kwargs):
        # new_request = dict(request.data)
        # new_request.update({'client_fk': [str(Client.objects.get(user__username=request.user).pk)]})
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response({"detail": "incorrectly date"}, status=status.HTTP_400_BAD_REQUEST)
