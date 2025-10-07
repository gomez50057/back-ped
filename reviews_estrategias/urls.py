"""
reviews_estrategias/urls.py
Define las rutas de la API para las revisiones de campo.
"""
from rest_framework import routers
from .views import CampoReviewViewSet

router = routers.DefaultRouter()
router.register(r'campo-reviews', CampoReviewViewSet, basename='campo-review')

urlpatterns = router.urls
