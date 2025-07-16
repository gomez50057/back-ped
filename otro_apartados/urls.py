# otro_apartados/urls.py

from rest_framework.routers import DefaultRouter
from .views import ElementoViewSet

router = DefaultRouter()
router.register('elementos', ElementoViewSet, basename='elemento')

urlpatterns = router.urls
