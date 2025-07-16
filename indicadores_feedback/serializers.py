from rest_framework import serializers
from .models import IndicadoresFeedback

class IndicadoresFeedbackSerializer(serializers.ModelSerializer):
    usuario = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = IndicadoresFeedback
        fields = ['id', 'usuario', 'envio_final', 'feedback', 'created_at', 'updated_at']