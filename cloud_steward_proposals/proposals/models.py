from decimal import Decimal
from django.db import models
from django.utils import timezone
import uuid

def thirty_days_from_now():
    return timezone.now() + timezone.timedelta(days=30)

def generate_slug():
    return uuid.uuid4().hex[:8]

class ClientPage(models.Model):
    slug = models.SlugField(unique=True, default=generate_slug)
    auto_link = models.URLField(blank=True, editable=False)
    company_name = models.CharField(max_length=200, blank=True)
    client_name = models.CharField(max_length=200, blank=True)
    project_name = models.CharField(max_length=200, blank=True)
    project_notes = models.TextField(blank=True)
    project_summary = models.TextField(blank=True)
    project_objectives = models.TextField(blank=True)
    project_only_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    project_with_subscription_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    tier_1_subscription_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=Decimal('295'))
    tier_2_subscription_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=Decimal('649'))
    tier_3_subscription_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=Decimal('1475'))
    is_consultant = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(default=thirty_days_from_now)
    project_discount_percent = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.client_name or 'Unknown'} - {self.project_name or 'Unnamed Project'}"

    def save(self, *args, **kwargs):
        if (
            self.project_only_price not in (None, 0) and
            self.project_with_subscription_price not in (None, 0)
        ):
            percentage_discount = round(
                ((self.project_only_price - self.project_with_subscription_price) / self.project_only_price) * 100
            )
            self.project_discount_percent = int(percentage_discount)
        else:
            self.project_discount_percent = None


        if not self.slug:
            self.slug = generate_slug()
        self.auto_link = f"https://proposals.thecloudsteward.com/{self.slug}"
        super().save(*args, **kwargs)
