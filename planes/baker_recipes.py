from model_bakery.recipe import Recipe, foreign_key
from .models import Series, PassengerPlane

series_ok = Recipe(
    Series,
    code=42,
    name="Okaish"
)
series_with_negatives = Recipe(
    Series,
    code=-12,
    name="Hackerish"
)
series_with_zero = Recipe(
    Series,
    code=0,
    name="Hackerish2"
)

plane_ok = Recipe(
    PassengerPlane,
    series=foreign_key(series_ok),
    name="Whateversday",
    capacity=32767
)
plane_with_negatives = Recipe(
    PassengerPlane,
    series=foreign_key(series_ok),
    capacity=-25
)