from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models


class User(AbstractUser):
    class TipoUsuario(models.TextChoices):
        ALUNO = "ALUNO", "Aluno"
        ORIENTADOR = "ORIENTADOR", "Orientador"
        ADMIN = "ADMIN", "Administrador"

    tipo = models.CharField(
        "Tipo de usuário",
        max_length=20,
        choices=TipoUsuario.choices,
        default=TipoUsuario.ALUNO,
    )
    nome_completo = models.CharField("Nome completo", max_length=150)
    email = models.EmailField("E-mail", unique=True)

    matricula = models.CharField(
        "Matrícula",
        max_length=20,
        blank=True,
        null=True,
        help_text="Obrigatória para alunos.",
    )
    area_atuacao = models.CharField(
        "Área de atuação",
        max_length=150,
        blank=True,
        null=True,
        help_text="Obrigatória para orientadores.",
    )

    def clean(self):
        super().clean()

        if self.tipo == self.TipoUsuario.ALUNO:
            if not self.matricula:
                raise ValidationError({"matricula": "Matrícula é obrigatória para alunos."})

        if self.tipo == self.TipoUsuario.ORIENTADOR:
            if not self.area_atuacao:
                raise ValidationError(
                    {"area_atuacao": "Área de atuação é obrigatória para orientadores."}
                )

    def __str__(self):
        return self.nome_completo or self.username

    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"
