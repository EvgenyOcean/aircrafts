from rest_framework import serializers

from ..models import PassengerPlane, Series


class TechnicalPlaneDetailsSerializer(serializers.ModelSerializer):
    fuel_tank_capacity = serializers.ReadOnlyField()
    min_fuel_consumption = serializers.ReadOnlyField()
    max_fuel_consumption = serializers.ReadOnlyField()
    max_mins_in_flight = serializers.ReadOnlyField()

    class Meta:
        model = PassengerPlane
        fields = [
            "fuel_tank_capacity",
            "min_fuel_consumption",
            "max_fuel_consumption",
            "max_mins_in_flight",
        ]


class PassengerPlaneSerializer(TechnicalPlaneDetailsSerializer):
    series_code = serializers.SlugRelatedField(
        slug_field="code", queryset=Series.objects.all(), source="series"
    )
    series_name = serializers.ReadOnlyField(source="series.name")

    class Meta:
        model = PassengerPlane
        exclude = ["series"]


class SeriesSerializer(serializers.ModelSerializer):
    planes = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Series
        fields = "__all__"
