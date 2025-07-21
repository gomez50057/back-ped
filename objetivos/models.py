from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class ObjetivoSet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='objetivo_set')
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Objetivos de {self.user.username}'

class Objetivo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='objetivos')
    clave = models.CharField(max_length=32, default="temp")  # Cambiado de id → clave
    nombre = models.CharField(max_length=512)
    set = models.ForeignKey(ObjetivoSet, related_name='objetivos', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'clave')

    def __str__(self):
        return f"{self.user.username} - {self.clave}"

class Estrategia(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='estrategias')
    clave = models.CharField(max_length=32, default="temp")  # Cambiado de id → clave
    nombre = models.CharField(max_length=512)
    objetivo = models.ForeignKey(Objetivo, related_name='estrategias', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'clave')

    def __str__(self):
        return f"{self.user.username} - {self.clave}"

class Linea(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lineas')
    clave = models.CharField(max_length=32, default="temp")  # Cambiado de id → clave
    text = models.TextField()
    estrategia = models.ForeignKey(Estrategia, related_name='lineas', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'clave')

    def __str__(self):
        return f"{self.user.username} - {self.clave}"


class FeedbackAvance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="feedback_avances")
    clave = models.CharField(
        max_length=120,
        help_text='Identificador de la sección, ej: EG01-propuesta-1_1_EG01'
    )
    acuerdo = models.CharField(
        max_length=10,
        choices=[('yes', 'Sí'), ('no', 'No')]
    )
    comoDecir = models.TextField()
    justificacion = models.TextField()
    envio_final = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'clave')  # Un feedback por usuario/sección
        verbose_name = "Feedback de Avance"
        verbose_name_plural = "Feedbacks de Avance"

    def __str__(self):
        return f"{self.user.username} - {self.clave}"