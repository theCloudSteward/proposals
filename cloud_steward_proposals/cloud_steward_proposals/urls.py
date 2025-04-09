from django.contrib import admin
from django.urls import path, re_path, include
from django.views.generic import TemplateView
from django.views.static import serve
from proposals.views import create_checkout_session, get_checkout_session_details
import os
from django.conf import settings

# Path to your React build directory
REACT_BUILD_DIR = os.path.join(settings.BASE_DIR, 'frontend', 'build')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/create-checkout-session/', create_checkout_session, name='create-checkout-session'),
    path('api/order/success/', get_checkout_session_details, name='order-success'),
    path('api/', include('proposals.urls')),
    
    # Explicitly serve favicon.ico from your React build folder.
    path('favicon.ico', serve, {'document_root': REACT_BUILD_DIR, 'path': 'favicon.ico'}),

    # Fallback: serve index.html for all other non-API routes.
    re_path(r'^(?!api/|c/success).*$', TemplateView.as_view(template_name='index.html')),
]
