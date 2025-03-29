# proposals/serializers.py
from rest_framework import serializers
from .models import ClientPage

class ClientPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientPage
        fields = '__all__'
