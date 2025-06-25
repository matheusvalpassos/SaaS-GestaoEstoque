# 📦 Plataforma de Automação de Relatórios Top Clube

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![Python Version](https://img.shields.io/badge/Python-3.11+-blue)
![Django Version](https://img.shields.io/badge/Django-5.0-darkgreen)
![Status](https://img.shields.io/badge/Status-Online%20na%20Render-brightgreen)

> Uma ferramenta web interna para a Rede Bellas, projetada para automatizar e centralizar a gestão de relatórios de resgate de produtos do programa Top Clube.

---

## 📌 Sobre

Este projeto foi desenvolvido como uma solução interna para otimizar os processos operacionais da Rede Bellas. A plataforma automatiza a importação de dados de resgates, a gestão de status, o controle de clientes e produtos, e a geração de relatórios e manifestos de entrega, substituindo processos manuais e planilhas.

O sistema permite:
- ✅ **Importação em Lote:** Processa e importa centenas de resgates de uma vez, copiando e colando os dados do sistema legado.
- ✅ **Gestão Centralizada:** Controla o ciclo de vida de cada resgate (Gerado, Resgatado, Cancelado) diretamente pela interface.
- 🔐 **Controle de Acesso:** Sistema de autenticação para garantir que apenas a equipe autorizada utilize a ferramenta.
- 🧩 **Interface Moderna:** Um dashboard intuitivo com gráficos e estatísticas para análise rápida.
- 📜 **Relatórios Detalhados:** Gera relatórios em PDF e exporta dados em CSV com um clique.

---

## 🖥️ Telas do Sistema em Ação

#### Dashboard Principal
![Tela do Dashboard Principal](backend/static_dev/img/meusaas%20(1).png)
*Visão geral com estatísticas, gráficos e listas dos itens mais relevantes.*

#### Gestão de Resgates
![Tela de Gestão de Resgates](backend/static_dev/img/meusaas%20(2).png)
*Interface para filtrar, visualizar e gerenciar todos os resgates.*

#### Detalhes e Atualização de Status
![Tela de Detalhes do Resgate](backend/static_dev/img/meusaas%20(3).png)
*Página de detalhes com um formulário dedicado para alterar o status de um resgate.*

#### Importação em Lote
![Tela de Importação em Lote](backend/static_dev/img/meusaas%20(4).png)
*Ferramenta para colar e processar dados brutos, automatizando a criação de registros.*

#### Relatório em PDF
![Exemplo de Relatório em PDF](backend/static_dev/img/meusaas%20(5).png)
*Exemplo do layout profissional dos relatórios gerados em PDF.*

---

## 🛠️ Funcionalidades Principais

| Recurso | Descrição |
|--------|-----------|
| 📊 **Dashboard Dinâmico** | Painel visual com estatísticas, gráficos interativos e listas de Top 5, com animações e saudação dinâmica. |
| 📥 **Importação Inteligente**| Processa texto bruto, cria automaticamente Produtos, Clientes e Postos que não existem e importa os resgates. |
| ⚙️ **Gestão de Status** | Permite alterar o status de cada resgate (Gerado, Resgatado, Cancelado) individualmente. |
| 📄 **Relatórios em PDF** | Gera relatórios gerais e manifestos de entrega em PDF com layout profissional, usando WeasyPrint. |
| 🎨 **Interface Responsiva** | Design moderno e consistente em todas as telas, construído com **Tailwind CSS** e **Font Awesome**. |
| 🔍 **Busca e Filtragem** | Ferramentas de busca e filtros avançados nas páginas de listagem para encontrar dados rapidamente. |

---

## ⚙️ Requisitos

Para rodar este projeto localmente, você precisa de:

- [Python 3.11+](https://www.python.org/downloads/)
- [Node.js](https://nodejs.org/) (para compilar o Tailwind CSS)
- Uma conta no [Supabase](https://supabase.com/) para o banco de dados PostgreSQL.

---

## 📦 Instalação

### Passo 1: Clone o repositório

```bash
git clone [https://github.com/matheusvalpassos/SaaS-GestaoEstoque.git](https://github.com/matheusvalpassos/SaaS-GestaoEstoque.git)
cd SaaS-GestaoEstoque
```

### Passo 2: Instale as dependências

**Backend (Python):**
```bash
cd backend
python -m venv .venv
# No Mac/Linux:
source .venv/bin/activate
# No Windows:
.venv\Scripts\activate
pip install -r requirements.txt
```
**Frontend (Tailwind):**
```bash
cd ../frontend
npm install
```

### Passo 3: Configure as variáveis de ambiente

Dentro da pasta `backend`, crie um arquivo chamado `.env` e adicione as seguintes chaves:
```env
# backend/.env

SECRET_KEY="sua_chave_secreta_django_aqui"
DEBUG=True
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost
DATABASE_URL="sua_connection_string_do_supabase_aqui"
```

### Passo 4: Execute o projeto

```bash
# Volte para a pasta do backend
cd ../backend

# Aplique as migrações do banco de dados
python manage.py migrate

# Inicie o servidor
python manage.py runserver
```
Acesse `http://127.0.0.1:8000` no seu navegador.

---

## 📁 Estrutura do Projeto

```
SaaS-GestaoEstoque/
│
├── backend/
│   ├── config/             # Configurações do projeto Django (settings.py)
│   ├── core/               # App principal com models, views e templates
│   ├── manage.py           # Gerenciador do Django
│   ├── build.sh            # Script de build para a Render
│   ├── requirements.txt    # Dependências do Python
│   └── uwsgi.ini           # Configuração do servidor uWSGI
│
└── frontend/
    ├── src/                # Arquivos fonte do CSS (input.css)
    ├── package.json        # Dependências do Node.js
    └── tailwind.config.js  # Configuração do Tailwind
```

---

## 🧪 Próximos Recursos Planejados

- [ ] Histórico de alterações por resgate.
- [ ] Gráficos mais detalhados com filtros de período no dashboard.
- [ ] Exportação de relatórios em formato Excel.

---

## 🤝 Contribuições
Contribuições são sempre bem-vindas! Se você tiver melhorias de código, correções ou novas funcionalidades, abra uma **Pull Request** ou crie uma **Issue**.

---

## 📝 Licença
MIT License – veja o arquivo `LICENSE` para mais detalhes.

---

## 💬 Contato
Se quiser falar comigo ou sugerir melhorias:

- **GitHub:** [@matheusvalpassos](https://github.com/matheusvalpassos)
- **Discord:** matheusvalpassos

---

## ⚠️ Aviso de Responsabilidade

Este projeto foi desenvolvido como uma ferramenta interna para a Rede Bellas. O autor não se responsabiliza por perdas de dados ou problemas decorrentes do uso inadequado deste software.
