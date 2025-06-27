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

    # CORREÇÃO APLICADA AQUI: Usando __iexact para busca case-insensitive
    pending_resgates = Resgate.objects.filter(status__iexact="gerado").count()
    completed_resgates = Resgate.objects.filter(status__iexact="resgatado").count()

    active_clients = Cliente.objects.count()
    total_points_redeemed_agg = Resgate.objects.filter(
        status__iexact="resgatado"
    ).aggregate(Sum("pontos_totais_resgatados"))
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
    status_labels_list = [
        entry["status"].capitalize() for entry in resgates_por_status
    ]  # Deixa os labels mais bonitos
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
    """
    Exibe a lista de resgates, com funcionalidade de filtro e exportação de relatório PDF.
    A lógica foi refatorada para garantir que os filtros sejam aplicados antes da decisão de gerar PDF.
    """
    # Inicia a queryset base
    resgates_query = (
        Resgate.objects.all()
        .select_related("produto", "cliente", "posto_resgate")
        .order_by("-gerado_em")
    )
    filter_form = ResgateFilterForm(request.GET or None)

    # Aplica os filtros se o formulário for válido
    if filter_form.is_valid():
        if filter_form.cleaned_data.get("posto"):
            resgates_query = resgates_query.filter(
                posto_resgate=filter_form.cleaned_data["posto"]
            )
        if filter_form.cleaned_data.get("produto"):
            resgates_query = resgates_query.filter(
                produto=filter_form.cleaned_data["produto"]
            )
        if filter_form.cleaned_data.get("data_geracao_inicio"):
            resgates_query = resgates_query.filter(
                gerado_em__gte=filter_form.cleaned_data["data_geracao_inicio"]
            )
        if filter_form.cleaned_data.get("data_geracao_fim"):
            resgates_query = resgates_query.filter(
                gerado_em__lte=filter_form.cleaned_data["data_geracao_fim"]
            )
        if filter_form.cleaned_data.get("codigo_rastreamento"):
            resgates_query = resgates_query.filter(
                codigo_rastreamento__icontains=filter_form.cleaned_data[
                    "codigo_rastreamento"
                ]
            )

    # Verifica se a requisição é para gerar um PDF
    if "format" in request.GET and request.GET["format"] == "pdf":
        current_generation_time = timezone.now()
        report_id = str(uuid.uuid4())[:8].upper()

        # Prepara o contexto para o PDF usando a queryset JÁ FILTRADA
        context_pdf = {
            "resgates": resgates_query,
            "current_generation_time": current_generation_time,
            "report_id": report_id,
            "posto_nome": (
                filter_form.cleaned_data.get("posto").nome
                if filter_form.cleaned_data.get("posto")
                else "Todos"
            ),
            "produto_nome": (
                filter_form.cleaned_data.get("produto").nome
                if filter_form.cleaned_data.get("produto")
                else "Todos"
            ),
            "data_geracao_inicio_pdf": filter_form.cleaned_data.get(
                "data_geracao_inicio"
            ),
            "data_geracao_fim_pdf": filter_form.cleaned_data.get("data_geracao_fim"),
        }

        # Salva o registro do relatório gerado
        try:
            filtros_para_salvar = {
                k: v.strftime("%d/%m/%Y %H:%M") if isinstance(v, datetime) else str(v)
                for k, v in filter_form.cleaned_data.items()
                if v
            }
            RelatorioGerado.objects.create(
                report_id=report_id,
                tipo="GERAL",
                data_geracao=current_generation_time,
                filtros_aplicados=filtros_para_salvar,
            )
        except Exception as e:
            messages.error(request, f"Erro ao registrar o relatório PDF: {e}")

        # Renderiza o PDF
        html_string = render_to_string(
            "resgates/relatorio_resgates_pdf.html", context_pdf
        )
        html = HTML(string=html_string, base_url=request.build_absolute_uri())
        pdf_file = html.write_pdf()

        response = HttpResponse(pdf_file, content_type="application/pdf")
        response["Content-Disposition"] = (
            f'inline; filename="relatorio_geral_{report_id}.pdf"'
        )
        return response

    # Se não for para gerar PDF, renderiza a página HTML normal com os resgates filtrados
    context = {
        "resgates": resgates_query,
        "filter_form": filter_form,
        "title": "Lista de Resgates",
    }
    return render(request, "resgates/resgate_list.html", context)


