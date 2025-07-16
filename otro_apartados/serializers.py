# otro_apartados/serializers.py

from rest_framework import serializers
from .models import Elemento

class ElementoSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Elemento
        fields = '__all__'
        read_only_fields = ['fecha_creacion', 'fecha_modificacion', 'user']
