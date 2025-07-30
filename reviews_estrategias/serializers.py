from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType
from .models import CampoReview

class CampoReviewSerializer(serializers.ModelSerializer):
    # Represent content_object by its model name and object ID
    content_type = serializers.SlugRelatedField(
        slug_field='model',
        queryset=ContentType.objects.all(),
        help_text="Modelo del objeto revisado (ej.: 'objetivo', 'estrategia')."
    )
    object_id = serializers.IntegerField(help_text="ID del objeto revisado")
    reviewer = serializers.PrimaryKeyRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = CampoReview
        fields = [
            'id', 'content_type', 'object_id', 'reviewer',
            'field_name', 'is_valid', 'justification', 'reviewed_at'
        ]
        read_only_fields = ['reviewed_at']

    def create(self, validated_data):
        # Asigna automáticamente al revisor actual
        validated_data['reviewer'] = self.context['request'].user
        return super().create(validated_data)

