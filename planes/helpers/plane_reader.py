from abc import ABC, abstractmethod
from typing import IO, NoReturn

from django.db import transaction
from django.db.utils import IntegrityError

from ..api.serializers import PassengerPlaneSerializer, SeriesSerializer
from ..helpers.errors import PlaneReaderError, ReaderError, SerializingPlanesError, SerializingSeriesError


class PlaneKeeper(ABC):
    def __init__(self, data: list[dict]) -> None:
        self.data: list[dict] = data

    @abstractmethod
    def save_data(self) -> None:
        raise NotImplementedError()


class DataPlaneKeeper(PlaneKeeper):
    def read_from_data(self) -> None | NoReturn:
        series_list = []
        for datum in self.data:
            series_data = {}
            for k, v in datum.items():
                if k.startswith("series_"):
                    series_data[k[7:]] = v
            series_list.append(series_data)
        try:
            with transaction.atomic():
                s_serializer = SeriesSerializer(data=series_list, many=True)
                if not s_serializer.is_valid():
                    raise SerializingSeriesError(s_serializer.errors)
                s_serializer.save()

                p_serializer = PassengerPlaneSerializer(data=self.data, many=True)
                if not p_serializer.is_valid():
                    raise SerializingPlanesError(p_serializer.errors)
                p_serializer.save()
        except IntegrityError as err:
            raise PlaneReaderError(errs=err.args)

    def save_data(self) -> None | NoReturn:
        self.read_from_data()


class FilePlaneKeeper(PlaneKeeper):
    def read_from_data(self):
        pass

    def save_data(self):
        self.read_from_data()


def get_reader(data: IO | list) -> PlaneKeeper:
    readers = {"data": DataPlaneKeeper, "file": FilePlaneKeeper}

    try:
        data[0].get("series_id")
        reader = "data"
    except Exception as err:
        # For different parsing methods
        raise ReaderError()
    return readers[reader](data)
