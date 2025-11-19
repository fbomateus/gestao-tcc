from django.core.exceptions import PermissionDenied, ValidationError
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q

from tcc.models import TemaTCC, Entrega
from .forms import AlunoRegisterForm, UsuarioAdminForm
from .models import User


def register_view(request):
    """Tela de cadastro (apenas alunos)."""
    if request.method == "POST":
        form = AlunoRegisterForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Cadastro realizado com sucesso! Faça login.")
                return redirect("core:login")
            except ValidationError as e:
                messages.error(request, f"Erro ao registrar: {e.message}")
    else:
        form = AlunoRegisterForm()

    return render(request, "core/register.html", {"form": form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect("core:dashboard")

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("core:dashboard")
        else:
            messages.error(request, "Usuário ou senha inválidos.")
    else:
        form = AuthenticationForm()

    return render(request, "core/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("core:login")


@login_required
def dashboard_view(request):
    user = request.user
    contexto = {}

    if user.tipo == User.TipoUsuario.ALUNO:
        temas = TemaTCC.objects.filter(aluno=user)
        entregas = Entrega.objects.filter(tema__aluno=user).order_by("-data_entrega")[:5]

        contexto.update(
            {
                "temas": temas,
                "ultimas_entregas": entregas,
                "tipo_dashboard": "aluno",
            }
        )

    elif user.tipo == User.TipoUsuario.ORIENTADOR:
        temas = TemaTCC.objects.filter(orientador=user)
        entregas_pendentes = Entrega.objects.filter(
            tema__orientador=user,
        ).order_by("-data_entrega")[:5]

        contexto.update(
            {
                "temas": temas,
                "entregas_pendentes": entregas_pendentes,
                "tipo_dashboard": "orientador",
            }
        )

    else:  # ADMIN
        contexto.update(
            {
                "total_usuarios": User.objects.count(),
                "total_temas": TemaTCC.objects.count(),
                "total_entregas": Entrega.objects.count(),
                "tipo_dashboard": "admin",
            }
        )

    return render(request, "core/dashboard.html", contexto)

@login_required
def usuario_list_view(request):
    if request.user.tipo != User.TipoUsuario.ADMIN:
        raise PermissionDenied()

    usuarios = User.objects.exclude(tipo=User.TipoUsuario.ADMIN).order_by("nome_completo")
    return render(request, "core/usuario_list.html", {"usuarios": usuarios})


@login_required
def usuario_create_view(request):
    if request.user.tipo != User.TipoUsuario.ADMIN:
        raise PermissionDenied()

    if request.method == "POST":
        form = UsuarioAdminForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Usuário criado com sucesso.")
                return redirect("core:usuario_list")
            except ValidationError as e:
                messages.error(request, f"Erro ao criar usuário: {e.message}")
    else:
        form = UsuarioAdminForm()

    return render(request, "core/usuario_form.html", {"form": form, "titulo": "Novo usuário"})


@login_required
def usuario_update_view(request, pk):
    if request.user.tipo != User.TipoUsuario.ADMIN:
        raise PermissionDenied()

    usuario = get_object_or_404(User, pk=pk)
    if usuario.tipo == User.TipoUsuario.ADMIN:
        raise PermissionDenied()

    if request.method == "POST":
        form = UsuarioAdminForm(request.POST, instance=usuario)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Usuário atualizado com sucesso.")
                return redirect("core:usuario_list")
            except ValidationError as e:
                messages.error(request, f"Erro ao atualizar usuário: {e.message}")
    else:
        form = UsuarioAdminForm(instance=usuario)

    return render(request, "core/usuario_form.html", {"form": form, "titulo": "Editar usuário"})

@login_required
def usuario_detail_view(request, pk):
    usuario = get_object_or_404(User, pk=pk)

    # admin pode ver todo mundo; o próprio usuário pode ver ele mesmo
    if not (request.user.tipo == User.TipoUsuario.ADMIN or request.user.pk == usuario.pk):
        raise PermissionDenied()

    temas = TemaTCC.objects.filter(
        Q(aluno=usuario) | Q(orientador=usuario)
    ).select_related("aluno", "orientador")

    return render(
        request,
        "core/usuario_detail.html",
        {"usuario": usuario, "temas": temas},
    )
