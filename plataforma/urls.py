# plataforma/urls.py

from rest_framework.routers import DefaultRouter
from .views import UserAxisSelectionViewSet

router = DefaultRouter()
router.register(r'user-axis-selection', UserAxisSelectionViewSet, basename='useraxisselection')

urlpatterns = router.urls
