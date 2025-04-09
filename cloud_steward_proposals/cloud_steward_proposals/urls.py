from django.contrib import admin
from django.urls import path, re_path, include
from django.views.generic import View
from django.http import HttpResponse, Http404
from django.views.static import serve as static_serve
from django.conf import settings
import os
from proposals.views import create_checkout_session, get_checkout_session_details

# Path to your React build directory
REACT_BUILD_DIR = os.path.join(settings.BASE_DIR, 'frontend', 'build')

class ReactAppView(View):
    def get(self, request, path='', *args, **kwargs):
        file_path = os.path.join(REACT_BUILD_DIR, path)

        if os.path.exists(file_path) and os.path.isfile(file_path):
            return static_serve(request, path, document_root=REACT_BUILD_DIR)

        index_path = os.path.join(REACT_BUILD_DIR, 'index.html')
        if os.path.exists(index_path):
            with open(index_path, encoding='utf-8') as f:
                return HttpResponse(f.read(), content_type='text/html')

        raise Http404("index.html not found")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/create-checkout-session/', create_checkout_session, name='create-checkout-session'),
    path('api/order/success/', get_checkout_session_details, name='order-success'),
    path('api/', include('proposals.urls')),

    # Serve favicon.ico explicitly to avoid 404s or 500s
    path('favicon.ico', static_serve, {
        'document_root': REACT_BUILD_DIR,
        'path': 'favicon.ico'
    }),

    # Catch-all to serve the React app
    re_path(r'^(?P<path>.*)$', ReactAppView.as_view()),
]
