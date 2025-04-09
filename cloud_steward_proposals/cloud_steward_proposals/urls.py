from django.contrib import admin
from django.urls import path, re_path, include
from django.views.generic import TemplateView
from django.views.static import serve
from django.conf import settings
import os
from proposals.views import create_checkout_session, get_checkout_session_details

# Path to your React build directory (adjust if different)
REACT_BUILD_DIR = os.path.join(settings.BASE_DIR, 'frontend', 'build')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/create-checkout-session/', create_checkout_session, name='create-checkout-session'),
    path('api/order/success/', get_checkout_session_details, name='order-success'),
    path('api/', include('proposals.urls')),
    # Serve static files from the React build directory
    re_path(r'^(?P<path>(favicon\.ico|android-chrome-.*\.png|apple-touch-icon\.png|manifest\.json|robots\.txt))$', serve, {
        'document_root': REACT_BUILD_DIR,
    }),
    # Catch-all route for React app (SPA)
    re_path(r'^(?!api/|c/success).*$', TemplateView.as_view(template_name='index.html')),
]