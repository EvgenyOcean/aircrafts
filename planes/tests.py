from math import log10

from model_bakery import baker
from django.test import TestCase
from django.db.utils import IntegrityError
from rest_framework.test import APIClient

from .models import Series, PassengerPlane
from .helpers.roundings import round_down, round_up


############################
# Testing models real quick.
############################
class TestModels(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.plane_one = baker.make_recipe("planes.plane_ok")
        cls.series_one = cls.plane_one.series
        cls.TANK_COEF = 200
        cls.FUEL_PER_MINUTE_COEF = 0.8
        cls.FUEL_INCREASED_PER_PERSON = 0.002

    def setUp(self):
        pass

    def test_series_str(self):
        self.assertEqual(str(self.series_one), "Series: #42 | Okaish")

    def test_plane_str(self):
        self.assertEqual(str(self.plane_one), "Plane: #42 | Whateversday")

    def test_negatives_in_series(self):
        with self.assertRaises(IntegrityError):
            baker.make_recipe("planes.series_with_negatives")

    def test_negatives_in_code(self):
        with self.assertRaises(IntegrityError):
            baker.make_recipe("planes.plane_with_negatives")

    def test_zero_code_in_series(self):
        with self.assertRaises(IntegrityError):
            baker.make_recipe("planes.series_with_zero")
        
    def test_fuel_tank_capacity(self):
        expected = self.TANK_COEF * self.series_one.code
        self.assertEqual(self.plane_one.fuel_tank_capacity, expected)

    def test_min_fuel_consumption(self):
        expected = round_up(log10(self.series_one.code) * self.FUEL_PER_MINUTE_COEF, 4)
        self.assertEqual(self.plane_one.min_fuel_consumption, expected)

    def test_max_fuel_consumption(self):
        expected = round_up(
            self.plane_one.min_fuel_consumption
            + self.plane_one.capacity * self.FUEL_INCREASED_PER_PERSON,
            4,
        )
        self.assertEqual(self.plane_one.max_fuel_consumption, expected)

    def test_max_mins_in_flight(self):
        expected = round_down(self.plane_one.fuel_tank_capacity / self.plane_one.max_fuel_consumption)
        self.assertEqual(expected, self.plane_one.max_mins_in_flight)
        self.assertGreater(int(expected), 0)


############################
# Testing views real quick.
############################
class TestPlaneViewSet(TestCase):
    def test_many_empty_values(self):
        client = APIClient()
        res = client.post(
            '/api/v1/planes/many/', 
            [], 
            format='json')
        self.assertEqual(res.status_code, 400)
        
    def test_many_expected_values(self):
        client = APIClient()
        res = client.post(
            '/api/v1/planes/many/', 
            [
                {"series_code": 1, "series_name": "One", "capacity": 1},
                {"series_code": 2, "series_name": "Two", "capacity": 20},
                {"series_code": 3, "series_name": "Three", "capacity": 30},
                {"series_code": 4, "series_name": "Four", "capacity": 4},
                {"series_code": 5, "series_name": "Five", "capacity": 50},
                {"series_code": 6, "series_name": "Sex", "capacity": 60},
                {"series_code": 7, "series_name": "Seven", "capacity": 7},
                {"series_code": 8, "series_name": "Eight", "capacity": 80},
                {"series_code": 9, "series_name": "Nine", "capacity": 9},
                {"series_code": 10, "series_name": "Ten", "capacity": 100}
            ],
            format='json')
        self.assertEqual(res.status_code, 201)
        self.assertEqual(Series.objects.count(), 10)
        self.assertEqual(PassengerPlane.objects.count(), 10)

    def test_many_duplicate_values(self):
        client = APIClient()
        res = client.post(
            '/api/v1/planes/many/', 
            [
                {"series_code": 1, "series_name": "One", "capacity": 1},
                {"series_code": 1, "series_name": "Four", "capacity": 4}
            ],
            format='json')
        self.assertEqual(res.status_code, 400)
