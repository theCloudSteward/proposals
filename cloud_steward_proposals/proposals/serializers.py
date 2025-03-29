# proposals/serializers.py
from rest_framework import serializers
from .models import ClientPage

class ClientPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientPage
        fields = ['slug', 'client_name','company_name', 'project_name','project_details', 'project_price', 'is_consultant', 'created_at', 'expires_at']
