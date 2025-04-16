# cloud_steward_proposals/urls.py

from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt

from proposals.views import (
    create_checkout_session,
    get_checkout_session_details,
)
from proposals.webhooks import stripe_webhook


urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # 1) Checkout endpoints
    path(
        'api/create-checkout-session/',
        create_checkout_session,
        name='create-checkout-session',
    ),
    path(
        'api/order/success/',
        get_checkout_session_details,
        name='order-success',
    ),

    # 2) Stripe webhook endpoint (must be CSRF exempt)
    path(
        'api/stripe/webhook/',
        csrf_exempt(stripe_webhook),
        name='stripe-webhook',
    ),

    # 3) All other API routes in your proposals app
    path('api/', include('proposals.urls')),

    # 4) Catch‑all for React/front‑end routes
    re_path(
        r'^(?!api/).*$', 
        TemplateView.as_view(template_name='index.html'),
        name='react-catchall',
    ),
]
