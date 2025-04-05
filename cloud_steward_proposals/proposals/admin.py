from django.contrib import admin
from .models import ClientPage

@admin.register(ClientPage)
class ClientPageAdmin(admin.ModelAdmin):
    list_display = ('slug', 'client_name','company_name', 'project_name','project_details', 'project_price', 'is_consultant', 'created_at', 'expires_at')