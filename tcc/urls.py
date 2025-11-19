from django.urls import path
from . import views

app_name = "tcc"

urlpatterns = [
    # Temas
    path("temas/", views.TemaListView.as_view(), name="tema_list"),
    path("temas/novo/", views.TemaCreateView.as_view(), name="tema_create"),
    path("temas/<int:pk>/editar/", views.TemaUpdateView.as_view(), name="tema_update"),
    path("temas/<int:pk>/excluir/", views.TemaDeleteView.as_view(), name="tema_delete"),

    # Entregas
    path("temas/<int:tema_id>/entregas/", views.entrega_list_view, name="entrega_list"),
    path("temas/<int:tema_id>/entregas/nova/", views.entrega_create_view, name="entrega_create"),
    path("entregas/<int:entrega_id>/feedback/", views.entrega_feedback_view, name="entrega_feedback"),

    # Orientadores
    path("orientadores/", views.OrientadorListView.as_view(), name="orientador_list"),
    path("orientadores/<int:pk>/", views.orientador_detail_view, name="orientador_detail"),
]
