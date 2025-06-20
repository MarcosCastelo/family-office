# 🧠 Family Office Digital — Sistema de Gestão Patrimonial

## 🎯 Visão Geral

Sistema web para **gestão de patrimônio e finanças**, com foco em:
- Cadastro de ativos financeiros por classe
- Análise de risco (individual e consolidada)
- Alertas e recomendações baseadas em regras
- Multiusuários vinculados a múltiplas famílias (multi-tenant)
- Controle de permissões e escopos
- Geração de relatórios e exportações fiscais

---

## 🧱 Stack e Ferramentas

| Componente             | Ferramenta                  |
|------------------------|-----------------------------|
| Backend                | Flask 3.1.1 (App Factory)    |
| ORM                   | SQLAlchemy                  |
| Auth                  | Flask-JWT-Extended          |
| Migrations            | Alembic via Flask-Migrate   |
| Agendamentos          | APScheduler                 |
| Relatórios            | WeasyPrint                  |
| OCR                   | Tesseract + pdfminer.six    |
| Dependências          | Poetry + pyproject.toml     |
| Banco Local           | SQLite (`local.db`)         |
| Testes                | Pytest                      |
| Uploads (futuro)      | Pandas, openpyxl, xlrd      |
| Documentação API      | Flask-RESTX (Swagger)       |

---

## 📁 Estrutura do Projeto

```bash
family_office/
├── app/
│   ├── config/
│   │   ├── config.py
│   │   └── extensions.py
│   ├── models/
│   │   ├── user.py
│   │   ├── family.py
│   │   └── permission.py
│   ├── routes/
│   │   ├── auth.py
│   │   └── family.py
│   ├── schema/
│   │   └── user_schema.py
│   ├── services/
│   │   ├── __init__.py
│   │   └── auth_service.py
│   └── decorators/
│       ├── permissions.py
│       └── family_access.py
├── migrations/
├── tests/
├── .env
├── .env.example
├── .tool-versions
├── .gitignore
├── local.db
├── pyproject.toml
├── poetry.lock
├── run.py
└── README.md
```

---

## ✅ Funcionalidades já implementadas

- Autenticação JWT com refresh token
- Registro de usuários com senha hash
- Migrations automáticas com Alembic
- Associação N:N entre usuários e famílias (`user_family`)
- Permissões N:N (`user_permission`)
- Decorators:
  - `@require_permission('admin')`
  - `@require_family(family_id)`
- Blueprint de auth funcionando: `/auth/login`, `/auth/register`
- Rota `/family/join/<id>` para vincular usuário autenticado à família
- `DATABASE_URL` carregado do `.env` com `sqlite:///local.db`

---

## 🔜 Próximos passos

### 📦 Cadastro de ativos
- Modelos para classes de ativos (RF, RV, Fundos, Imóveis)
- Herança de modelo `Asset`
- Asso à ciação dos ativos`Family`

### 📥 Uploads
- Upload de `.csv`, `.xlsx` com validação
- OCR com Tesseract
- Autoidentificação de tipo de ativo

### 📊 Risco e Alertas
- Score de risco por ativo e carteira
- Alertas: concentração, liquidez, inadimplência

### 📑 Relatórios
- PDF com WeasyPrint
- Exportações fiscais (ganhos/prejuízos)

### 🧠 Suitability
- Definição de perfil (conservador, moderado, arrojado)
- Análise de compatibilidade da carteira
- Sugestões de rebalanceamento

---

## 📌 Comandos úteis

```bash
poetry install
poetry run flask run
poetry run flask db migrate -m "..."
poetry run flask db upgrade
poetry run pytest
poetry shell
```
