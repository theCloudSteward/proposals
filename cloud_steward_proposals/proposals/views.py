# proposals/views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.utils import timezone
from .models import ClientPage
from .serializers import ClientPageSerializer

class ClientPageViewSet(viewsets.ViewSet):
    def retrieve(self, request, slug=None):
        try:
            page = ClientPage.objects.get(slug=slug)
        except ClientPage.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # If expired, treat it as a 404
        if page.expires_at < timezone.now():
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = ClientPageSerializer(page)
        return Response(serializer.data)
