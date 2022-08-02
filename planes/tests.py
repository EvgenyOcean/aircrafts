from time import sleep
from math import log10

from model_bakery import baker
from django.test import TestCase
from django.db.utils import IntegrityError

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
