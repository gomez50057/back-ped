from django.db import models
from django.contrib.auth import get_user_model

from django.core.validators import RegexValidator

ALFANUMERIC_PATTERN = r'^[\w\-]+$'  # permite letras, números, guion bajo y guion

class NewIndicadorProposal(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    indicator_name = models.CharField(max_length=255)
    ped_alignment = models.CharField(max_length=255, blank=True)
    national_plan_alignment = models.CharField(max_length=255)
    ods_alignment = models.JSONField(default=list)
    description = models.TextField(blank=True)
    periodicity = models.CharField(max_length=100, blank=True)
    trend = models.CharField(max_length=100, blank=True)
    baseline = models.CharField(max_length=255, blank=True)
    goal_2028 = models.CharField(max_length=255, blank=True)
    goal_2040 = models.CharField(max_length=255, blank=True)
    sources = models.JSONField(default=list)
    indicador = models.CharField(
        max_length=100,
        blank=True,
        validators=[RegexValidator(ALFANUMERIC_PATTERN, 'Solo letras, números, guion y guion bajo')]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.indicator_name

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'indicador'], name='unique_indicador_per_user')
        ]

