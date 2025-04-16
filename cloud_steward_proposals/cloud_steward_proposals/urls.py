# cloud_steward_proposals/urls.py

import os
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.decorators.csrf import csrf_exempt
from django.views.static import serve as static_serve
from django.conf import settings
from django.conf.urls.static import static

from proposals.views import create_checkout_session, get_checkout_session_details
from proposals.webhooks import stripe_webhook

# Adjust this to point at your React `build/` directory
REACT_BUILD_DIR = os.path.join(settings.BASE_DIR, 'frontend', 'build')

urlpatterns = [
    # Django admin
    path('admin/', admin.site.urls),

    # Stripe checkout API
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

    # All other API routes
    path('api/', include('proposals.urls')),

    # Serve React static assets (JS/CSS/images)
    re_path(
        r'^static/(?P<path>.*)$',
        static_serve,
        {'document_root': os.path.join(REACT_BUILD_DIR, 'static')}
    ),

    # Serve favicon & manifest from your build/
    path(
        'favicon.ico',
        static_serve,
        {'document_root': REACT_BUILD_DIR, 'path': 'favicon.ico'}
    ),
    path(
        'manifest.json',
        static_serve,
        {'document_root': REACT_BUILD_DIR, 'path': 'manifest.json'}
    ),

    # “Success” landing page for React to pick up (matches /success?session_id=…)
    re_path(
        r'^success/?$',
        static_serve,
        {'document_root': REACT_BUILD_DIR, 'path': 'index.html'},
        name='react-success'
    ),

    # Everything else (except api/, static/, media/, favicon.ico, manifest.json)
    # should return index.html so React Router can handle it
    re_path(
        r'^(?!api/|static/|media/|favicon\.ico|manifest\.json).*$',
        static_serve,
        {'document_root': REACT_BUILD_DIR, 'path': 'index.html'},
        name='react-catchall'
    ),
]

# During development, still have Django serve your own STATIC/MEDIA
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,  document_root=settings.MEDIA_ROOT)
