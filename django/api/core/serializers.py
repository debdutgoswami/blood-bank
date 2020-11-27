from rest_framework import serializers
from .models import Donor, RequestTicket, Address
from .fields import PointField


class AddressSerializer(serializers.ModelSerializer):
    coordinate = PointField(read_only=True)

    class Meta:
        model = Address
        fields = [
            "address_line_1",
            "address_line_2",
            "city",
            "zipcode",
            "state",
            "country",
            "coordinate",
        ]


class DonorSerializer(serializers.ModelSerializer):
    address = AddressSerializer()

    class Meta:
        model = Donor
        fields = [
            "name",
            "email",
            "sex",
            "phone",
            "bloodgroup",
            "age",
            "weight",
            "address",
        ]

    def create(self, validated_data: dict):
        """
        Creates a Donor
        """
        address_input = validated_data.pop("address")
        # for relations, we need to separately create them in table
        address_obj = Address.objects.create(**address_input)
        return self.Meta.model.objects.create(address=address_obj, **validated_data)


class RequestTicketSerializer(serializers.ModelSerializer):
    address = AddressSerializer()

    class Meta:
        model = RequestTicket
        fields = [
            "name",
            "email",
            "phone",
            "bloodgroup",
            "address"
        ]

    def create(self, validated_data: dict):
        """
        Creates Request Tickets
        """
        address_input = validated_data.pop("address")
        # for relations, we need to separately create them in table
        address_obj = Address.objects.create(**address_input)
        return self.Meta.model.objects.create(address=address_obj, **validated_data)
