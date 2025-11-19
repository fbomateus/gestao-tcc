from django import forms
from django.forms import DateInput

from core.models import User
from .models import TemaTCC, Entrega
from .validators import validate_max_file_size, validate_file_extension


class DatePickerInput(DateInput):
    input_type = "date"  # HTML5 datepicker do próprio browser


class TemaTCCForm(forms.ModelForm):
    class Meta:
        model = TemaTCC
        fields = [
            "titulo",
            "descricao",
            "orientador",
            "status",
            "data_inicio",
            "data_fim_prevista",
        ]
        widgets = {
            "data_inicio": DatePickerInput(),
            "data_fim_prevista": DatePickerInput(),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        # Orientadores ativos
        self.fields["orientador"].queryset = User.objects.filter(
            tipo=User.TipoUsuario.ORIENTADOR,
            is_active=True,
        ).order_by("nome_completo")

        # Se for aluno, restringe as opções de status
        if self.user and self.user.tipo == User.TipoUsuario.ALUNO:
            allowed_status = [
                TemaTCC.Status.PROPOSTO,
                TemaTCC.Status.EM_ANDAMENTO,
            ]
            self.fields["status"].choices = [
                (value, label)
                for value, label in self.fields["status"].choices
                if value in allowed_status
            ]

    def clean(self):
        cleaned_data = super().clean()
        # regras adicionais já estão no model.clean()
        return cleaned_data


class EntregaForm(forms.ModelForm):
    class Meta:
        model = Entrega
        fields = ["titulo", "arquivo", "data_entrega"]
        widgets = {
            "data_entrega": DatePickerInput(),
        }

    def __init__(self, *args, **kwargs):
        # se quiser usar o user aqui no futuro:
        self.user = kwargs.pop("user", None)
        self.tema = kwargs.pop("tema", None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()

        # regra: só o aluno dono do tema pode criar entrega (validação extra de segurança)
        if self.user and self.tema:
            if self.user != self.tema.aluno and self.user.tipo != User.TipoUsuario.ADMIN:
                raise forms.ValidationError(
                    "Você não tem permissão para enviar entregas para este tema."
                )

        return cleaned_data


class EntregaFeedbackForm(forms.ModelForm):
    class Meta:
        model = Entrega
        fields = ["comentario_orientador", "nota"]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()

        # Regra principal: ALUNO NÃO DÁ NOTA
        if self.user:
            if self.user.tipo == User.TipoUsuario.ALUNO:
                raise forms.ValidationError(
                    "Alunos não podem lançar nota ou feedback de orientador."
                )

        return cleaned_data
