from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView

from proposals.views import create_checkout_session, get_checkout_session_details
from proposals.webhooks import stripe_webhook

urlpatterns = [
    # Django admin
    path('admin/', admin.site.urls),

    # Your API endpoints
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
    path('api/', include('proposals.urls')),

    # Stripe → Django webhook receiver
    # Must come before the React catch-all below
    path('stripe/webhook/', stripe_webhook, name='stripe-webhook'),

    # React front‑end catch‑all (do NOT match anything starting with "api/")
    re_path(
        r'^(?!api/).*$', 
        TemplateView.as_view(template_name='index.html')
    ),
]
