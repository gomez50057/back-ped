from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .serializers import MyTokenObtainPairSerializer, CurrentUserSerializer
from rest_framework import generics, permissions

class LoginView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class RefreshTokenView(TokenRefreshView):
    pass

class CurrentUserView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CurrentUserSerializer

    def get_object(self):
        return self.request.user
