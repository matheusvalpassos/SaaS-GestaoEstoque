# core/models.py

from django.db import models
from django.utils import timezone
import uuid  # Para gerar códigos de rastreamento únicos
from django.db.models import JSONField  # Importar JSONField para armazenar filtros

# As escolhas de status para Resgate já estão dentro da classe Resgate, o que é ok.


class Posto(models.Model):
    nome = models.CharField(max_length=100, unique=True, verbose_name="Nome do Posto")
    endereco = models.CharField(
        max_length=200, blank=True, null=True, verbose_name="Endereço"
    )
    # Você pode adicionar mais campos como telefone, CNPJ, etc.

    class Meta:
        verbose_name = "Posto"
        verbose_name_plural = "Postos"
        ordering = ["nome"]  # Ordena por nome do posto

    def __str__(self):
        return self.nome


class Produto(models.Model):
    nome = models.CharField(max_length=200)
    descricao = models.TextField(blank=True, null=True)
    pontos_necessarios = models.IntegerField(default=0)
    estoque = models.IntegerField(default=0)
    ativo = models.BooleanField(default=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"
        ordering = ["nome"]

    def __str__(self):
        return self.nome


class Cliente(models.Model):
    # user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, help_text="Usuário Django associado a este cliente (opcional)") # Opcional: para linkar com usuários de login
    nome_completo = models.CharField(max_length=255)
    cpf = models.CharField(max_length=14, unique=True, null=True, blank=True)
    telefone = models.CharField(max_length=20, blank=True, null=True)
    data_nascimento = models.DateField(blank=True, null=True)
    pontos = models.IntegerField(default=0)
    data_cadastro = models.DateTimeField(auto_now_add=True)
    data_ultima_atualizacao = models.DateTimeField(auto_now=True)

    # Adicione ESTA LINHA para incluir o campo 'observacao'
    observacao = models.TextField(
        blank=True,
        null=True,
        help_text="Observações adicionais sobre o cliente, como origem da criação.",
    )

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ["nome_completo"]

    def __str__(self):
        return self.nome_completo


class Resgate(models.Model):
    STATUS_CHOICES = [
        ("GERADO", "Gerado"),
        ("RESGATADO", "Resgatado"),
        ("VENCIDO", "Vencido"),
        ("CANCELADO", "Cancelado"),
    ]

    produto = models.ForeignKey(
        Produto,
        on_delete=models.PROTECT,
        related_name="resgates",
        verbose_name="Produto",
    )
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.PROTECT,
        related_name="resgates",
        verbose_name="Cliente",
    )
    posto_resgate = models.ForeignKey(
        Posto,
        on_delete=models.PROTECT,
        related_name="resgates",
        verbose_name="Posto de Resgate",
    )

    # O campo 'Resgate em' na sua tabela parece ser um campo de texto descritivo.
    # Vamos chamá-lo de 'tipo_resgate'
    tipo_resgate = models.CharField(
        max_length=255,
        default="Resgate em estabelecimentos escolhidos (estoque próprio)",
        verbose_name="Tipo de Resgate",
    )

    gerado_em = models.DateTimeField(default=timezone.now, verbose_name="Gerado Em")
    vencimento = models.DateTimeField(verbose_name="Vencimento")
    quantidade = models.PositiveIntegerField(default=1, verbose_name="Quantidade")
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default="GERADO", verbose_name="Situação"
    )

    # Para o "Total Resgatado", pode ser uma propriedade que calcula pontos * quantidade
    # Ou um campo armazenado se necessário para performance ou auditoria
    pontos_totais_resgatados = models.PositiveIntegerField(
        editable=False,  # Não será editável diretamente no admin
        verbose_name="Total Resgatado (Pontos)",
    )

    # Campo para o código de rastreamento
    codigo_rastreamento = models.CharField(
        max_length=32,
        unique=True,
        default=uuid.uuid4,  # Gera um UUID automaticamente
        verbose_name="Código de Rastreamento",
    )

    # Campos para as assinaturas no recibo
    nome_recebedor = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name="Nome do Recebedor (na entrega)",
    )
    assinatura_recebedor = models.TextField(
        blank=True, null=True, verbose_name="Assinatura Recebedor (Base64/Imagem)"
    )  # Para futura implementação de captura de assinatura
    nome_motorista = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name="Nome do Motorista (na entrega)",
    )
    assinatura_motorista = models.TextField(
        blank=True, null=True, verbose_name="Assinatura Motorista (Base64/Imagem)"
    )  # Para futura implementação de captura de assinatura

    class Meta:
        verbose_name = "Resgate"
        verbose_name_plural = "Resgates"
        ordering = ["-gerado_em"]  # Ordena do mais novo para o mais antigo

    def save(self, *args, **kwargs):
        # Calcula os pontos totais antes de salvar
        if not self.pontos_totais_resgatados or self.pontos_totais_resgatados == 0:
            if self.produto and self.quantidade is not None:
                self.pontos_totais_resgatados = (
                    self.produto.pontos_necessarios * self.quantidade
                )
            else:
                self.pontos_totais_resgatados = 0  # Garante um valor padrão se produto/quantidade não estiverem disponíveis

        # Gerar um código de rastreamento se não existir e se o campo for default=uuid.uuid4
        # A forma default=uuid.uuid4 já garante que um UUID será gerado na criação do objeto,
        # então não é estritamente necessário um 'if not self.codigo_rastreamento' aqui a menos que você
        # sobrescreva o default em algum momento.
        # self.codigo_rastreamento = str(uuid.uuid4())[:10].upper() # Ex: F8D2A1C7B9

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Resgate de {self.quantidade}x {self.produto.nome} por {self.cliente.nome_completo}"


# NOVO MODELO PARA ARMAZENAR METADADOS DE RELATÓRIOS GERADOS
class RelatorioGerado(models.Model):
    REPORT_TYPE_CHOICES = [
        ("GERAL", "Relatório Geral"),
        ("MANIFESTO_LOTE", "Manifesto de Lote"),
    ]

    report_id = models.CharField(
        max_length=50, unique=True, help_text="ID único de cada relatório gerado."
    )
    tipo = models.CharField(max_length=20, choices=REPORT_TYPE_CHOICES)
    data_geracao = models.DateTimeField(default=timezone.now)
    # Use JSONField para armazenar os filtros de forma flexível. Certifique-se de que JSONField está importado.
    filtros_aplicados = JSONField(blank=True, null=True)
    codigo_rastreamento_lote = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Código de rastreamento se for um manifesto de lote.",
    )
    # Link para o usuário que gerou o relatório (opcional, requer User importado)
    # gerado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Relatório {self.report_id} - {self.get_tipo_display()} em {self.data_geracao.strftime('%d/%m/%Y %H:%M')}"

    class Meta:
        verbose_name = "Relatório Gerado"
        verbose_name_plural = "Relatórios Gerados"
        ordering = ["-data_geracao"]  # Ordena os relatórios pelo mais recente
