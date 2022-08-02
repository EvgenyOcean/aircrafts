from math import log10
from uuid import uuid4

from django.db import models

from .helpers.roundings import round_down, round_up


# Create your models here.
class Series(models.Model):
    code = models.IntegerField("Series unique id", null=False, blank=False, unique=True)
    name = models.CharField(
        "Series name", max_length=36, null=False, unique=True, default=uuid4
    )

    def __str__(self):
        return f"Series: #{self.code} | {self.name}"


class Plane(models.Model):
    TANK_COEF = 200
    FUEL_PER_MINUTE_COEF = 0.8
    FUEL_INCREASED_PER_PERSON = 0.002

    name = models.CharField(
        "Plane name", max_length=36, null=False, unique=True, default=uuid4
    )
    capacity = models.IntegerField("People capacity", null=False, blank=False)

    series = models.ForeignKey(
        Series,
        on_delete=models.PROTECT,
        related_name="planes",
        null=False,
        to_field="code",
    )

    class Meta:
        abstract = True

    def __str__(self):
        return f"Plane: #{self.series.code} | {self.name}"


class PassengerPlane(Plane):
    @property
    def fuel_tank_capacity(self) -> float:
        return self.TANK_COEF * self.series.code

    @property
    def min_fuel_consumption(self) -> float:
        return round_up(log10(self.series.code) * self.FUEL_PER_MINUTE_COEF, 4)

    @property
    def max_fuel_consumption(self) -> float:
        return round_up(
            self.min_fuel_consumption + self.capacity * self.FUEL_INCREASED_PER_PERSON,
            4,
        )

    @property
    def max_mins_in_flight(self) -> float:
        return round_down(self.fuel_tank_capacity / self.max_fuel_consumption)
