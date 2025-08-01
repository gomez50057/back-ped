# otro_apartados/serializers.py

from rest_framework import serializers
from .models import Elemento

class ElementoSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Elemento
        fields = '__all__'
        read_only_fields = ['fecha_creacion', 'fecha_modificacion', 'user']

# otro_apartados/serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Elemento

class ElementoSerializerFull(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(read_only=True, slug_field='username')

    class Meta:
        model = Elemento
        fields = [
            'user',
            'envio_final',
            'asIs',
            'justification',
            'page',
            'sectionName',
            'shouldBe',
            'fecha_creacion',
            'fecha_modificacion',
        ]
