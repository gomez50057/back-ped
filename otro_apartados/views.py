# otro_apartados/views.py

from rest_framework import viewsets, permissions
from .models import Elemento
from .serializers import ElementoSerializer

class ElementoViewSet(viewsets.ModelViewSet):
    serializer_class = ElementoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Solo mostrar los elementos del usuario autenticado
        # return Elemento.objects.filter(user=self.request.user).order_by('-fecha_modificacion')
        return Elemento.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# otro_apartados/views.py
from rest_framework import generics, permissions
from .models import Elemento
from .serializers import ElementoSerializerFull

class ElementoListAPIViewFull(generics.ListAPIView):
    queryset = Elemento.objects.all().order_by('-fecha_creacion')
    serializer_class = ElementoSerializerFull
