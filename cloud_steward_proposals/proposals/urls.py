from django.urls import path

urlpatterns = [
    path('pages/<slug:slug>/', ClientPageViewSet.as_view({'get': 'retrieve'})),
]
