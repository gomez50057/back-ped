from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .serializers import MyTokenObtainPairSerializer, UserSerializer
from rest_framework import generics, permissions

class LoginView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class RefreshTokenView(TokenRefreshView):
    pass

class CurrentUserView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
