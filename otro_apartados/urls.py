# otro_apartados/urls.py

from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import ElementoViewSet, ElementoListAPIViewFull

router = DefaultRouter()
router.register(r'elementos', ElementoViewSet, basename='elemento')

urlpatterns = [
    # /api/otro_apartados/elementos/       → ElementoViewSet (CRUD completo)
    # /api/otro_apartados/elementos-full/  → ElementoListAPIViewFull (solo lectura)
    path('', include(router.urls)),
    path('elementos-full/', ElementoListAPIViewFull.as_view(), name='elementos-list-full'),
]
