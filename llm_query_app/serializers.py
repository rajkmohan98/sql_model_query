from rest_framework import serializers
from .models import QueryResponse

class QueryResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = QueryResponse
        fields = '__all__'
