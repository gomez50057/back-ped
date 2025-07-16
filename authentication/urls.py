from django.urls import path
from .views import LoginView, RefreshTokenView, CurrentUserView

urlpatterns = [
    path('login/',       LoginView.as_view(),    name='token_obtain_pair'),
    path('refresh/',     RefreshTokenView.as_view(), name='token_refresh'),
    path('current_user/', CurrentUserView.as_view(), name='current_user'),
]
