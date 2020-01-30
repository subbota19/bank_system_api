from abc import ABC
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from .models import Operation
from client.models import Client
from bank.models import Bank


class OperationSerializer(serializers.ModelSerializer):
    """This class provides get-request with all operation """

    # SRF class allow get data in convenience view and choice needed field for view(slug_field)
    client_fk = serializers.StringRelatedField()
    destination_fk = serializers.StringRelatedField()
    bank_fk = serializers.SlugRelatedField(read_only=True, slug_field='name')

    class Meta:
        model = Operation
        fields = ['id', 'name', 'total', 'is_valid', 'client_fk', 'destination_fk', 'bank_fk']


class OperationRelatedField(serializers.RelatedField, ABC):
    """This class just override for different representations such as name """

    def display_value(self, instance):
        return instance

    def to_representation(self, value):
        return str(value)

    def to_internal_value(self, data):
        try:
            return Client.objects.get(name=data)
        except ObjectDoesNotExist:
            return Bank.objects.get(name=data)


class CreateOperationSerializer(serializers.ModelSerializer):
    """This class need for creating new object after post-request,in ORF class you should to pass queryset"""
    client_fk = Client
    destination_fk = Client
    bank_fk = Bank

    class Meta:
        model = Operation
        fields = ['name', 'total', 'is_valid', 'client_fk', 'destination_fk', 'bank_fk']

    def create(self, validated_data):
        # use save in serializer because db send error('IntegrityError: UNIQUE constraint failed')
        operation = Operation(**validated_data)
        operation.save()
        return operation


class DetailOperationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Operation
        fields = ['name', 'total', 'is_valid', 'client_fk', 'destination_fk', 'bank_fk']

    def update(self, instance, validated_data):
        instance.delete()
        operation = Operation(**validated_data)
        operation.save()
        return operation
