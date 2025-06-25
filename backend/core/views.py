# backend/core/views.py
import os
from datetime import datetime
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
import re, uuid, csv, os, tempfile
from django.http import HttpResponse
from weasyprint import HTML, CSS
from django.template.loader import render_to_string
from django.conf import settings
from django.db.models import Q, Sum, Count


# Importações dos seus modelos, incluindo RelatorioGerado
from .models import Produto, Cliente, Posto, Resgate, RelatorioGerado

# Importações dos seus formulários
from .forms import (
    CustomUserCreationForm,
    ProdutoForm,
    ClienteForm,
    ResgateParseForm,
    ResgateFilterForm,
)


def homepage(request):
    return render(request, "homepage.html")


@login_required
def dashboard_view(request):
    """
    Exibe o dashboard principal com informações resumidas e estatísticas.
    """
    total_products = Produto.objects.count()
    pending_resgates = Resgate.objects.filter(status="GERADO").count()
    active_clients = Cliente.objects.count()
    completed_resgates = Resgate.objects.filter(status="RESGATADO").count()
    total_points_redeemed_agg = Resgate.objects.filter(status="RESGATADO").aggregate(
        Sum("pontos_totais_resgatados")
    )
    total_points_redeemed = (
        total_points_redeemed_agg["pontos_totais_resgatados__sum"] or 0
    )
    total_postos = Posto.objects.count()

    top_products = (
        Resgate.objects.values("produto__nome")
        .annotate(total_quantidade=Sum("quantidade"))
        .order_by("-total_quantidade")[:5]
    )

    top_clients = (
        Resgate.objects.values("cliente__nome_completo")
        .annotate(total_resgates=Count("id"))
        .order_by("-total_resgates")[:5]
    )

    resgates_por_status = Resgate.objects.values("status").annotate(count=Count("id"))
    status_labels_list = [entry["status"] for entry in resgates_por_status]
    status_counts_list = [entry["count"] for entry in resgates_por_status]

    resgates_por_posto = (
        Resgate.objects.values("posto_resgate__nome")
        .annotate(count=Count("id"))
        .order_by("-count")[:5]
    )
    posto_labels_list = [entry["posto_resgate__nome"] for entry in resgates_por_posto]
    posto_counts_list = [entry["count"] for entry in resgates_por_posto]

    context = {
        "title": "Dashboard",
        "total_products": total_products,
        "pending_resgates": pending_resgates,
        "active_clients": active_clients,
        "completed_resgates": completed_resgates,
        "total_points_redeemed": total_points_redeemed,
        "total_postos": total_postos,
        "top_products": top_products,
        "top_clients": top_clients,
        "status_labels": json.dumps(status_labels_list),
        "status_counts": json.dumps(status_counts_list),
        "posto_labels": json.dumps(posto_labels_list),
        "posto_counts": json.dumps(posto_counts_list),
    }
    return render(request, "dashboard.html", context)


@login_required
def product_list(request):
    products = Produto.objects.all().order_by("nome")
    context = {"products": products}
    return render(request, "products/product_list.html", context)


def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(
                request, f"Conta criada para {username}! Agora você pode fazer login."
            )
            return redirect("login")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Erro no campo '{field}': {error}")
    else:
        form = CustomUserCreationForm()

    context = {"form": form}
    return render(request, "registration/register.html", context)


@login_required
def product_create(request):
    if request.method == "POST":
        form = ProdutoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("products_list")
        else:
            messages.error(request, "Erro ao criar produto. Verifique os dados.")
    else:
        form = ProdutoForm()

    context = {"form": form, "title": "Adicionar Novo Produto"}
    return render(request, "products/product_form.html", context)


@login_required
def product_update(request, pk):
    product = get_object_or_404(Produto, pk=pk)
    if request.method == "POST":
        form = ProdutoForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect("products_list")
        else:
            messages.error(request, "Erro ao atualizar produto. Verifique os dados.")
    else:
        form = ProdutoForm(instance=product)

    context = {"form": form, "title": "Editar Produto"}
    return render(request, "products/product_form.html", context)


@login_required
def product_delete(request, pk):
    product = get_object_or_404(Produto, pk=pk)
    if request.method == "POST":
        product.delete()
        messages.success(request, f'Produto "{product.nome}" excluído com sucesso!')
        return redirect("products_list")
    context = {"product": product, "title": "Confirmar Exclusão de Produto"}
    return render(request, "products/product_confirm_delete.html", context)


@login_required
def client_list(request):
    clients = Cliente.objects.all().order_by("nome_completo")
    context = {"clients": clients}
    return render(request, "clients/client_list.html", context)


@login_required
def client_create(request):
    if request.method == "POST":
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Cliente adicionado com sucesso!")
            return redirect("client_list")
        else:
            messages.error(request, "Erro ao criar cliente. Verifique os dados.")
    else:
        form = ClienteForm()

    context = {"form": form, "title": "Adicionar Novo Cliente"}
    return render(request, "clients/client_form.html", context)


@login_required
def client_update(request, pk):
    client = get_object_or_404(Cliente, pk=pk)
    if request.method == "POST":
        form = ClienteForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            messages.success(
                request, f'Cliente "{client.nome_completo}" atualizado com sucesso!'
            )
            return redirect("client_list")
        else:
            messages.error(request, "Erro ao atualizar cliente. Verifique os dados.")
    else:
        form = ClienteForm(instance=client)

    context = {"form": form, "title": "Editar Cliente"}
    return render(request, "clients/client_form.html", context)


