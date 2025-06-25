# backend/core/views.py
import os
from datetime import datetime
import json  # NOVO: Importar a biblioteca json
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
    # Estatísticas existentes
    total_products = Produto.objects.count()
    pending_resgates = Resgate.objects.filter(status="GERADO").count()
    active_clients = Cliente.objects.count()

    # NOVAS ESTATÍSTICAS DO DASHBOARD
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

    # DADOS PARA GRÁFICOS
    # 1. Resgates por Status (Gráfico de Rosca/Pizza)
    resgates_por_status = Resgate.objects.values("status").annotate(count=Count("id"))
    status_labels_list = [entry["status"] for entry in resgates_por_status]
    status_counts_list = [entry["count"] for entry in resgates_por_status]

    # 2. Resgates por Posto (Gráfico de Barras) - Top 5 Postos
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
        # Dados para os gráficos - AGORA SERIALIZADOS PARA JSON
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
    Também registra o relatório gerado no banco de dados.
    """
    resgates = Resgate.objects.all().order_by("-gerado_em")

    filter_form = ResgateFilterForm(request.GET)

    # Variáveis para o contexto do PDF, inicializadas com defaults
    pdf_posto_nome = "Todos"
    pdf_produto_nome = "Todos"
    pdf_data_geracao_inicio = "Qualquer"
    pdf_data_geracao_fim = "Qualquer"
    pdf_codigo_rastreamento = "Todos"
    is_manifesto_lote = False
    cliente_nome = "Não Informado"
    cliente_cpf = "Não Informado"
    total_pontos_lote = 0

    # Lógica para aplicar filtros na queryset `resgates`
    if filter_form.is_valid():
        posto = filter_form.cleaned_data.get("posto")
        produto = filter_form.cleaned_data.get("produto")
        data_geracao_inicio = filter_form.cleaned_data.get("data_geracao_inicio")
        data_geracao_fim = filter_form.cleaned_data.get("data_geracao_fim")
        codigo_rastreamento_filter = filter_form.cleaned_data.get("codigo_rastreamento")

        if posto:
            resgates = resgates.filter(posto_resgate=posto)
            pdf_posto_nome = posto.nome
        if produto:
            resgates = resgates.filter(produto=produto)
            pdf_produto_nome = produto.nome

        if data_geracao_inicio:
            resgates = resgates.filter(gerado_em__gte=data_geracao_inicio)
            pdf_data_geracao_inicio = data_geracao_inicio
        if data_geracao_fim:
            resgates = resgates.filter(gerado_em__lte=data_geracao_fim)
            pdf_data_geracao_fim = data_geracao_fim

        # Lógica para MANIFESTO DE LOTE
        if (
            "format" in request.GET
            and request.GET["format"] == "pdf"
            and codigo_rastreamento_filter
        ):
            resgates_do_lote = Resgate.objects.filter(
                codigo_rastreamento=codigo_rastreamento_filter
            ).order_by("id")

            if resgates_do_lote.exists():
                is_manifesto_lote = True
                resgates = resgates_do_lote
                pdf_codigo_rastreamento = codigo_rastreamento_filter

                primeiro_resgate = resgates_do_lote.first()
                if primeiro_resgate.posto_resgate:
                    pdf_posto_nome = primeiro_resgate.posto_resgate.nome
                if primeiro_resgate.cliente:
                    cliente_nome = primeiro_resgate.cliente.nome_completo
                    cliente_cpf = (
                        primeiro_resgate.cliente.cpf
                        if primeiro_resgate.cliente.cpf
                        else "Não Informado"
                    )

                total_pontos_lote = (
                    resgates_do_lote.aggregate(Sum("pontos_totais_resgatados"))[
                        "pontos_totais_resgatados__sum"
                    ]
                    or 0
                )
            else:
                messages.warning(
                    request,
                    f"Nenhum resgate encontrado para o código de rastreamento: '{codigo_rastreamento_filter}'. Gerando relatório geral com outros filtros.",
                )
                is_manifesto_lote = False
                resgates = Resgate.objects.all().order_by("-gerado_em")
                if posto:
                    resgates = resgates.filter(posto_resgate=posto)
                if produto:
                    resgates = resgates.filter(produto=produto)
                if data_geracao_inicio:
                    resgates = resgates.filter(gerado_em__gte=data_geracao_inicio)
                if data_geracao_fim:
                    resgates = resgates.filter(gerado_em__lte=data_geracao_fim)
        elif "format" in request.GET and request.GET["format"] == "pdf":
            pdf_codigo_rastreamento = "Todos"

    # Se a requisição for para gerar PDF
    if "format" in request.GET and request.GET["format"] == "pdf":
        current_generation_time = timezone.now()
        report_id = str(uuid.uuid4())[:8].upper()  # Gera um UUID curto para o relatório

        # Preparar os filtros aplicados para salvar no JSONField
        filtros_para_salvar = {
            "posto": pdf_posto_nome,
            "produto": pdf_produto_nome,
            "data_geracao_inicio": (
                pdf_data_geracao_inicio.strftime("%d/%m/%Y %H:%M")
                if isinstance(pdf_data_geracao_inicio, datetime)
                else pdf_data_geracao_inicio
            ),
            "data_geracao_fim": (
                pdf_data_geracao_fim.strftime("%d/%m/%Y %H:%M")
                if isinstance(pdf_data_geracao_fim, datetime)
                else pdf_data_geracao_fim
            ),
            "codigo_rastreamento_filtro": (
                pdf_codigo_rastreamento if is_manifesto_lote else None
            ),  # Só salva se foi o filtro principal
        }

        # Determine o tipo de relatório a ser salvo
        report_type = "MANIFESTO_LOTE" if is_manifesto_lote else "GERAL"

        # Salvar o registro do relatório gerado no banco de dados
        try:
            RelatorioGerado.objects.create(
                report_id=report_id,
                tipo=report_type,
                data_geracao=current_generation_time,
                filtros_aplicados=filtros_para_salvar,
                codigo_rastreamento_lote=(
                    pdf_codigo_rastreamento if is_manifesto_lote else None
                ),
                # gerado_por=request.user # Descomente se tiver um campo User no modelo RelatorioGerado
            )
            messages.success(
                request, f"Relatório PDF '{report_id}' gerado e registrado com sucesso!"
            )
        except Exception as e:
            messages.error(request, f"Erro ao registrar o relatório PDF: {e}")
            # Você pode logar o erro aqui

        # Renderização do PDF
        context_pdf = {
            "resgates": resgates,
            "current_generation_time": current_generation_time,
            "is_manifesto_lote": is_manifesto_lote,
            "report_id": report_id,  # Passa o ID do relatório para o template
            "posto_nome": pdf_posto_nome,
            "produto_nome": pdf_produto_nome,
            "data_geracao_inicio_pdf": pdf_data_geracao_inicio,
            "data_geracao_fim_pdf": pdf_data_geracao_fim,
            "codigo_rastreamento_pdf": pdf_codigo_rastreamento,
            "cliente_nome": cliente_nome,
            "cliente_cpf": cliente_cpf,
            "total_pontos_lote": total_pontos_lote,
        }
        html_string = render_to_string(
            "resgates/relatorio_resgates_pdf.html", context_pdf
        )

        html = HTML(string=html_string, base_url=request.build_absolute_uri())

        stylesheets = []
        css_file_path = os.path.join(settings.STATIC_ROOT, "css", "output.css")

        if os.path.exists(css_file_path):
            stylesheets.append(CSS(filename=css_file_path))
        else:
            print(
                f"ATENÇÃO: output.css não encontrado em {css_file_path}. O PDF pode não ter estilo."
            )

        pdf_file = html.write_pdf(stylesheets=stylesheets)

        response = HttpResponse(pdf_file, content_type="application/pdf")
        filename = (
            f"manifesto_lote_{pdf_codigo_rastreamento}_{report_id}.pdf"
            if is_manifesto_lote
            else f"relatorio_geral_{report_id}.pdf"
        )
        response["Content-Disposition"] = f'inline; filename="{filename}"'
        return response

    # Contexto para a visualização HTML normal da lista de resgates
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

            parsed_resgates = []
            errors = []

            clean_data = raw_data.replace("\r\n", "\n")
            clean_data = re.sub(r"^\d+\/\d+\s*$", "", clean_data, flags=re.MULTILINE)
            clean_data = re.sub(
                r"^Produto \/ Cliente.*Situação\*?\s*$",
                "",
                clean_data,
                flags=re.MULTILINE,
            )
            clean_data = re.sub(
                r"^\*?Total resgatado.*pontos.*$", "", clean_data, flags=re.MULTILINE
            )

            clean_data = re.sub(r"\t+", " ", clean_data)
            clean_data = re.sub(r"^\s*\n", "", clean_data, flags=re.MULTILINE)
            clean_data = clean_data.strip()

            print("\n--- RAW DATA RECEBIDO ---")
            print(repr(raw_data))
            print("\n--- CLEAN DATA (APÓS PRÉ-PROCESSAMENTO) ---")
            print(repr(clean_data))
            print("\n--------------------------\n")

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

            matches = block_pattern.finditer(clean_data)
            match_list = list(matches)
            found_matches = len(match_list)
            print(
                f"\n--- TOTAL DE MATCHES ENCONTRADOS PELO REGEX: {found_matches} ---\n"
            )

            num_parsed = 0
            for match in match_list:
                data = match.groupdict()

                try:
                    gerado_em_str = (
                        f"{data['data_geracao_data']} {data['data_geracao_hora']}"
                    )
                    gerado_em_naive = datetime.strptime(gerado_em_str, "%d/%m/%Y %H:%M")
                    gerado_em_aware = timezone.make_aware(gerado_em_naive)

                    vencimento_str = (
                        f"{data['data_vencimento_data']} {data['data_vencimento_hora']}"
                    )
                    vencimento_naive = datetime.strptime(
                        vencimento_str, "%d/%m/%Y %H:%M"
                    )
                    vencimento_aware = timezone.make_aware(vencimento_naive)

                    quantidade = int(data["quantidade"])
                    pontos_prod = int(data["pontos_prod"])

                except ValueError as e:
                    messages.error(
                        request,
                        f"Erro ao processar dados de resgate (data/hora, quantidade ou pontos): {e}. Dados brutos do item: {match.group(0)}",
                    )
                    errors.append(
                        f"Erro de dados em um resgate: {e}. Detalhes: {match.group(0)[:100]}..."
                    )
                    continue

                produto, created_produto = Produto.objects.get_or_create(
                    nome__iexact=data["produto_full"],
                    defaults={
                        "nome": data["produto_full"],
                        "pontos_necessarios": pontos_prod,
                        "descricao": f"Produto criado automaticamente via importação. Pontos: {pontos_prod}",
                    },
                )
                if created_produto:
                    messages.warning(
                        request,
                        f"Produto '{produto.nome}' não encontrado e foi criado automaticamente. **Revise o estoque e descrição!**",
                    )
                else:
                    if quantidade > 0:
                        pontos_por_unidade_texto = int(pontos_prod / quantidade)
                    else:
                        pontos_por_unidade_texto = 0

                    if pontos_por_unidade_texto != produto.pontos_necessarios:
                        messages.warning(
                            request,
                            f"Pontos por unidade para '{produto.nome}' no texto ({pontos_por_unidade_texto}) "
                            f"diferem do DB ({produto.pontos_necessarios}). "
                            f"**Verifique e ajuste os pontos do produto no cadastro principal.**",
                        )

                cliente, created_cliente = Cliente.objects.get_or_create(
                    nome_completo__iexact=data["cliente_nome"],
                    defaults={
                        "nome_completo": data["cliente_nome"],
                        "observacao": "Cliente criado automaticamente via importação. **Revise o CPF e pontos!**",
                    },
                )
                if created_cliente:
                    messages.warning(
                        request,
                        f"Cliente '{cliente.nome_completo}' não encontrado e foi criado automaticamente. **Revise o CPF e pontos!**",
                    )

                posto, created_posto = Posto.objects.get_or_create(
                    nome__iexact=data["posto_nome"],
                    defaults={
                        "nome": data["posto_nome"],
                        "endereco": "Endereço a ser revisado (criação automática).",
                    },
                )
                if created_posto:
                    messages.warning(
                        request,
                        f"Posto '{posto.nome}' não encontrado e foi criado automaticamente. **Revise o endereço!**",
                    )

                try:
                    Resgate.objects.create(
                        produto=produto,
                        cliente=cliente,
                        posto_resgate=posto,
                        tipo_resgate=data["tipo_resgate"],
                        gerado_em=gerado_em_aware,
                        vencimento=vencimento_aware,
                        quantidade=quantidade,
                        status=data["situacao"] if data["situacao"] else "GERADO",
                    )
                    num_parsed += 1
                except Exception as e:
                    messages.error(
                        request,
                        f"Erro ao salvar resgate para o produto '{produto.nome}': {e}",
                    )
                    errors.append(
                        f"Erro ao salvar: {e}. Detalhes: {match.group(0)[:100]}..."
                    )

            if num_parsed > 0:
                messages.success(
                    request, f"{num_parsed} resgates importados com sucesso!"
                )

            if errors:
                messages.warning(
                    request,
                    f"{len(errors)} resgates tiveram problemas na importação. Verifique as mensagens de aviso.",
                )

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
    messages.warning(
        request,
        "Método não permitido para exclusão direta. Por favor, use o formulário de exclusão.",
    )
    return redirect("resgate_list")


@login_required
def resgate_delete_all(request):
    if request.method == "POST":
        Resgate.objects.all().delete()
        messages.success(request, "Todos os resgates foram excluídos com sucesso!")
        return redirect("resgate_list")
    messages.warning(request, "A exclusão em massa requer uma requisição POST.")
    return redirect("resgate_list")


@login_required
def resgate_export_csv(request):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = (
        f'attachment; filename="resgates_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv"'
    )

    writer = csv.writer(response)

    writer.writerow(
        [
            "ID Resgate",
            "Produto",
            "Pontos Produto (Unid.)",
            "Cliente",
            "CPF Cliente",
            "Posto de Resgate",
            "Endereco Posto",
            "Tipo de Resgate",
            "Gerado Em",
            "Vencimento",
            "Quantidade",
            "Pontos Totais Resgatados",
            "Status",
            "Codigo Rastreamento",
            "Nome Recebedor",
            "Nome Motorista",
        ]
    )

    resgates = Resgate.objects.all().select_related(
        "produto", "cliente", "posto_resgate"
    )
    for resgate in resgates:
        writer.writerow(
            [
                resgate.id,
                resgate.produto.nome,
                resgate.produto.pontos_necessarios,
                resgate.cliente.nome_completo,
                resgate.cliente.cpf,
                resgate.posto_resgate.nome,
                resgate.posto_resgate.endereco,
                resgate.tipo_resgate,
                resgate.gerado_em.strftime("%d/%m/%Y %H:%M"),
                resgate.vencimento.strftime("%d/%m/%Y %H:%M"),
                resgate.quantidade,
                resgate.pontos_totais_resgatados,
                resgate.get_status_display(),
                resgate.codigo_rastreamento,
                resgate.nome_recebedor if resgate.nome_recebedor else "",
                resgate.nome_motorista if resgate.nome_motorista else "",
            ]
        )
    return response


@login_required
def resgate_detail(request, pk):
    """
    Exibe os detalhes de um resgate específico ou gera um PDF do recibo.
    """
    resgate = get_object_or_404(Resgate, pk=pk)

    if "format" in request.GET and request.GET["format"] == "pdf":
        html_string = render_to_string(
            "resgates/recibo_pdf_template.html",
            {"resgate": resgate},
        )

        html = HTML(string=html_string, base_url=request.build_absolute_uri())

        stylesheets = []
        css_file_path = os.path.join(settings.STATIC_ROOT, "css", "output.css")

        if os.path.exists(css_file_path):
            stylesheets.append(CSS(filename=css_file_path))
        else:
            print(
                f"ATENÇÃO: output.css não encontrado em {css_file_path}. O PDF pode não ter estilo."
            )

        pdf_file = html.write_pdf(stylesheets=stylesheets)

        response = HttpResponse(pdf_file, content_type="application/pdf")
        response["Content-Disposition"] = (
            f'inline; filename="recibo_resgate_{resgate.codigo_rastreamento}.pdf"'
        )
        return response

    context = {"resgate": resgate, "title": "Detalhes do Resgate e Recibo"}
    return render(request, "resgates/resgate_detail.html", context)


@login_required
def resgate_validate_tracking(request):
    resgate = None
    if request.method == "POST":
        codigo_rastreamento = request.POST.get("codigo_rastreamento", "").strip()
        nome_recebedor = request.POST.get("nome_recebedor", "").strip()
        nome_motorista = request.POST.get("nome_motorista", "").strip()

        if not codigo_rastreamento:
            messages.error(request, "O código de rastreamento não pode estar vazio.")
        else:
            try:
                resgate = Resgate.objects.get(codigo_rastreamento=codigo_rastreamento)

                if resgate.status == "RESGATADO":
                    messages.warning(
                        request,
                        f"Resgate com código '{codigo_rastreamento}' já foi marcado como RESGATADO anteriormente.",
                    )
                elif resgate.status == "VENCIDO":
                    messages.error(
                        request,
                        f"Resgate com código '{codigo_rastreamento}' está VENCIDO e não pode ser resgatado.",
                    )
                elif resgate.status == "CANCELADO":
                    messages.error(
                        request,
                        f"Resgate com código '{codigo_rastreamento}' está CANCELADO e não pode ser resgatado.",
                    )
                else:
                    resgate.status = "RESGATADO"
                    resgate.nome_recebedor = nome_recebedor if nome_recebedor else None
                    resgate.nome_motorista = nome_motorista if nome_motorista else None
                    resgate.save()
                    messages.success(
                        request,
                        f"Resgate de {resgate.produto.nome} para {resgate.cliente.nome_completo} validado com sucesso!",
                    )
                    return redirect("resgate_detail", pk=resgate.pk)

            except Resgate.DoesNotExist:
                messages.error(
                    request,
                    f"Código de rastreamento '{codigo_rastreamento}' não encontrado.",
                )
            except Exception as e:
                messages.error(request, f"Ocorreu um erro ao validar o resgate: {e}")

    context = {
        "title": "Validar Resgate por Código",
        "resgate_encontrado": resgate,
    }
    return render(request, "resgates/resgate_validate_tracking.html", context)


# NOVA VIEW: Lista de Relatórios Gerados
@login_required
def report_list(request):
    """
    Exibe a lista de todos os relatórios PDF gerados e registrados.
    """
    reports = RelatorioGerado.objects.all().order_by(
        "-data_geracao"
    )  # Ordena do mais recente para o mais antigo

    context = {
        "title": "Relatórios Gerados",
        "reports": reports,
    }
    return render(request, "reports/report_list.html", context)


# NOVA VIEW: Excluir Relatórios Selecionados
@login_required
def report_delete_selected(request):
    if request.method == "POST":
        report_ids = request.POST.getlist(
            "report_ids"
        )  # Obtém a lista de IDs dos checkboxes
        if report_ids:
            try:
                # Filtra e exclui os relatórios com base nos IDs recebidos
                deleted_count, _ = RelatorioGerado.objects.filter(
                    id__in=report_ids
                ).delete()
                messages.success(
                    request, f"{deleted_count} relatório(s) excluído(s) com sucesso!"
                )
            except Exception as e:
                messages.error(request, f"Erro ao excluir relatórios selecionados: {e}")
        else:
            messages.warning(request, "Nenhum relatório selecionado para exclusão.")
    return redirect("report_list")


# NOVA VIEW: Excluir Todos os Relatórios
@login_required
def report_delete_all(request):
    if request.method == "POST":
        try:
            deleted_count, _ = RelatorioGerado.objects.all().delete()
            messages.success(
                request,
                f"Todos os {deleted_count} relatório(s) foram excluído(s) com sucesso!",
            )
        except Exception as e:
            messages.error(request, f"Erro ao excluir todos os relatórios: {e}")
    return redirect("report_list")


# NOVA VIEW: Excluir um único relatório (usado pelo botão individual)
@login_required
def report_delete_single(request, pk):
    if request.method == "POST":
        try:
            report = get_object_or_404(RelatorioGerado, pk=pk)
            report.delete()
            messages.success(
                request, f"Relatório '{report.report_id}' excluído com sucesso!"
            )
        except Exception as e:
            messages.error(request, f"Erro ao excluir relatório: {e}")
    return redirect("report_list")
