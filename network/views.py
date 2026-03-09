from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import NetworkNode
from .serializers import (
    NetworkNodeSerializer,
    NetworkNodeCreateSerializer,
    NetworkNodeUpdateSerializer
)
from .permissions import IsActiveStaff


class NetworkNodeViewSet(viewsets.ModelViewSet):
    queryset = NetworkNode.objects.all()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = {
        'contact__country': ['exact'],  # фильтр по стране
    }
    permission_classes = [IsActiveStaff]

    def get_serializer_class(self):
        if self.action == 'create':
            return NetworkNodeCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return NetworkNodeUpdateSerializer
        return NetworkNodeSerializer