from django.urls import path
from .views import ClientPageViewSet, create_checkout_session

urlpatterns = [
    path('pages/<slug:slug>/', ClientPageViewSet.as_view({'get': 'retrieve'})),
]
