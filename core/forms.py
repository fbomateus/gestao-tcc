from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class AlunoRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            "username",
            "nome_completo",
            "email",
            "matricula",
            "password1",
            "password2",
        ]

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not email:
            raise forms.ValidationError("E-mail é obrigatório.")
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Já existe um usuário com este e-mail.")
        return email

    def clean_matricula(self):
        matricula = self.cleaned_data.get("matricula")
        if not matricula:
            raise forms.ValidationError("Matrícula é obrigatória para alunos.")
        if User.objects.filter(matricula=matricula).exists():
            raise forms.ValidationError("Já existe um aluno com esta matrícula.")
        return matricula

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError("As senhas não conferem.")
        
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.tipo = User.TipoUsuario.ALUNO
        if commit:
            user.full_clean()  # Chamar full_clean antes de salvar
            user.save()
        return user
    

class UsuarioAdminForm(forms.ModelForm):
    password = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput,
        required=False,
        help_text="Obrigatório apenas na criação.",
    )
    password_confirm = forms.CharField(
        label="Confirmação de senha",
        widget=forms.PasswordInput,
        required=False,
    )

    class Meta:
        model = User
        fields = [
            "username",
            "nome_completo",
            "email",
            "tipo",
            "matricula",
            "area_atuacao",
            "is_active",
        ]

    def clean(self):
        cleaned_data = super().clean()
        tipo = cleaned_data.get("tipo")
        matricula = cleaned_data.get("matricula")
        area = cleaned_data.get("area_atuacao")

        # regras de obrigatoriedade
        if tipo == User.TipoUsuario.ALUNO and not matricula:
            self.add_error("matricula", "Matrícula é obrigatória para alunos.")
        if tipo == User.TipoUsuario.ORIENTADOR and not area:
            self.add_error("area_atuacao", "Área de atuação é obrigatória para orientadores.")

        # validação de senha na criação
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if not self.instance.pk:  # criação
            if not password:
                self.add_error("password", "Senha é obrigatória na criação.")
        if password or password_confirm:
            if password != password_confirm:
                self.add_error("password_confirm", "As senhas não conferem.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get("password")

        if password:
            user.set_password(password)

        if commit:
            user.full_clean()  # Chamar full_clean antes de salvar
            user.save()
        return user
