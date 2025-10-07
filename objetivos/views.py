from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import ObjetivoSet, Objetivo, Estrategia, Linea
from .serializers import ObjetivoSetSerializer, ObjetivoSerializer
from rest_framework import serializers

class ObjetivoSetView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        obj_set = getattr(request.user, 'objetivo_set', None)
        if obj_set:
            serializer = ObjetivoSetSerializer(obj_set)
            return Response(serializer.data)
        return Response({'detail': 'No hay objetivos para este usuario'}, status=404)

    def post(self, request):
        if hasattr(request.user, 'objetivo_set'):
            return Response({'detail': 'Ya tienes un conjunto de objetivos, usa PUT para actualizar.'}, status=400)

        obj_set = ObjetivoSet.objects.create(user=request.user)
        objetivos_data = request.data.get("objetivos", [])

        for obj_data in objetivos_data:
            obj = Objetivo.objects.create(
                clave=obj_data["clave"],
                nombre=obj_data["nombre"],
                set=obj_set,
                user=request.user
            )
            for est_data in obj_data.get("estrategias", []):
                est = Estrategia.objects.create(
                    clave=est_data["clave"],
                    nombre=est_data["nombre"],
                    objetivo=obj,
                    user=request.user
                )
                for lin_data in est_data.get("lineas", []):
                    Linea.objects.create(
                        clave=lin_data["clave"],
                        text=lin_data["text"],
                        estrategia=est,
                        user=request.user
                    )
        return Response({'detail': 'Cargado correctamente.'}, status=status.HTTP_201_CREATED)

    def put(self, request):
        obj_set = getattr(request.user, 'objetivo_set', None)
        if not obj_set:
            return Response({'detail': 'No tienes objetivos aún, usa POST.'}, status=404)

        obj_set.objetivos.all().delete()

        objetivos_data = request.data.get("objetivos", [])

        for obj_data in objetivos_data:
            obj = Objetivo.objects.create(
                clave=obj_data["clave"],
                nombre=obj_data["nombre"],
                set=obj_set,
                user=request.user
            )
            for est_data in obj_data.get("estrategias", []):
                est = Estrategia.objects.create(
                    clave=est_data["clave"],
                    nombre=est_data["nombre"],
                    objetivo=obj,
                    user=request.user
                )
                for lin_data in est_data.get("lineas", []):
                    Linea.objects.create(
                        clave=lin_data["clave"],
                        text=lin_data["text"],
                        estrategia=est,
                        user=request.user
                    )
        return Response({'detail': 'Actualizado correctamente.'}, status=status.HTTP_200_OK)

class ObjetivoDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, objetivo_clave):
        obj_set = getattr(request.user, 'objetivo_set', None)
        if not obj_set:
            return Response({'detail': 'No tienes objetivos.'}, status=404)
        try:
            objetivo = obj_set.objetivos.get(clave=objetivo_clave, user=request.user)
        except Objetivo.DoesNotExist:
            return Response({'detail': 'No existe ese objetivo.'}, status=404)
        serializer = ObjetivoSerializer(objetivo)
        return Response(serializer.data)

    def patch(self, request, objetivo_clave):
        obj_set = getattr(request.user, 'objetivo_set', None)
        if not obj_set:
            return Response({'detail': 'No tienes objetivos.'}, status=404)
        try:
            objetivo = obj_set.objetivos.get(clave=objetivo_clave, user=request.user)
        except Objetivo.DoesNotExist:
            return Response({'detail': 'No existe ese objetivo.'}, status=404)
        nombre = request.data.get('nombre')
        if nombre:
            objetivo.nombre = nombre
            objetivo.save()
            serializer = ObjetivoSerializer(objetivo)
            return Response(serializer.data)
        return Response({'detail': 'No se proporcionó un nombre.'}, status=400)

    def delete(self, request, objetivo_clave):
        obj_set = getattr(request.user, 'objetivo_set', None)
        if not obj_set:
            return Response({'detail': 'No tienes objetivos.'}, status=404)
        try:
            objetivo = obj_set.objetivos.get(clave=objetivo_clave, user=request.user)
        except Objetivo.DoesNotExist:
            return Response({'detail': 'No existe ese objetivo.'}, status=404)
        objetivo.delete()
        return Response({'detail': 'Objetivo eliminado.'}, status=204)

class LineaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Linea
        fields = ('id', 'text')

class EstrategiaSerializer(serializers.ModelSerializer):
    lineas = LineaSerializer(many=True, read_only=True)

    class Meta:
        model = Estrategia
        fields = ('id', 'nombre', 'lineas')

class ObjetivoSerializer(serializers.ModelSerializer):
    estrategias = EstrategiaSerializer(many=True, read_only=True)

    class Meta:
        model = Objetivo
        fields = ('id', 'nombre', 'estrategias')



