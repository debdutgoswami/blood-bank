from rest_framework.generics import CreateAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.gis.measure import D
from django.db.models import QuerySet

from .fields import PointField
from .serializers import DonorSerializer, RequestTicketSerializer
from .models import Donor, RequestTicket
from .utils import get_coordinates


# Create your views here.
class RetrieveViewByAddress(APIView):
    """
    #! MUST BE INHERITED

    Generic GET view for fetching by blood group and (lat, lon) or address.
    """
    model = None  # this fields should be overridden inside the sub class
    serializer = None  # this fields should be overridden inside the sub class

    def get(self, request: Request):
        """
        Returns a list of users by location

        @query_params
        lat (float)
        lon (float)
        bloodgroup (str): `+` sign needs to be urlencoded to `%2B`. Example: B+ would be B%2B
        address (str): url safe address
        """

        if not self.model:
            raise NotImplementedError("Model not provided")
        if not self.serializer:
            raise NotImplementedError("Serializer not provided")

        def get_donors_from_coordinate(latitude: float, longitude: float) -> QuerySet:
            pnt = PointField().to_internal_value(
                {
                    "latitude": latitude,
                    "longitude": longitude,
                }
            )
            # __distance_lte is pronounced as `distance less than or equal to`
            # this basically filters out all the coordinates which `distance are less than or equal to`
            # the point specified and D(km=distance)
            return self.model.objects.filter(
                bloodgroup__exact=blood_group,
                address__coordinate__distance_lte=(pnt, D(km=int(distance)))
            )

        params: dict = request.query_params
        blood_group: str = params.get('bloodgroup')
        if not blood_group:
            return Response(data={"status": "ERROR", "message": "Blood group is missing"}, status=status.HTTP_200_OK)
        endswith_plus_or_minus = not blood_group.endswith('+') and not blood_group.endswith('-')
        if endswith_plus_or_minus:
            return Response(
                data={
                    "status": "ERROR",
                    "message": "Blood group must end with + or -"
                },
                status=status.HTTP_200_OK
            )
        distance = params.get('distance', 5)
        lat, lon = params.get('lat'), params.get('lon')
        address = params.get('address')
        if not lat or not lon:
            if not address:
                donors = self.model.objects.all()
            else:
                res = get_coordinates(address)
                donors = get_donors_from_coordinate(res['lat'], res['lon'])
        else:
            donors = get_donors_from_coordinate(lat, lon)
        # many=True param specifies that the data passed is a query set
        data = self.serializer(donors, many=True).data
        return Response(data={"status": "OK", "data": data}, status=status.HTTP_200_OK)


class DonorCreateView(CreateAPIView):
    queryset = Donor
    serializer_class = DonorSerializer


class RequestTicketCreateView(CreateAPIView):
    queryset = RequestTicket
    serializer_class = RequestTicketSerializer


class DonorRetrieveView(RetrieveViewByAddress):
    model = Donor
    serializer = DonorSerializer


class RequestTicketRetrieveView(RetrieveViewByAddress):
    model = RequestTicket
    serializer = RequestTicketSerializer
