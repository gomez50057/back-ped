# from rest_framework import generics, permissions
# from .models import NewIndicadorProposal
# from .serializers import NewIndicadorProposalSerializer

# # List & Create
# class NewIndicadorProposalListCreateView(generics.ListCreateAPIView):
#     queryset = NewIndicadorProposal.objects.all()
#     serializer_class = NewIndicadorProposalSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)

# # Retrieve, Update, Delete
# class NewIndicadorProposalDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = NewIndicadorProposal.objects.all()
#     serializer_class = NewIndicadorProposalSerializer
#     permission_classes = [permissions.IsAuthenticated]
#     lookup_field = 'indicador'

from rest_framework import generics, permissions
from .models import NewIndicadorProposal
from .serializers import NewIndicadorProposalSerializer

# Base Mixin para filtrar por usuario
class UserQuerySetMixin:
    def get_queryset(self):
        # Siempre devuelve sólo los objetos del usuario actual
        return NewIndicadorProposal.objects.filter(user=self.request.user)

# List & Create
class NewIndicadorProposalListCreateView(UserQuerySetMixin, generics.ListCreateAPIView):
    serializer_class = NewIndicadorProposalSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# Retrieve, Update, Delete
class NewIndicadorProposalDetailView(UserQuerySetMixin, generics.RetrieveUpdateDestroyAPIView):
    serializer_class = NewIndicadorProposalSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'indicador'


# views.py
from rest_framework import generics, permissions
from .models import NewIndicadorProposal
from .serializers import NewIndicadorProposalSerializerFull

class NewIndicadorProposalListAPIViewFull(generics.ListAPIView):
    queryset = NewIndicadorProposal.objects.all().order_by('-created_at')
    serializer_class = NewIndicadorProposalSerializerFull
