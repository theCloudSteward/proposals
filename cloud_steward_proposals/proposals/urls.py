# proposals/urls.py
from django.urls import path, re_path, include
from .views import ClientPageViewSet

urlpatterns = [
    path('pages/<slug:slug>/', ClientPageViewSet.as_view({'get': 'retrieve'})),
    re_path(r'^.*$', ClientPageViewSet.as_view({'get': 'retrieve'})),
]

