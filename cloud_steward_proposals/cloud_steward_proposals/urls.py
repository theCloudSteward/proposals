from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView

# views wired directly in the project‑level urls
from proposals.views import (
    create_checkout_session,
    get_checkout_session_details,
)
from proposals.webhooks import stripe_webhook   # <-- NEW ‑ your webhook handler

urlpatterns = [
    # Django admin
    path("admin/", admin.site.urls),

    # REST endpoints that your React front‑end calls
    path("api/create-checkout-session/", create_checkout_session, name="create-checkout-session"),
    path("api/order/success/", get_checkout_session_details,    name="order-success"),

    # App‑level routers (e.g. /api/client‑pages/…)
    path("api/", include("proposals.urls")),

    # Stripe → Django Webhook (must be ABOVE the catch‑all so it’s matched first)
    path("stripe/webhook/", stripe_webhook, name="stripe-webhook"),

    # ------------------------------------------------------------
    # Catch‑all: serve React’s index.html for every non‑API route
    # (keep this LAST so it doesn’t swallow real back‑end URLs)
    # ------------------------------------------------------------
    re_path(r"^(?!api/).*$", TemplateView.as_view(template_name="index.html")),
]
