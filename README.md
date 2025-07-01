# 📦 Plataforma de Automação de Relatórios Top Clube

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![Python Version](https://img.shields.io/badge/Python-3.10-blue)
![Django Version](https://img.shields.io/badge/Django-5.0-darkgreen)
![Status](https://img.shields.io/badge/Deploy-PythonAnywhere-brightgreen)

> Uma ferramenta web interna para a Rede Bellas, projetada para automatizar e centralizar a gestão de relatórios de resgate de produtos do programa Top Clube.

---

## 📌 Sobre

Este projeto foi desenvolvido como uma solução interna para otimizar os processos operacionais da Rede Bellas. A plataforma automatiza a importação de dados de resgates, a gestão de status, o controle de clientes e produtos, e a geração de relatórios, substituindo processos manuais e planilhas.

O sistema permite:
- ✅ **Importação em Lote:** Processa e importa centenas de resgates de uma vez, copiando e colando os dados do sistema legado.
- ✅ **Gestão Centralizada:** Controla o ciclo de vida de cada resgate (Gerado, Resgatado, Cancelado) diretamente pela interface.
- 🔐 **Controle de Acesso:** Sistema de autenticação para garantir que apenas a equipe autorizada utilize a ferramenta.
- 🧩 **Interface Moderna:** Um dashboard intuitivo com gráficos e estatísticas para análise rápida.
- 📜 **Relatórios Detalhados:** Gera relatórios em PDF e exporta dados em CSV com um clique.

---

## 🖥️ Telas do Sistema em Ação

Acesse a aplicação ao vivo em: **[https://msvrocha.pythonanywhere.com/](https://msvrocha.pythonanywhere.com/)**

#### Homepage
![Tela da Homepage](backend/static_dev/img/meusaas%20(6).png)
*Página inicial de apresentação da plataforma.*

#### Página de Login e Registro
![Tela de Login](backend/static_dev/img/meusaas%20(7).png)
*Formulários de acesso e criação de conta para usuários autorizados.*

#### Dashboard Principal
![Tela do Dashboard Principal](backend/static_dev/img/meusaas%20(1).png)
*Visão geral com estatísticas, gráficos e listas dos itens mais relevantes.*

#### Relatórios Gerados
![Tela de Relatórios Gerados](backend/static_dev/img/meusaas%20(2).png)
*Visualize e gerencie todos os relatórios gerados no sistema.*

#### Lista de Resgates
![Tela da Lista de Resgates](backend/static_dev/img/meusaas%20(3).png)
*Filtre, visualize, exporte e gerencie todos os resgates do sistema.*

#### Gerenciar Clientes
![Tela de Gerenciar Clientes](backend/static_dev/img/meusaas%20(4).png)
*Adicione, edite e visualize todos os clientes do sistema.*

#### Gerenciar Produtos
![Tela de Gerenciar Produtos](backend/static_dev/img/meusaas%20(5).png)
*Adicione, edite e visualize todos os produtos disponíveis para resgate.*


---

## 🛠️ Funcionalidades Principais

| Recurso | Descrição |
|--------|-----------|
| 📊 **Dashboard Dinâmico** | Painel visual com estatísticas, gráficos interativos e listas de Top 5, com animações e saudação dinâmica. |
| 📥 **Importação Inteligente**| Processa texto bruto, cria automaticamente Produtos, Clientes e Postos que não existem e importa os resgates. |
| ⚙️ **Gestão de Status** | Permite alterar o status de cada resgate (Gerado, Resgatado, Cancelado) individualmente. |
| 📄 **Relatórios em PDF** | Gera relatórios em PDF com layout profissional, usando WeasyPrint. |
| 🎨 **Interface Responsiva** | Design moderno e consistente em todas as telas, construído com **Tailwind CSS** e **Font Awesome**. |
| 🔍 **Busca e Filtragem** | Ferramentas de busca e filtros avançados nas páginas de listagem para encontrar dados rapidamente. |

---

## ⚙️ Requisitos

Para rodar este projeto localmente, você precisa de:

- [Python 3.10+](https://www.python.org/downloads/)
- [Node.js](https://nodejs.org/) (para compilar o Tailwind CSS)

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
```
> **Nota:** Para o ambiente local, o banco de dados padrão é o `SQLite`, que não requer uma `DATABASE_URL`.

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
│   └── requirements.txt    # Dependências do Python
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
