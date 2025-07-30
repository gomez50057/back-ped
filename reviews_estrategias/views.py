from rest_framework import viewsets, permissions
from .models import CampoReview
from .serializers import CampoReviewSerializer

class CampoReviewViewSet(viewsets.ModelViewSet):
    """
    ViewSet para CRUD de revisiones de campo.
    """
    queryset = CampoReview.objects.all()
    serializer_class = CampoReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Asigna el usuario autenticado como revisor
        serializer.save(reviewer=self.request.user)


# Para registrar en rutas (ejemplo en reviews_estrategias/urls.py)
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'campo-reviews', CampoReviewViewSet, basename='campo-review')

urlpatterns = router.urls