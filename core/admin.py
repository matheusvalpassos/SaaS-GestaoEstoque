from django.contrib import admin
from .models import Posto, Produto, Cliente, Resgate


@admin.register(Posto)
class PostoAdmin(admin.ModelAdmin):
    list_display = (
        "nome",
        "endereco",
    )
    search_fields = (
        "nome",
        "endereco",
    )


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = (
        "nome",
        "pontos_necessarios",
        "ativo",
    )
    list_filter = ("ativo",)
    search_fields = ("nome",)


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = (
        "nome_completo",
        "cpf",
        "telefone",
    )
    search_fields = (
        "nome_completo",
        "cpf",
    )


@admin.register(Resgate)
class ResgateAdmin(admin.ModelAdmin):
    list_display = (
        "produto",
        "cliente",
        "posto_resgate",
        "gerado_em",
        "vencimento",
        "quantidade",
        "status",
        "pontos_totais_resgatados",
        "codigo_rastreamento",
        "nome_recebedor",
    )
    list_filter = (
        "status",
        "posto_resgate",
        "gerado_em",
        "vencimento",
    )
    search_fields = (
        "produto__nome",
        "cliente__nome_completo",
        "posto_resgate__nome",
        "codigo_rastreamento",
        "nome_recebedor",
    )
    # Campos que podem ser editados diretamente na lista
    list_editable = ("status",)
    # Campos que não serão exibidos no formulário de edição (calculados/gerados automaticamente)
    readonly_fields = ("gerado_em", "pontos_totais_resgatados", "codigo_rastreamento")
