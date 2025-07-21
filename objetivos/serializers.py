from rest_framework import serializers
from .models import ObjetivoSet, Objetivo, Estrategia, Linea, FeedbackAvance

class LineaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Linea
        fields = ('pk', 'clave', 'text')

class EstrategiaSerializer(serializers.ModelSerializer):
    lineas = LineaSerializer(many=True, read_only=True)
    class Meta:
        model = Estrategia
        fields = ('pk', 'clave', 'nombre', 'lineas')

class ObjetivoSerializer(serializers.ModelSerializer):
    estrategias = EstrategiaSerializer(many=True, read_only=True)
    class Meta:
        model = Objetivo
        fields = ('pk', 'clave', 'nombre', 'estrategias')

class ObjetivoSetSerializer(serializers.ModelSerializer):
    objetivos = ObjetivoSerializer(many=True, read_only=True)
    class Meta:
        model = ObjetivoSet
        fields = ('pk', 'id', 'objetivos', 'creado', 'actualizado')


class FeedbackAvanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedbackAvance
        fields = [
            'id', 'user', 'clave', 'acuerdo', 'comoDecir', 'justificacion', 'envio_final', 
            'created', 'updated'
        ]
        read_only_fields = ['id', 'user', 'created', 'updated']
