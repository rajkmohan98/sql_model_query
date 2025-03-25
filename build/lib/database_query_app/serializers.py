from rest_framework import serializers
from .models import SQLQueryResponse

class SQLQueryResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = SQLQueryResponse
        fields = "__all__"
