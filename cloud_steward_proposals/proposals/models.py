# proposals/models.py
from django.db import models
from django.utils import timezone

def thirty_days_from_now():
    return timezone.now() + timezone.timedelta(days=30)

class ClientPage(models.Model):
    # For each custom page, store a unique slug or token
    slug = models.SlugField(unique=True)
    client_name = models.CharField(max_length=200, blank=True)
    company_name = models.CharField(max_length=200, blank=True)
    project_name = models.CharField(max_length=200, blank=True)
    project_details = models.TextField(blank=True)
    project_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    is_consultant = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(default=thirty_days_from_now)

def __str__(self):
    return f"{self.client_name} - {self.project_name}"
