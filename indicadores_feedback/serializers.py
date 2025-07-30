from rest_framework import serializers
from .models import IndicadoresFeedback

class IndicadoresFeedbackSerializer(serializers.ModelSerializer):
    usuario = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = IndicadoresFeedback
        fields = ['id', 'usuario', 'envio_final', 'feedback', 'created_at', 'updated_at']

        # serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import IndicadoresFeedback

User = get_user_model()

class IndicadoresFeedbackSerializerFull(serializers.ModelSerializer):
    # Representamos al usuario por su username
    user = serializers.SlugRelatedField(read_only=True, slug_field='username')

    class Meta:
        model = IndicadoresFeedback
        # Incluimos todos los campos
        fields = ['user', 'envio_final', 'feedback', 'created_at', 'updated_at']
