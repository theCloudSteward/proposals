from django.contrib import admin
from .models import ClientPage

@admin.register(ClientPage)
class ClientPageAdmin(admin.ModelAdmin):
    list_display = (
        'slug',
        'auto_link',
        'client_name',
        'company_name',
        'project_name',
        'project_notes',
        'project_summary',
        'project_objectives',
        'project_only_price',
        'project_with_subscription_price',
        'tier_1_subscription_price',
        'tier_2_subscription_price',
        'tier_3_subscription_price',
        'is_consultant',
        'created_at',
        'expires_at',
    )
