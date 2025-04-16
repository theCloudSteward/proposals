# cloud_steward_proposals/urls.py
#
# ├── cloud_steward_proposals   ← Django “project” pkg (this file lives here)
# │   ├── urls.py               ← **THIS FILE**
# │   └── settings.py
# ├── proposals                 ← Django “app” pkg
# │   ├── views.py
# │   └── webhooks.py           ← stripe_webhook lives here
#
# The import below (“proposals.webhooks”) is correct because “proposals”
# is a top‑level Python package (it has an __init__.py and is in INSTALLED_APPS).

from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt

from proposals.views import (
    create_checkout_session,
    get_checkout_session_details,
)
from proposals.webhooks import stripe_webhook          # <-- ✅ CORRECT import


urlpatterns = [
    # ---------------------------------------------------------------------
    # 1.  Admin
    # ---------------------------------------------------------------------
    path("admin/", admin.site.urls),

    # ---------------------------------------------------------------------
    # 2.  Checkout endpoints (called by your React front‑end)
    # ---------------------------------------------------------------------
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

    # ---------------------------------------------------------------------
    # 3.  Stripe Webhook endpoint
    #     ‑ must be CSRF‑exempt because Stripe is an external service
    # ---------------------------------------------------------------------
    path(
        "api/stripe/webhook/",
        csrf_exempt(stripe_webhook),
        name="stripe-webhook",
    ),

    # ---------------------------------------------------------------------
    # 4.  Other API routes in the “proposals” app
    # ---------------------------------------------------------------------
    path("api/", include("proposals.urls")),

    # ---------------------------------------------------------------------
    # 5.  Catch‑all: anything **not** starting with /api/ should render
    #     the React SPA’s index.html.  Keep this *last*.
    # ---------------------------------------------------------------------
    re_path(
        r"^(?!api/).*$",
        TemplateView.as_view(template_name="index.html"),
        name="react-catchall",
    ),
]
