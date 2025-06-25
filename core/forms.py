# backend/core/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from .models import Produto, Cliente, Posto, Resgate


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + ("email",)  # Opcional: adicionar email


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = UserChangeForm.Meta.fields


class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ["nome", "descricao", "pontos_necessarios", "estoque", "ativo"]
        # Opcional: Você pode personalizar os widgets para melhor aparência
        widgets = {
            "nome": forms.TextInput(
                attrs={
                    "class": "shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                }
            ),
            "descricao": forms.Textarea(
                attrs={
                    "class": "shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline h-32"
                }
            ),
            "pontos_necessarios": forms.NumberInput(
                attrs={
                    "class": "shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                }
            ),
            "estoque": forms.NumberInput(
                attrs={
                    "class": "shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                }
            ),
            "ativo": forms.CheckboxInput(attrs={"class": "mr-2 leading-tight"}),
        }
        labels = {
            "nome": "Nome do Produto",
            "descricao": "Descrição",
            "pontos_necessarios": "Pontos Necessários",
            "estoque": "Estoque Disponível",
            "ativo": "Ativo (Disponível para resgate)",
        }


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        # Inclua todos os campos que você deseja gerenciar via formulário
        fields = ["nome_completo", "cpf", "telefone", "data_nascimento", "pontos"]
        # Opcional: Personalize os widgets para Tailwind CSS
        widgets = {
            "nome_completo": forms.TextInput(
                attrs={
                    "class": "shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                }
            ),
            "cpf": forms.TextInput(
                attrs={
                    "class": "shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                }
            ),
            "telefone": forms.TextInput(
                attrs={
                    "class": "shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                }
            ),
            "data_nascimento": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline",
                }
            ),
            "pontos": forms.NumberInput(
                attrs={
                    "class": "shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                }
            ),
        }
        labels = {
            "nome_completo": "Nome Completo",
            "cpf": "CPF",
            "telefone": "Telefone",
            "data_nascimento": "Data de Nascimento",
            "pontos": "Pontos Atuais",
        }


class ResgateParseForm(forms.Form):
    raw_data = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "rows": 20,
                "class": "shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline",
                "placeholder": "Cole os dados de resgate aqui...",
            }
        ),
        label="Colar Dados de Resgate",
        help_text="Cole o texto dos resgates exatamente como copiado da origem.",
    )


class ResgateFilterForm(forms.Form):
    """
    Formulário para filtrar resgates por Posto, Produto e Data/Hora de Geração.
    """

    posto = forms.ModelChoiceField(
        queryset=Posto.objects.all().order_by("nome"),
        empty_label="Todos os Postos",
        required=False,
        widget=forms.Select(
            attrs={
                "class": "mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"
            }
        ),
    )
    produto = forms.ModelChoiceField(
        queryset=Produto.objects.all().order_by("nome"),
        empty_label="Todos os Produtos",
        required=False,
        widget=forms.Select(
            attrs={
                "class": "mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"
            }
        ),
    )
    # Novos campos para o filtro de data/hora de importação
    data_geracao_inicio = forms.DateTimeField(
        label="Data/Hora de Geração (Início)",
        required=False,
        widget=forms.DateTimeInput(
            attrs={
                "type": "datetime-local",  # Usa o widget HTML5 para data e hora
                "class": "mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50",
            }
        ),
        input_formats=["%Y-%m-%dT%H:%M"],  # Formato esperado do input datetime-local
    )
    data_geracao_fim = forms.DateTimeField(
        label="Data/Hora de Geração (Fim)",
        required=False,
        widget=forms.DateTimeInput(
            attrs={
                "type": "datetime-local",  # Usa o widget HTML5 para data e hora
                "class": "mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50",
            }
        ),
        input_formats=["%Y-%m-%dT%H:%M"],  # Formato esperado do input datetime-local
    )
    # NOVO CAMPO: Código de Rastreamento para filtro
    codigo_rastreamento = forms.CharField(
        label="Cód. Rastr. (Lote)",
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50",
                "placeholder": "Ex: 123ABC456",
            }
        ),
    )
