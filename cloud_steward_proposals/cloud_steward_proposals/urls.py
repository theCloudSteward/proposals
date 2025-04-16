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

    # Stripe webhook (no CSRF token)
    path(
        'api/stripe/webhook/',
        csrf_exempt(stripe_webhook),
        name='stripe-webhook'
    ),

    # Any other API endpoints
    path('api/', include('proposals.urls')),

    # Serve favicon & manifest directly (so they’re not routed to index.html)
    path('favicon.ico',  TemplateView.as_view(template_name='favicon.ico')),
    path('manifest.json', TemplateView.as_view(template_name='manifest.json')),

    # Front‑end “success” page
    re_path(
        r'^success/?$',
        TemplateView.as_view(template_name='index.html'),
        name='react-success'
    ),

    # Everything else (except API, static, media, favicon, manifest) → React
    re_path(
        r'^(?!api/|static/|media/|favicon\.ico|manifest\.json).*$',
        TemplateView.as_view(template_name='index.html'),
        name='react-catchall'
    ),
]

# In DEBUG mode, serve static & media via Django
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
