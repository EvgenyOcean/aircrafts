from rest_framework.exceptions import APIException


class PlaneReaderError(Exception):
    def __init__(self, errs: list = []) -> None:
        self.errs = errs


class ReaderError(APIException):
    status_code = 400
    default_detail = 'The data you sent cannot be processed.'
    default_code = 'reader_not_implemented'

class SerializingSeriesError(PlaneReaderError): ...
class SerializingPlanesError(PlaneReaderError): ...
