from rest_framework import status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action

from ..models import PassengerPlane, Series
from ..helpers.plane_reader import get_reader
from ..helpers.errors import PlaneReaderError
from .serializers import PassengerPlaneSerializer, SeriesSerializer


# Creat CRUD for series
class SeriesViewSet(ModelViewSet):
    queryset = Series.objects.all()
    serializer_class = SeriesSerializer


class PlaneViewSet(ModelViewSet):
    queryset = PassengerPlane.objects.all()
    serializer_class = PassengerPlaneSerializer

    @action(detail=False, methods=["post"])
    def many(self, request: Request):
        data = request.data
        reader = get_reader(data)
        try:
            reader.save_data()
        except PlaneReaderError as exc:
            return Response(
                {"msg": "Oops, something went wrong!", "details": exc.errs},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response({"msg": "Success"}, status=status.HTTP_201_CREATED)
