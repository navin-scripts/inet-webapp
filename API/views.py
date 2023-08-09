from rest_framework import viewsets
from NOC.models import UnifiSite, Kit
from .serializers import UnifiSiteSerializer, KitSerializer
from rest_framework.permissions import IsAuthenticated



class UnifiSiteViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = UnifiSite.objects.all()
    serializer_class = UnifiSiteSerializer

class KitViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Kit.objects.all()
    serializer_class = KitSerializer