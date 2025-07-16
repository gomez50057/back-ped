from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import ObjetivoSet, Objetivo, Estrategia, Linea
from .serializers import ObjetivoSetSerializer, ObjetivoSerializer

class ObjetivoSetView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Devuelve el set del usuario autenticado (o vacío)
        obj_set = getattr(request.user, 'objetivo_set', None)
        if obj_set:
            serializer = ObjetivoSetSerializer(obj_set)
            return Response(serializer.data)
        return Response({'detail': 'No hay objetivos para este usuario'}, status=404)

    def post(self, request):
        # Si el usuario ya tiene un set, devuelve error
        if hasattr(request.user, 'objetivo_set'):
            return Response({'detail': 'Ya tienes un conjunto de objetivos, usa PUT para actualizar.'}, status=400)
        
        # Crea el set y todos los objetivos/estrategias/líneas enviados
        obj_set = ObjetivoSet.objects.create(user=request.user)
        objetivos_data = request.data.get("objetivos", [])

        for obj_data in objetivos_data:
            obj = Objetivo.objects.create(
                id=obj_data["id"],
                nombre=obj_data["nombre"],
                set=obj_set
            )
            for est_data in obj_data.get("estrategias", []):
                est = Estrategia.objects.create(
                    id=est_data["id"],
                    nombre=est_data["nombre"],
                    objetivo=obj
                )
                for lin_data in est_data.get("lineas", []):
                    Linea.objects.create(
                        id=lin_data["id"],
                        text=lin_data["text"],
                        estrategia=est
                    )
        return Response({'detail': 'Cargado correctamente.'}, status=status.HTTP_201_CREATED)

    def put(self, request):
        # Solo actualiza el set del usuario autenticado
        obj_set = getattr(request.user, 'objetivo_set', None)
        if not obj_set:
            return Response({'detail': 'No tienes objetivos aún, usa POST.'}, status=404)
        
        # Limpia todos los objetivos, estrategias y líneas previas del set
        obj_set.objetivos.all().delete()

        # Vuelve a cargar los datos enviados
        objetivos_data = request.data.get("objetivos", [])

        for obj_data in objetivos_data:
            obj = Objetivo.objects.create(
                id=obj_data["id"],
                nombre=obj_data["nombre"],
                set=obj_set
            )
            for est_data in obj_data.get("estrategias", []):
                est = Estrategia.objects.create(
                    id=est_data["id"],
                    nombre=est_data["nombre"],
                    objetivo=obj
                )
                for lin_data in est_data.get("lineas", []):
                    Linea.objects.create(
                        id=lin_data["id"],
                        text=lin_data["text"],
                        estrategia=est
                    )
        return Response({'detail': 'Actualizado correctamente.'}, status=status.HTTP_200_OK)


class ObjetivoDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, objetivo_id):
        obj_set = getattr(request.user, 'objetivo_set', None)
        if not obj_set:
            return Response({'detail': 'No tienes objetivos.'}, status=404)
        try:
            objetivo = obj_set.objetivos.get(id=objetivo_id)
        except Objetivo.DoesNotExist:
            return Response({'detail': 'No existe ese objetivo.'}, status=404)
        serializer = ObjetivoSerializer(objetivo)
        return Response(serializer.data)

    def patch(self, request, objetivo_id):
        obj_set = getattr(request.user, 'objetivo_set', None)
        if not obj_set:
            return Response({'detail': 'No tienes objetivos.'}, status=404)
        try:
            objetivo = obj_set.objetivos.get(id=objetivo_id)
        except Objetivo.DoesNotExist:
            return Response({'detail': 'No existe ese objetivo.'}, status=404)
        nombre = request.data.get('nombre')
        if nombre:
            objetivo.nombre = nombre
            objetivo.save()
            serializer = ObjetivoSerializer(objetivo)
            return Response(serializer.data)
        return Response({'detail': 'No se proporcionó un nombre.'}, status=400)

    def delete(self, request, objetivo_id):
        obj_set = getattr(request.user, 'objetivo_set', None)
        if not obj_set:
            return Response({'detail': 'No tienes objetivos.'}, status=404)
        try:
            objetivo = obj_set.objetivos.get(id=objetivo_id)
        except Objetivo.DoesNotExist:
            return Response({'detail': 'No existe ese objetivo.'}, status=404)
        objetivo.delete()
        return Response({'detail': 'Objetivo eliminado.'}, status=204)


from rest_framework import serializers
from .models import Objetivo, Estrategia, Linea

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
