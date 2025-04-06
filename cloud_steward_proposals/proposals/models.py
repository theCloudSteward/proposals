import uuid
from django.db import models
from django.utils import timezone

def thirty_days_from_now():
    return timezone.now() + timezone.timedelta(days=30)

def generate_slug():
    # Generate an 8-character hexadecimal string.
    # You could also use the full uuid if you prefer.
    return uuid.uuid4().hex[:8]

class ClientPage(models.Model):
    # The slug field will use generate_slug() to set a default value.
    slug = models.SlugField(unique=True, default=generate_slug)
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
