from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied, ValidationError
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from django.contrib import messages

from core.models import User
from .forms import EntregaFeedbackForm, EntregaForm, TemaTCCForm
from .models import Entrega, TemaTCC


# TEMAS


class TemaListView(LoginRequiredMixin, ListView):
    model = TemaTCC
    template_name = "tcc/tema_list.html"
    context_object_name = "temas"

    def get_queryset(self):
        user = self.request.user
        if user.tipo == User.TipoUsuario.ALUNO:
            return TemaTCC.objects.filter(aluno=user)
        if user.tipo == User.TipoUsuario.ORIENTADOR:
            return TemaTCC.objects.filter(orientador=user)
        return TemaTCC.objects.all()  # ADMIN vê tudo


class TemaCreateView(LoginRequiredMixin, CreateView):
    model = TemaTCC
    form_class = TemaTCCForm
    template_name = "tcc/tema_form.html"
    success_url = reverse_lazy("tcc:tema_list")

    def dispatch(self, request, *args, **kwargs):
        if request.user.tipo != User.TipoUsuario.ALUNO:
            raise PermissionDenied("Somente alunos podem criar temas.")
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        tema = form.save(commit=False)
        tema.aluno = self.request.user
        # tema começa como PROPOSTO
        if not tema.status:
            tema.status = TemaTCC.Status.PROPOSTO
        try:
            tema.full_clean()
            tema.save()
            messages.success(self.request, "Tema criado com sucesso!")
        except ValidationError as e:
            messages.error(self.request, f"Erro ao criar tema: {e.message}")
            return self.form_invalid(form)
        return redirect(self.success_url)


class TemaUpdateView(LoginRequiredMixin, UpdateView):
    model = TemaTCC
    form_class = TemaTCCForm
    template_name = "tcc/tema_form.html"
    success_url = reverse_lazy("tcc:tema_list")
    context_object_name = "tema"

    def get_queryset(self):
        user = self.request.user
        if user.tipo == User.TipoUsuario.ALUNO:
            return TemaTCC.objects.filter(aluno=user)
        if user.tipo == User.TipoUsuario.ORIENTADOR:
            return TemaTCC.objects.filter(orientador=user)
        if user.tipo == User.TipoUsuario.ADMIN:
            return TemaTCC.objects.all()
        return TemaTCC.objects.none()

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        tema = form.save(commit=False)
        try:
            tema.full_clean()
            tema.save()
            messages.success(self.request, "Tema atualizado com sucesso!")
        except ValidationError as e:
            messages.error(self.request, f"Erro ao atualizar tema: {e.message}")
            return self.form_invalid(form)
        return redirect(self.success_url)


class TemaDeleteView(LoginRequiredMixin, DeleteView):
    model = TemaTCC
    template_name = "tcc/tema_confirm_delete.html"
    success_url = reverse_lazy("tcc:tema_list")

    def get_queryset(self):
        user = self.request.user
        if user.tipo == User.TipoUsuario.ALUNO:
            return TemaTCC.objects.filter(aluno=user)
        if user.tipo == User.TipoUsuario.ORIENTADOR:
            return TemaTCC.objects.filter(orientador=user)
        if user.tipo == User.TipoUsuario.ADMIN:
            return TemaTCC.objects.all()
        return TemaTCC.objects.none()


# ENTREGAS


@login_required
def entrega_list_view(request, tema_id):
    tema = get_object_or_404(TemaTCC, id=tema_id)
    entregas = tema.entregas.all().order_by("-data_entrega")
    return render(
        request,
        "tcc/entrega_list.html",
        {"tema": tema, "entregas": entregas},
    )


@login_required
def entrega_create_view(request, tema_id):
    tema = get_object_or_404(TemaTCC, id=tema_id)

    # Apenas aluno dono do tema (ou admin) pode criar entrega
    if request.user != tema.aluno and request.user.tipo != User.TipoUsuario.ADMIN:
        raise PermissionDenied("Você não pode enviar entrega para este tema.")

    if request.method == "POST":
        form = EntregaForm(
            request.POST,
            request.FILES,
            user=request.user,
            tema=tema,
        )
        if form.is_valid():
            entrega = form.save(commit=False)
            entrega.tema = tema
            try:
                entrega.full_clean()
                entrega.save()
                messages.success(request, "Entrega salva com sucesso!")
            except ValidationError as e:
                messages.error(request, f"Erro ao salvar entrega: {e.message}")
                return render(
                    request,
                    "tcc/entrega_form.html",
                    {"form": form, "tema": tema},
                )
            return redirect("tcc:entrega_list", tema_id=tema.id)
    else:
        form = EntregaForm(user=request.user, tema=tema)

    return render(
        request,
        "tcc/entrega_form.html",
        {"form": form, "tema": tema},
    )


@login_required
def entrega_feedback_view(request, entrega_id):
    entrega = get_object_or_404(Entrega, id=entrega_id)
    tema = entrega.tema

    # Apenas orientador do tema ou admin pode avaliar
    if not (
        request.user.tipo == User.TipoUsuario.ADMIN
        or (request.user.tipo == User.TipoUsuario.ORIENTADOR and tema.orientador == request.user)
    ):
        raise PermissionDenied("Você não pode avaliar esta entrega.")

    if request.method == "POST":
        form = EntregaFeedbackForm(request.POST, instance=entrega, user=request.user)
        if form.is_valid():
            try:
                entrega = form.save(commit=False)
                entrega.full_clean()
                entrega.save()
                messages.success(request, "Feedback salvo com sucesso!")
            except ValidationError as e:
                messages.error(request, f"Erro ao salvar feedback: {e.message}")
                return render(
                    request,
                    "tcc/entrega_feedback_form.html",
                    {"form": form, "entrega": entrega},
                )
            return redirect("tcc:entrega_list", tema_id=tema.id)
    else:
        form = EntregaFeedbackForm(instance=entrega, user=request.user)

    return render(
        request,
        "tcc/entrega_feedback_form.html",
        {"form": form, "entrega": entrega},
    )


# ORIENTADORES


class OrientadorListView(LoginRequiredMixin, ListView):
    model = User
    template_name = "tcc/orientador_list.html"
    context_object_name = "orientadores"

    def get_queryset(self):
        return User.objects.filter(tipo=User.TipoUsuario.ORIENTADOR, is_active=True)


@login_required
def orientador_detail_view(request, pk):
    orientador = get_object_or_404(User, pk=pk, tipo=User.TipoUsuario.ORIENTADOR)
    temas = TemaTCC.objects.filter(orientador=orientador)
    return render(
        request,
        "tcc/orientador_detail.html",
        {"orientador": orientador, "temas": temas},
    )
