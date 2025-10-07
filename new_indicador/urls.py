# from django.urls import path
# from . import views

# urlpatterns = [
#     path('new-indicador/', views.NewIndicadorProposalListCreateView.as_view(), name='new-indicador-list-create'),
#     path('new-indicador/<int:pk>/', views.NewIndicadorProposalRetrieveUpdateDestroyView.as_view(), name='new-indicador-detail'),
# ]


from django.urls import path
from .views import (
    NewIndicadorProposalListCreateView,
    NewIndicadorProposalDetailView
)
from .views import NewIndicadorProposalListAPIViewFull

urlpatterns = [
    path('new-indicador/', NewIndicadorProposalListCreateView.as_view(), name='new-indicador-create'),
    path('new-indicador/<str:indicador>/', NewIndicadorProposalDetailView.as_view(), name='new-indicador-detail'),
    path('new-indicador-full/', NewIndicadorProposalListAPIViewFull.as_view(), name='new-indicador-proposal-list-full'),
]
