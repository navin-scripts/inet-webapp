from rest_framework.routers import DefaultRouter
from .views import UnifiSiteViewSet, KitViewSet

app_name = 'API'

router = DefaultRouter()
router.register(r'unifisites', UnifiSiteViewSet)
router.register(r'kits', KitViewSet)

urlpatterns = router.urls