@login_required
def resgate_upload_parse(request):
    """
    Processa um bloco de texto bruto, extrai múltiplos resgates e os importa
    para o banco de dados. Cria automaticamente produtos, clientes ou postos
    se não existirem.
    """
    if request.method == "POST":
        form = ResgateParseForm(request.POST)
        if form.is_valid():
            raw_data = form.cleaned_data["raw_data"]

            # --- Etapa de Limpeza dos Dados ---
            # Remove cabeçalhos, rodapés e linhas em branco indesejadas do texto copiado
            clean_data = re.sub(r"^\d+\/\d+\s*$", "", raw_data, flags=re.MULTILINE)
            clean_data = re.sub(
                r"^Produto \/ Cliente.*Situação\*?\s*$",
                "",
                clean_data,
                flags=re.MULTILINE,
            )
            clean_data = re.sub(
                r"^\*?Total resgatado.*pontos.*$", "", clean_data, flags=re.MULTILINE
            )
            clean_data = re.sub(
                r"\t+", " ", clean_data
            )  # Converte tabs múltiplos em espaço
            clean_data = re.sub(
                r"^\s*\n", "", clean_data, flags=re.MULTILINE
            ).strip()  # Remove linhas vazias

            # --- Etapa de Parse com Regex ---
            # Expressão regular para capturar cada bloco de resgate
            block_pattern = re.compile(
                r"(?P<produto_full>.+?)\s*\[(?P<pontos_prod>\d+)\s*pontos\]\s*\n"
                r"(?P<cliente_nome>.+?)\s+POSTO\s*(?P<posto_nome>.+?)\s*\n"
                r"(?P<tipo_resgate>.+?)\s+"
                r"(?P<data_geracao_data>\d{2}\/\d{2}\/\d{4})\s*\n"
                r"(?P<data_geracao_hora>\d{2}:\d{2})\s+"
                r"(?P<data_vencimento_data>\d{2}\/\d{2}\/\d{4})\s*\n"
                r"(?P<data_vencimento_hora>\d{2}:\d{2})\s+"
                r"(?P<quantidade>\d+)\s*"
                r"(?P<situacao>(?:Gerado|Resgatado|Vencido|Cancelado|Em Análise)?)\s*$",
                re.MULTILINE | re.DOTALL,
            )

            matches = list(block_pattern.finditer(clean_data))
            num_parsed = 0
            num_errors = 0

            if not matches:
                messages.error(
                    request,
                    "Nenhum resgate válido encontrado no texto. Verifique o formato dos dados copiados.",
                )
                return redirect("resgate_upload_parse")

            # --- Etapa de Processamento e Criação no Banco ---
            for match in matches:
                data = match.groupdict()
                try:
                    # Converte datas e números
                    gerado_em_str = (
                        f"{data['data_geracao_data']} {data['data_geracao_hora']}"
                    )
                    gerado_em_aware = timezone.make_aware(
                        datetime.strptime(gerado_em_str, "%d/%m/%Y %H:%M")
                    )
                    vencimento_str = (
                        f"{data['data_vencimento_data']} {data['data_vencimento_hora']}"
                    )
                    vencimento_aware = timezone.make_aware(
                        datetime.strptime(vencimento_str, "%d/%m/%Y %H:%M")
                    )
                    quantidade = int(data["quantidade"])
                    pontos_prod = int(data["pontos_prod"])

                    # Cria ou busca o Produto
                    produto, created = Produto.objects.get_or_create(
                        nome__iexact=data["produto_full"].strip(),
                        defaults={
                            "nome": data["produto_full"].strip(),
                            "pontos_necessarios": (
                                pontos_prod / quantidade if quantidade > 0 else 0
                            ),
                        },
                    )
                    if created:
                        messages.warning(
                            request,
                            f"Produto '{produto.nome}' criado automaticamente. Revise os detalhes!",
                        )

                    # Cria ou busca o Cliente
                    cliente, created = Cliente.objects.get_or_create(
                        nome_completo__iexact=data["cliente_nome"].strip(),
                        defaults={"nome_completo": data["cliente_nome"].strip()},
                    )
                    if created:
                        messages.warning(
                            request,
                            f"Cliente '{cliente.nome_completo}' criado automaticamente. Revise os detalhes!",
                        )

                    # Cria ou busca o Posto
                    posto, created = Posto.objects.get_or_create(
                        nome__iexact=data["posto_nome"].strip(),
                        defaults={"nome": data["posto_nome"].strip()},
                    )
                    if created:
                        messages.warning(
                            request,
                            f"Posto '{posto.nome}' criado automaticamente. Revise os detalhes!",
                        )

                    # Cria o objeto Resgate
                    Resgate.objects.create(
                        produto=produto,
                        cliente=cliente,
                        posto_resgate=posto,
                        tipo_resgate=data["tipo_resgate"].strip(),
                        gerado_em=gerado_em_aware,
                        vencimento=vencimento_aware,
                        quantidade=quantidade,
                        status=(
                            data["situacao"].strip().upper()
                            if data["situacao"]
                            else "GERADO"
                        ),
                    )
                    num_parsed += 1

                except Exception as e:
                    num_errors += 1
                    messages.error(
                        request,
                        f"Erro ao processar um item: {e}. Detalhes: {match.group(0)[:100]}...",
                    )

            if num_parsed > 0:
                messages.success(
                    request, f"{num_parsed} resgates importados com sucesso!"
                )
            if num_errors > 0:
                messages.error(
                    request,
                    f"Falha ao importar {num_errors} resgates. Verifique os erros detalhados.",
                )

            return redirect("resgate_list")
    else:
        form = ResgateParseForm()

    context = {"title": "Importar Resgates", "form": form}
    return render(request, "resgates/resgate_upload_parse.html", context)


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
def resgate_delete_selected(request):
    """
    Exclui múltiplos resgates com base nos IDs selecionados enviados via POST.
    """
    if request.method == "POST":
        # Pega a lista de IDs dos checkboxes marcados
        resgate_ids = request.POST.getlist("resgate_ids")

        if not resgate_ids:
            messages.warning(request, "Nenhum resgate foi selecionado para exclusão.")
            return redirect("resgate_list")

        try:
            # Filtra os resgates pelos IDs e os deleta
            resgates_to_delete = Resgate.objects.filter(id__in=resgate_ids)
            count = resgates_to_delete.count()
            resgates_to_delete.delete()

            messages.success(
                request,
                f"{count} resgate(s) selecionado(s) foram excluídos com sucesso!",
            )
        except Exception as e:
            messages.error(
                request, f"Ocorreu um erro ao tentar excluir os resgates: {e}"
            )

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
    """
    Processa a validação de um resgate em duas etapas:
    1. Busca (GET): Procura por um código e exibe os detalhes para conferência.
    2. Confirmação (POST): Efetivamente valida o resgate e altera seu status.
    """
    resgate_encontrado = None
    codigo_buscado = request.GET.get("codigo_rastreamento", "").strip()

    # --- ETAPA 1: BUSCA (Quando a página é carregada ou um código é buscado) ---
    if codigo_buscado:
        try:
            resgate_encontrado = Resgate.objects.get(
                codigo_rastreamento__iexact=codigo_buscado
            )
            messages.info(
                request,
                "Resgate encontrado. Por favor, confira os dados e confirme a entrega.",
            )
        except Resgate.DoesNotExist:
            messages.error(
                request,
                f"Código de rastreamento '{codigo_buscado}' não encontrado no sistema.",
            )
            resgate_encontrado = None  # Garante que nada seja exibido se não encontrado

    # --- ETAPA 2: CONFIRMAÇÃO (Quando o formulário de validação é enviado) ---
    if request.method == "POST":
        resgate_id = request.POST.get("resgate_id")
        resgate = get_object_or_404(Resgate, id=resgate_id)

        # Pega os nomes do formulário de confirmação
        nome_recebedor = request.POST.get("nome_recebedor", "").strip()
        nome_motorista = request.POST.get("nome_motorista", "").strip()

        # Valida o status antes de alterar
        if resgate.status == "GERADO":
            resgate.status = "RESGATADO"
            resgate.nome_recebedor = nome_recebedor if nome_recebedor else None
            resgate.nome_motorista = nome_motorista if nome_motorista else None
            resgate.save()
            messages.success(
                request, f"Resgate de '{resgate.produto.nome}' validado com sucesso!"
            )
        else:
            messages.warning(
                request,
                f"Este resgate já possui o status '{resgate.get_status_display()}' e não pode ser alterado aqui.",
            )

        # Redireciona para a mesma página, que agora mostrará a mensagem de sucesso
        return redirect(
            f"{request.path}?codigo_rastreamento={resgate.codigo_rastreamento}"
        )

    context = {
        "title": "Validar Resgate por Código",
        "resgate_encontrado": resgate_encontrado,
        "codigo_buscado": codigo_buscado,
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


@login_required
def regenerate_report_pdf(request, pk):
    """
    Busca um relatório já gerado pelo seu ID e recria o PDF
    com base nos filtros que foram salvos.
    """
    report = get_object_or_404(RelatorioGerado, pk=pk)
    filters = report.filtros_aplicados

    # Recria a queryset de resgates com base nos filtros salvos
    resgates = Resgate.objects.all().order_by("-gerado_em")

    if filters.get("posto") and filters["posto"] != "Todos":
        resgates = resgates.filter(posto_resgate__nome=filters["posto"])
    if filters.get("produto") and filters["produto"] != "Todos":
        resgates = resgates.filter(produto__nome=filters["produto"])
    if (
        filters.get("data_geracao_inicio")
        and filters["data_geracao_inicio"] != "Qualquer"
    ):
        try:
            start_date = datetime.strptime(
                filters["data_geracao_inicio"], "%d/%m/%Y %H:%M"
            )
            resgates = resgates.filter(gerado_em__gte=timezone.make_aware(start_date))
        except (ValueError, TypeError):
            pass
    if filters.get("data_geracao_fim") and filters["data_geracao_fim"] != "Qualquer":
        try:
            end_date = datetime.strptime(filters["data_geracao_fim"], "%d/%m/%Y %H:%M")
            resgates = resgates.filter(gerado_em__lte=timezone.make_aware(end_date))
        except (ValueError, TypeError):
            pass

    # Lida com o caso de ser um manifesto de lote
    is_manifesto_lote = report.tipo == "MANIFESTO_LOTE"
    if is_manifesto_lote and report.codigo_rastreamento_lote:
        resgates = Resgate.objects.filter(
            codigo_rastreamento=report.codigo_rastreamento_lote
        ).order_by("id")

    # Prepara o contexto para renderizar o template do PDF
    context_pdf = {
        "resgates": resgates,
        "current_generation_time": report.data_geracao,
        "report_id": report.report_id,
        "is_manifesto_lote": is_manifesto_lote,
        # ... (adicione outras variáveis de contexto que seu template de PDF precisa)
    }

    html_string = render_to_string("resgates/relatorio_resgates_pdf.html", context_pdf)
    html = HTML(string=html_string, base_url=request.build_absolute_uri())
    pdf_file = html.write_pdf()

    response = HttpResponse(pdf_file, content_type="application/pdf")
    response["Content-Disposition"] = (
        f'inline; filename="relatorio_{report.report_id}.pdf"'
    )
    return response


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
