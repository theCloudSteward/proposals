# cloud_steward_proposals/urls.py
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView

# views that already existed
from proposals.views import (
    create_checkout_session,
    get_checkout_session_details,
)

# NEW – import the webhook view you just created
from proposals.webhooks import stripe_webhook

urlpatterns = [
    # ── Django Admin ────────────────────────────────────────────────
    path("admin/", admin.site.urls),

    # ── API End‑points (existing) ───────────────────────────────────
    path(
        "api/create-checkout-session/",
        create_checkout_session,
        name="create-checkout-session",
    ),
    path(
        "api/order/success/",
        get_checkout_session_details,
        name="order-success",
    ),

    # ── Stripe Webhook (new) ────────────────────────────────────────
    # Stripe will POST events (payment_intent.succeeded, invoice.paid, etc.)
    # to this URL.  Make sure you add the same URL in the Stripe Dashboard.
    path("stripe/webhook/", stripe_webhook, name="stripe-webhook"),

    # ── Include the rest of your proposals‑app API routes ───────────
    path("api/", include("proposals.urls")),

    # ── Catch‑all for the React frontend ────────────────────────────
    # (Only runs after everything above fails to match.)
    re_path(r"^(?!api/).*$", TemplateView.as_view(template_name="index.html")),
]
