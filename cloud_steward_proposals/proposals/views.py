# proposals/views.py
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet
from django.shortcuts import get_object_or_404
from .models import ClientPage
from .serializers import ClientPageSerializer

class ClientPageViewSet(ReadOnlyModelViewSet):
    queryset = ClientPage.objects.all()
    serializer_class = ClientPageSerializer
    lookup_field = 'slug'

    # Corrected retrieve method without @action
    def retrieve(self, request, slug=None, *args, **kwargs):
        client_page = get_object_or_404(ClientPage, slug=slug)
        serializer = self.get_serializer(client_page)
        return Response(serializer.data)
