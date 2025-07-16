from rest_framework import serializers
from .models import NewIndicadorProposal

class NewIndicadorProposalSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)
    class Meta:
        model = NewIndicadorProposal
        fields = '__all__'
        read_only_fields = ['user', 'created_at', 'updated_at']
