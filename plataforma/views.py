# plataforma/views.py
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import UserAxisSelection
from .serializers import UserAxisSelectionSerializer

class UserAxisSelectionViewSet(viewsets.ModelViewSet):
    serializer_class = UserAxisSelectionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserAxisSelection.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        user = request.user
        existing = UserAxisSelection.objects.filter(user=user).first()
        if existing:
            serializer = self.get_serializer(existing)
            # Puedes cambiar a status=status.HTTP_409_CONFLICT si prefieres
            return Response(serializer.data, status=status.HTTP_200_OK)
        return super().create(request, *args, **kwargs)
    