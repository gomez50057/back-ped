from rest_framework.routers import DefaultRouter
from .views import UserIndicatorSelectionViewSet

router = DefaultRouter()
router.register(r'user-indicator-selection', UserIndicatorSelectionViewSet, basename='userindicatorselection')

urlpatterns = router.urls
