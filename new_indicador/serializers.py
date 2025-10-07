from rest_framework import serializers
from .models import NewIndicadorProposal

class NewIndicadorProposalSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)
    class Meta:
        model = NewIndicadorProposal
        fields = '__all__'
        read_only_fields = ['user', 'created_at', 'updated_at']


# serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import NewIndicadorProposal

User = get_user_model()

class NewIndicadorProposalSerializerFull(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(read_only=True, slug_field='username')

    class Meta:
        model = NewIndicadorProposal
        fields = [
            'user',
            'indicator_name',
            'ped_alignment',
            'national_plan_alignment',
            'ods_alignment',
            'description',
            'periodicity',
            'trend',
            'baseline',
            'goal_2028',
            'goal_2040',
            'sources',
            'indicador',
            'created_at',
            'updated_at',
        ]
