from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from .validators import validate_max_file_size, validate_file_extension


class TemaTCC(models.Model):
    class Status(models.TextChoices):
        PROPOSTO = "PROPOSTO", "Proposto"
        EM_ANDAMENTO = "EM_ANDAMENTO", "Em andamento"
        CONCLUIDO = "CONCLUIDO", "Concluído"
        CANCELADO = "CANCELADO", "Cancelado"

    titulo = models.CharField("Título", max_length=200)
    descricao = models.TextField("Descrição")

    aluno = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Aluno",
        related_name="temas_como_aluno",
    )
    orientador = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        verbose_name="Orientador",
        related_name="temas_como_orientador",
        blank=True,
        null=True,
    )

    status = models.CharField(
        "Status",
        max_length=20,
        choices=Status.choices,
        default=Status.PROPOSTO,
    )
    data_inicio = models.DateField("Data de início", blank=True, null=True)
    data_fim_prevista = models.DateField("Data fim prevista", blank=True, null=True)

    class Meta:
        verbose_name = "Tema de TCC"
        verbose_name_plural = "Temas de TCC"
        ordering = ["titulo"]
        unique_together = ("aluno", "titulo")

    def clean(self):
        super().clean()

        # Coerência de tipos
        from core.models import User  # import aqui para evitar import circular

        if self.aluno_id:
            aluno = getattr(self, "aluno", None)
            if isinstance(aluno, User) and aluno.tipo != User.TipoUsuario.ALUNO:
                raise ValidationError({"aluno": "O usuário selecionado não é um aluno."})

        if self.orientador_id:
            orientador = getattr(self, "orientador", None)
            if isinstance(orientador, User) and orientador.tipo != User.TipoUsuario.ORIENTADOR:
                raise ValidationError(
                    {"orientador": "O usuário selecionado não é um orientador."}
                )

        # Datas coerentes
        if self.data_inicio and self.data_fim_prevista:
            if self.data_fim_prevista < self.data_inicio:
                raise ValidationError(
                    {"data_fim_prevista": "A data fim prevista não pode ser anterior à data de início."}
                )

        # Regra de negócio de status
        if self.status != self.Status.PROPOSTO and not self.orientador:
            raise ValidationError(
                {"status": "Para avançar o status, escolha um orientador."}
            )

    def __str__(self):
        return self.titulo


class Entrega(models.Model):
    tema = models.ForeignKey(
        TemaTCC,
        on_delete=models.CASCADE,
        related_name="entregas",
        verbose_name="Tema",
    )
    titulo = models.CharField("Título", max_length=200)
    arquivo = models.FileField(
        "Arquivo", 
        upload_to="entregas/",
        validators=[validate_max_file_size, validate_file_extension],
    )
    data_entrega = models.DateField("Data da entrega", default=timezone.localdate)

    comentario_orientador = models.TextField(
        "Comentário do orientador",
        blank=True,
        null=True,
    )
    nota = models.DecimalField(
        "Nota",
        max_digits=4,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Valor entre 0 e 10.",
    )

    class Meta:
        verbose_name = "Entrega"
        verbose_name_plural = "Entregas"
        ordering = ["-data_entrega"]

    def clean(self):
        super().clean()

        if self.data_entrega and self.data_entrega > timezone.localdate():
            raise ValidationError(
                {"data_entrega": "A data de entrega não pode ser no futuro."}
            )

        if self.nota is not None:
            if self.nota < 0 or self.nota > 10:
                raise ValidationError({"nota": "A nota deve estar entre 0 e 10."})

    def __str__(self):
        return f"{self.titulo} - {self.tema.titulo}"
