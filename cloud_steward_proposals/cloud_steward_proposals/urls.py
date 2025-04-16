# cloud_steward_proposals/urls.py

from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt

from django.conf import settings
from django.conf.urls.static import static

from proposals.views import create_checkout_session, get_checkout_session_details
from proposals.webhooks import stripe_webhook

urlpatterns = [
    # Django admin
    path('admin/', admin.site.urls),

    # Your checkout endpoints
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

    # Stripe webhook endpoint (must be CSRF‑exempt and under /api/)
    path(
        'api/stripe/webhook/',
        csrf_exempt(stripe_webhook),
        name='stripe-webhook'
    ),

    # All other API routes in proposals/urls.py
    path('api/', include('proposals.urls')),

    # Finally: catch‑all for React front end,
    # but don’t intercept static or media files
    re_path(
        r'^(?!api/|static/|media/).*$',
        TemplateView.as_view(template_name='index.html'),
        name='react-catchall'
    ),
]

# Serve static and media files during development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,  document_root=settings.MEDIA_ROOT)
