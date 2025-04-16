# cloud_steward_proposals/urls.py

from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt

from proposals.views import create_checkout_session, get_checkout_session_details
from proposals.webhooks import stripe_webhook

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # Checkout endpoints
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

    # Stripe webhook (must be csrf_exempt so Stripe can POST without a CSRF token)
    path(
        'api/stripe/webhook/',
        csrf_exempt(stripe_webhook),
        name='stripe-webhook'
    ),

    # All other API endpoints in your proposals app
    path('api/', include('proposals.urls')),

    # Finally, anything else gets served by your React app
    re_path(
        r'^(?!api/).*$', 
        TemplateView.as_view(template_name='index.html'),
        name='react-catchall'
    ),
]
