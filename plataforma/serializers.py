# plataforma/serializers.py

from rest_framework import serializers
from .models import StrategicAxis, UserAxisSelection

class StrategicAxisSerializer(serializers.ModelSerializer):
    class Meta:
        model = StrategicAxis
        fields = ('id', 'code', 'name')

class UserAxisSelectionSerializer(serializers.ModelSerializer):
    axes = serializers.PrimaryKeyRelatedField(
        queryset=StrategicAxis.objects.all(),
        many=True,
        source='selected_axes'
    )

    class Meta:
        model = UserAxisSelection
        fields = ("id", "axes", "created_at", "updated_at")

    def create(self, validated_data):
        axes = validated_data.pop("selected_axes")
        instance = UserAxisSelection.objects.create(**validated_data)
        instance.selected_axes.set(axes)
        return instance

    def update(self, instance, validated_data):
        axes = validated_data.pop("selected_axes", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if axes is not None:
            instance.selected_axes.set(axes)
        return instance