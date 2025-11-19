from django.contrib import admin
from .models import TemaTCC, Entrega


@admin.register(TemaTCC)
class TemaTCCAdmin(admin.ModelAdmin):
    list_display = ("titulo", "aluno", "orientador", "status", "data_inicio")
    list_filter = ("status", "data_inicio")
    search_fields = ("titulo", "aluno__nome_completo", "orientador__nome_completo")
    readonly_fields = ("criado_em",) if hasattr(TemaTCC, "criado_em") else ()


@admin.register(Entrega)
class EntregaAdmin(admin.ModelAdmin):
    list_display = ("titulo", "tema", "data_entrega", "nota")
    list_filter = ("data_entrega", "nota")
    search_fields = ("titulo", "tema__titulo")
    readonly_fields = ("data_entrega",) if not Entrega._meta.get_field("data_entrega").blank else ()
