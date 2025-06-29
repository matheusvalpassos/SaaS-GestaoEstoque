# Generated by Django 5.2.3 on 2025-06-23 13:08

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0002_produto_atualizado_em_produto_criado_em_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="produto",
            name="atualizado_em",
        ),
        migrations.RemoveField(
            model_name="produto",
            name="criado_em",
        ),
        migrations.AddField(
            model_name="cliente",
            name="data_cadastro",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="cliente",
            name="data_nascimento",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="cliente",
            name="data_ultima_atualizacao",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name="cliente",
            name="pontos",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="produto",
            name="data_atualizacao",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name="produto",
            name="data_criacao",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="cliente",
            name="cpf",
            field=models.CharField(default=1, max_length=14, unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="cliente",
            name="nome_completo",
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name="cliente",
            name="telefone",
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name="produto",
            name="ativo",
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name="produto",
            name="descricao",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="produto",
            name="estoque",
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="produto",
            name="nome",
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name="produto",
            name="pontos_necessarios",
            field=models.IntegerField(default=0),
        ),
    ]
