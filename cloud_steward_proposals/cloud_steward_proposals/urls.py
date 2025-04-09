from django.contrib import admin
from django.urls import path, re_path, include
from django.views.generic import TemplateView
from proposals.views import create_checkout_session, get_checkout_session_details

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/create-checkout-session/', create_checkout_session, name='create-checkout-session'),
    path('api/order/success/', get_checkout_session_details, name='order-success'),
    path('api/', include('proposals.urls')),

    # Catch-all for frontend routing, but EXCLUDE /api/ and /admin/
    re_path(r'^(?!api/|admin/).*$', TemplateView.as_view(template_name='index.html')),
]