from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import FeedbackAvance
from .serializers import FeedbackAvanceSerializer

class UserFeedbackAvanceView(generics.ListCreateAPIView):
    serializer_class = FeedbackAvanceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return FeedbackAvance.objects.filter(user=self.request.user).order_by('clave')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        data = request.data
        if isinstance(data, dict):
            data = [data]
        results = []
        errors = []
        for entry in data:
            entry['user'] = self.request.user.id
            serializer = self.get_serializer(data=entry)
            if serializer.is_valid():
                obj, created = FeedbackAvance.objects.update_or_create(
                    user=self.request.user,
                    clave=entry['clave'],
                    defaults={
                        'acuerdo': entry['acuerdo'],
                        'comoDecir': entry['comoDecir'],
                        'justificacion': entry['justificacion'],
                        'envio_final': entry.get('envio_final', False),
                    }
                )
                results.append(self.get_serializer(obj).data)
            else:
                errors.append(serializer.errors)
        if errors:
            return Response({'errors': errors, 'results': results}, status=status.HTTP_400_BAD_REQUEST)
        return Response(results, status=status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        data = request.data
        if isinstance(data, dict):
            data = [data]
        results = []
        errors = []
        for entry in data:
            try:
                obj = FeedbackAvance.objects.get(user=self.request.user, clave=entry['clave'])
                serializer = self.get_serializer(obj, data=entry, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    results.append(serializer.data)
                else:
                    errors.append(serializer.errors)
            except FeedbackAvance.DoesNotExist:
                errors.append({'clave': entry.get('clave'), 'error': 'No existe el feedback para este usuario/clave'})
        if errors:
            return Response({'errors': errors, 'results': results}, status=status.HTTP_400_BAD_REQUEST)
        return Response(results, status=status.HTTP_200_OK)


# # objetivos/views.py
# from django.contrib.auth import get_user_model
# from rest_framework import viewsets, permissions
# from .models import ObjetivoSet, FeedbackAvance
# from .serializers import ObjetivoSetSerializer, FeedbackAvanceSerializer

# User = get_user_model()

# class IsRevisionUser(permissions.BasePermission):
#     """
#     Solo permiten acceso a usuarios en el grupo 'revision'.
#     """
#     def has_permission(self, request, view):
#         return (
#             request.user.is_authenticated and
#             request.user.groups.filter(name='revision').exists()
#         )

# class ObjetivoSetViewSet(viewsets.ReadOnlyModelViewSet):
#     """
#     - Usuarios normales: solo ven su propio ObjetivoSet.
#     - Usuarios 'revision': ven todos los ObjetivoSet.
#     """
#     queryset = ObjetivoSet.objects.all()
#     serializer_class = ObjetivoSetSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         qs = super().get_queryset()
#         if not self.request.user.groups.filter(name='revision').exists():
#             qs = qs.filter(user=self.request.user)
#         return qs

# class FeedbackAvanceViewSet(viewsets.ReadOnlyModelViewSet):
#     """
#     - Usuarios normales: solo ven su propio FeedbackAvance.
#     - Usuarios 'revision': ven todo el FeedbackAvance.
#     """
#     queryset = FeedbackAvance.objects.all()
#     serializer_class = FeedbackAvanceSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         qs = super().get_queryset()
#         if not self.request.user.groups.filter(name='revision').exists():
#             qs = qs.filter(user=self.request.user)
#         return qs


#
#

from rest_framework.generics import ListAPIView
from .models import ObjetivoSet, Objetivo, Estrategia, Linea
from .serializers import (
    ObjetivoSetSerializerFull,
    ObjetivoSerializerFull,
    EstrategiaSerializerFull,
    LineaSerializerFull
)
from rest_framework.permissions import AllowAny

class AllObjetivoSetView(ListAPIView):
    queryset = ObjetivoSet.objects.all()
    serializer_class = ObjetivoSetSerializerFull
    permission_classes = [AllowAny]

class AllObjetivoView(ListAPIView):
    queryset = Objetivo.objects.all()
    serializer_class = ObjetivoSerializerFull
    permission_classes = [AllowAny]

class AllEstrategiaView(ListAPIView):
    queryset = Estrategia.objects.all()
    serializer_class = EstrategiaSerializerFull
    permission_classes = [AllowAny]

class AllLineaView(ListAPIView):
    queryset = Linea.objects.all()
    serializer_class = LineaSerializerFull
    permission_classes = [AllowAny]
    
#
#
#
from rest_framework.generics import ListAPIView
from .models import FeedbackAvance
from .serializers import FeedbackAvanceSerializerFull
from rest_framework.permissions import AllowAny

class AllFeedbackAvanceView(ListAPIView):
    queryset = FeedbackAvance.objects.all()
    serializer_class = FeedbackAvanceSerializerFull
    permission_classes = [AllowAny]