@login_required
def client_delete(request, pk):
    client = get_object_or_404(Cliente, pk=pk)
    if request.method == "POST":
        client.delete()
        messages.success(
            request, f'Cliente "{client.nome_completo}" excluído com sucesso!'
        )
        return redirect("client_list")
    context = {"client": client, "title": "Confirmar Exclusão de Cliente"}
    return render(request, "clients/client_confirm_delete.html", context)


@login_required
def resgate_list(request):
    resgates = Resgate.objects.all().order_by("-gerado_em")
    filter_form = ResgateFilterForm(request.GET)
    if filter_form.is_valid():
        if filter_form.cleaned_data.get("posto"):
            resgates = resgates.filter(posto_resgate=filter_form.cleaned_data["posto"])
        if filter_form.cleaned_data.get("produto"):
            resgates = resgates.filter(produto=filter_form.cleaned_data["produto"])
        if filter_form.cleaned_data.get("data_geracao_inicio"):
            resgates = resgates.filter(
                gerado_em__gte=filter_form.cleaned_data["data_geracao_inicio"]
            )
        if filter_form.cleaned_data.get("data_geracao_fim"):
            resgates = resgates.filter(
                gerado_em__lte=filter_form.cleaned_data["data_geracao_fim"]
            )
        if filter_form.cleaned_data.get("codigo_rastreamento"):
            resgates = resgates.filter(
                codigo_rastreamento__icontains=filter_form.cleaned_data[
                    "codigo_rastreamento"
                ]
            )

    context = {
        "resgates": resgates,
        "filter_form": filter_form,
        "title": "Lista de Resgates",
    }
    return render(request, "resgates/resgate_list.html", context)


@login_required
def resgate_upload_parse(request):
    if request.method == "POST":
        form = ResgateParseForm(request.POST)
        if form.is_valid():
            raw_data = form.cleaned_data["raw_data"]
            # ... (Lógica de parse) ...
            return redirect("resgate_list")
    else:
        form = ResgateParseForm()
    return render(request, "resgates/resgate_upload_parse.html", {"form": form})


@login_required
def resgate_delete(request, pk):
    resgate = get_object_or_404(Resgate, pk=pk)
    if request.method == "POST":
        resgate.delete()
        messages.success(
            request,
            f"Resgate de {resgate.produto.nome} para {resgate.cliente.nome_completo} excluído com sucesso!",
        )
        return redirect("resgate_list")
    return redirect("resgate_list")


@login_required
def resgate_delete_all(request):
    if request.method == "POST":
        Resgate.objects.all().delete()
        messages.success(request, "Todos os resgates foram excluídos com sucesso!")
        return redirect("resgate_list")
    return redirect("resgate_list")


@login_required
def resgate_export_csv(request):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = (
        f'attachment; filename="resgates_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv"'
    )
    writer = csv.writer(response)
    writer.writerow(
        ["ID Resgate", "Produto", "Cliente", "Posto de Resgate", "Gerado Em", "Status"]
    )
    resgates = Resgate.objects.all().select_related(
        "produto", "cliente", "posto_resgate"
    )
    for resgate in resgates:
        writer.writerow(
            [
                resgate.id,
                resgate.produto.nome,
                resgate.cliente.nome_completo,
                resgate.posto_resgate.nome,
                resgate.gerado_em.strftime("%d/%m/%Y %H:%M"),
                resgate.get_status_display(),
            ]
        )
    return response


@login_required
def resgate_detail(request, pk):
    resgate = get_object_or_404(Resgate, pk=pk)
    context = {"resgate": resgate, "title": "Detalhes do Resgate"}
    return render(request, "resgates/resgate_detail.html", context)


@login_required
def resgate_validate_tracking(request):
    resgate = None
    if request.method == "POST":
        codigo_rastreamento = request.POST.get("codigo_rastreamento", "").strip()
        # ... (Lógica de validação) ...
    context = {
        "title": "Validar Resgate por Código",
        "resgate_encontrado": resgate,
    }
    return render(request, "resgates/resgate_validate_tracking.html", context)


@login_required
def report_list(request):
    reports = RelatorioGerado.objects.all().order_by("-data_geracao")
    context = {"title": "Relatórios Gerados", "reports": reports}
    return render(request, "reports/report_list.html", context)


@login_required
def report_delete_selected(request):
    if request.method == "POST":
        report_ids = request.POST.getlist("report_ids")
        if report_ids:
            RelatorioGerado.objects.filter(id__in=report_ids).delete()
            messages.success(
                request, f"{len(report_ids)} relatório(s) excluído(s) com sucesso!"
            )
    return redirect("report_list")


@login_required
def report_delete_all(request):
    if request.method == "POST":
        count, _ = RelatorioGerado.objects.all().delete()
        messages.success(
            request, f"Todos os {count} relatório(s) foram excluído(s) com sucesso!"
        )
    return redirect("report_list")


@login_required
def report_delete_single(request, pk):
    if request.method == "POST":
        report = get_object_or_404(RelatorioGerado, pk=pk)
        report.delete()
        messages.success(
            request, f"Relatório '{report.report_id}' excluído com sucesso!"
        )
    return redirect("report_list")


# --- NOVA VIEW ---
@login_required
def update_resgate_status(request, pk):
    """
    View para atualizar o status de um resgate específico.
    """
    if request.method == "POST":
        resgate = get_object_or_404(Resgate, pk=pk)
        novo_status = request.POST.get("status")
        status_validos = ["gerado", "resgatado", "vencido", "cancelado"]

        if novo_status in status_validos:
            resgate.status = novo_status
            resgate.save()
            messages.success(
                request,
                f"Status do resgate atualizado para '{resgate.get_status_display()}' com sucesso!",
            )
        else:
            messages.error(request, "Ocorreu um erro: status inválido.")

        return redirect("resgate_detail", pk=resgate.pk)

    return redirect("resgate_list")
