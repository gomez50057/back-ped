from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import IndicadoresFeedback
from .serializers import IndicadoresFeedbackSerializer

class IndicadoresFeedbackUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # Devuelve el feedback del usuario autenticado (único)
        try:
            feedback = IndicadoresFeedback.objects.get(user=request.user)
            serializer = IndicadoresFeedbackSerializer(feedback)
            return Response(serializer.data)
        except IndicadoresFeedback.DoesNotExist:
            return Response({"detail": "No hay feedback registrado para este usuario."}, status=404)

    def post(self, request):
        # Solo permite crear si no existe para el usuario
        if IndicadoresFeedback.objects.filter(user=request.user).exists():
            return Response({"detail": "Ya existe feedback para este usuario."}, status=400)
        serializer = IndicadoresFeedbackSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def put(self, request):
        # Permite actualizar el feedback ÚNICO del usuario
        try:
            feedback = IndicadoresFeedback.objects.get(user=request.user)
        except IndicadoresFeedback.DoesNotExist:
            return Response({"detail": "No hay feedback registrado para este usuario."}, status=404)

        serializer = IndicadoresFeedbackSerializer(feedback, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(user=request.user)  # Asegura el user correcto
            return Response(serializer.data)
        return Response(serializer.errors, status=400)


# views.py
from rest_framework import generics, permissions
from .models import IndicadoresFeedback
from .serializers import IndicadoresFeedbackSerializerFull

class IndicadoresFeedbackListAPIViewFull(generics.ListAPIView):
    queryset = IndicadoresFeedback.objects.all().order_by('-created_at')
    serializer_class = IndicadoresFeedbackSerializerFull
