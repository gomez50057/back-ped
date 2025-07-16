
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import UserIndicatorSelection
from .serializers import UserIndicatorSelectionSerializer

class UserIndicatorSelectionViewSet(viewsets.ModelViewSet):
    serializer_class = UserIndicatorSelectionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserIndicatorSelection.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        user = request.user
        existing = UserIndicatorSelection.objects.filter(user=user).first()
        if existing:
            serializer = self.get_serializer(existing)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return super().create(request, *args, **kwargs)
