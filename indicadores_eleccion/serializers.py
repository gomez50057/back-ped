from rest_framework import serializers
from .models import Indicator, UserIndicatorSelection

class IndicatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Indicator
        fields = ('id', 'code', 'name')

class UserIndicatorSelectionSerializer(serializers.ModelSerializer):
    axes = serializers.PrimaryKeyRelatedField(
        queryset=Indicator.objects.all(),
        many=True,
        source='selected_indicators'
    )

    class Meta:
        model = UserIndicatorSelection
        fields = ("id", "axes", "created_at", "updated_at")

    def create(self, validated_data):
        indicators = validated_data.pop("selected_indicators")
        instance = UserIndicatorSelection.objects.create(**validated_data)
        instance.selected_indicators.set(indicators)
        return instance

    def update(self, instance, validated_data):
        indicators = validated_data.pop("selected_indicators", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if indicators is not None:
            instance.selected_indicators.set(indicators)
        return instance
