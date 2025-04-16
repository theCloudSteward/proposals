# cloud_steward_proposals/urls.py

from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView

from proposals.views import create_checkout_session, get_checkout_session_details
from proposals.webhooks import stripe_webhook

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # Checkout API
    path(
        'api/create-checkout-session/',
        create_checkout_session,
        name='create-checkout-session'
    ),
    path(
        'api/order/success/',
        get_checkout_session_details,
        name='order-success'
    ),

    # Stripe will POST your webhook events here
    path(
        'api/stripe/webhook/',
        stripe_webhook,
        name='stripe-webhook'
    ),

    # Any other “api/…” routes live in proposals/urls.py
    path('api/', include('proposals.urls')),

    # Finally: serve React for everything else
    re_path(
        r'^(?!api/).*$', 
        TemplateView.as_view(template_name='index.html'),
        name='react-catchall'
    ),
]