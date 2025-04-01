from django.urls import path
from .views import ClientPageViewSet

urlpatterns = [
    path('pages/<slug:slug>/', ClientPageViewSet.as_view({'get': 'retrieve'})),
    # (No admin or catch-all here)
]
