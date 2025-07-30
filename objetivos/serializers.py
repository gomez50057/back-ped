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


#
# mustra todo
#


class LineaSerializerFull(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(read_only=True, slug_field='username')
    estrategia = serializers.SlugRelatedField(read_only=True, slug_field='nombre')
    class Meta:
        model = Linea
        fields = '__all__'

class EstrategiaSerializerFull(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(read_only=True, slug_field='username')
    objetivo = serializers.SlugRelatedField(read_only=True, slug_field='nombre')
    lineas = LineaSerializerFull(many=True, read_only=True)
    class Meta:
        model = Estrategia
        fields = '__all__'

class ObjetivoSerializerFull(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(read_only=True, slug_field='username')
    set = serializers.SlugRelatedField(read_only=True, slug_field='id')  # Si quieres el id, o cambia por otro campo
    estrategias = EstrategiaSerializerFull(many=True, read_only=True)
    class Meta:
        model = Objetivo
        fields = '__all__'

class ObjetivoSetSerializerFull(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(read_only=True, slug_field='username')
    objetivos = ObjetivoSerializerFull(many=True, read_only=True)
    class Meta:
        model = ObjetivoSet
        fields = ('pk', 'id', 'user', 'objetivos', 'creado', 'actualizado')
#
#
#
class FeedbackAvanceSerializerFull(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(read_only=True, slug_field='username')
    
    class Meta:
        model = FeedbackAvance
        fields = '__all__'