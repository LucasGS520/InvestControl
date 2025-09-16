# InvestControl

> Sistema de gestão de investimentos. Este README serve como a “capa” do projeto, guiando setup, execução, arquitetura, padrões e trilha de contribuição. Os requisitos e escopo detalhados estão descritos no SRS.

- Documento SRS: [SRS_InvestControl_Definitivo.pdf](./SRS_InvestControl_Definitivo.pdf)
- Status: Em definição e bootstrapping inicial
- Stack principal:
  - Backend: Python (FastAPI), PostgreSQL, SQLAlchemy, Alembic, JWT
  - Frontend Web: Vue.js, HTML, CSS
  - Mobile (futuro): Flutter
  - Infra/Operações: Docker, Docker Compose, Kubernetes, Prometheus, Grafana, Loki, CI/CD (GitHub Actions ou GitLab CI), Git

---

## Sumário
- [Visão Geral](#visão-geral)
- [Arquitetura & Tecnologias](#arquitetura--tecnologias)
- [Estrutura de Pastas (proposta)](#estrutura-de-pastas-proposta)
- [Primeiros Passos](#primeiros-passos)
  - [Requisitos](#requisitos)
  - [Execução Rápida (Docker Compose)](#execução-rápida-docker-compose)
  - [Setup Local - Backend](#setup-local---backend)
  - [Setup Local - Frontend](#setup-local---frontend)
- [Banco de Dados & Migrações](#banco-de-dados--migrações)
- [Autenticação & Autorização (JWT)](#autenticação--autorização-jwt)
- [Documentação da API](#documentação-da-api)
- [Qualidade (Lint, Testes, Formatação)](#qualidade-lint-testes-formatação)
- [Observabilidade & Logs](#observabilidade--logs)
- [CI/CD](#cicd)
- [Kubernetes (Produção)](#kubernetes-produção)
- [Roadmap](#roadmap)
- [Contribuição](#contribuição)
- [Variáveis de Ambiente](#variáveis-de-ambiente)
- [Licença](#licença)

---

## Visão Geral
O InvestControl é um sistema para controle e acompanhamento de investimentos, com foco em registro de operações, carteira, indicadores e relatórios. As funcionalidades, regras de negócio, personas e requisitos não-funcionais estão especificados no documento SRS.

- Consulte o SRS: [SRS_InvestControl_Definitivo.pdf](./SRS_InvestControl_Definitivo.pdf)
- Este README prioriza o “como” desenvolver, executar e manter o sistema.

## Arquitetura & Tecnologias
- Backend
  - Python + FastAPI
  - Banco: PostgreSQL
  - ORM: SQLAlchemy
  - Migrações: Alembic
  - Auth: JWT (Bearer Token)
- Frontend Web
  - Vue.js
  - HTML, CSS
- Mobile (futuro)
  - Flutter
- Infra e Operações
  - Docker e Docker Compose
  - Kubernetes (produção)
  - Observabilidade: Prometheus & Grafana
  - Logs: Loki (Grafana Loki)
  - CI/CD: GitHub Actions ou GitLab CI
  - Git (GitHub)

## Estrutura de Pastas (proposta)
A estrutura será consolidada conforme implementação. Proposta inicial:

```
.
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── api/            # rotas FastAPI
│   │   ├── core/           # config, segurança, deps
│   │   ├── models/         # SQLAlchemy
│   │   ├── schemas/        # Pydantic
│   │   ├── services/       # regras de negócio
│   │   └── db/             # sessão, repositórios
│   ├── alembic/
│   │   └── versions/
│   ├── alembic.ini
│   ├── pyproject.toml / requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── .env.example
├── infra/
│   ├── docker/
│   │   ├── backend.Dockerfile
│   │   └── frontend.Dockerfile
│   ├── k8s/
│   │   ├── base/
│   │   └── overlays/
│   ├── monitoring/         # prometheus, grafana, loki
│   └── docker-compose.yml
├── docs/
│   └── SRS_InvestControl_Definitivo.pdf
└── README.md
```

> Observação: No momento, apenas o SRS está versionado. O restante será adicionado conforme os módulos forem implementados.

## Primeiros Passos
### Requisitos
- Windows 10/11
- Python 3.11+
- Node.js 20+ e npm 10+
- Docker Desktop e Docker Compose
- (Opcional) PostgreSQL 14+ local, se não usar Docker

### Execução Rápida (Docker Compose)
Será disponibilizado um `infra/docker-compose.yml`. Exemplo de referência (simplificado):

```yaml
version: "3.9"
services:
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: investcontrol
      POSTGRES_USER: invest
      POSTGRES_PASSWORD: invest
    ports:
      - "5432:5432"
    volumes:
      - db_data:/var/lib/postgresql/data

  backend:
    build: ../backend
    environment:
      DATABASE_URL: postgresql+psycopg2://invest:invest@db:5432/investcontrol
      SECRET_KEY: change-me
      ACCESS_TOKEN_EXPIRE_MINUTES: 60
      ALGORITHM: HS256
    depends_on:
      - db
    ports:
      - "8000:8000"

  frontend:
    build: ../frontend
    ports:
      - "5173:5173"
    depends_on:
      - backend

volumes:
  db_data:
```

Com o arquivo criado:

```cmd
cd infra
docker compose up --build
```

- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Frontend: http://localhost:5173

### Setup Local - Backend
1) Criar e ativar virtualenv:
```cmd
cd backend
python -m venv .venv
.\.venv\Scripts\activate
```

2) Instalar dependências (será definido em `requirements.txt` ou `pyproject.toml`):
```cmd
pip install -r requirements.txt
```

3) Definir variáveis de ambiente (ou criar `.env`):
```cmd
set DATABASE_URL=postgresql+psycopg2://invest:invest@localhost:5432/investcontrol
set SECRET_KEY=change-me
set ACCESS_TOKEN_EXPIRE_MINUTES=60
set ALGORITHM=HS256
```

4) Aplicar migrações:
```cmd
alembic upgrade head
```

5) Executar a API (ex.: Uvicorn):
```cmd
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Setup Local - Frontend
1) Instalar dependências:
```cmd
cd frontend
npm install
```

2) Executar em modo dev:
```cmd
npm run dev
```

3) Build de produção:
```cmd
npm run build
```

> Configure a URL base da API (ex.: `VITE_API_BASE_URL=http://localhost:8000`) em um `.env` do frontend.

## Banco de Dados & Migrações
- Alembic
  - Criar nova migração: `alembic revision --autogenerate -m "<mensagem>"`
  - Aplicar migrações: `alembic upgrade head`
  - Reverter: `alembic downgrade -1`
- Modelagem com SQLAlchemy (camada `app/models`) e mapeamentos Pydantic (`app/schemas`).

## Autenticação & Autorização (JWT)
- Fluxo: login → emissão de access token (Bearer) → consumo de endpoints protegidos.
- Header de autorização: `Authorization: Bearer <token>`
- Claims mínimas: `sub` (usuário), expiração (`exp`).
- Rotas públicas vs. privadas conforme definido no SRS.

## Documentação da API
- FastAPI expõe Swagger UI em `/docs` e Redoc em `/redoc`.
- Ao subir localmente, acesse: `http://localhost:8000/docs`.

## Qualidade (Lint, Testes, Formatação)
- Lint/format: recomenda-se `ruff` + `black` (Python) e `eslint` + `prettier` (Frontend).
- Testes backend: `pytest` com cobertura.
- Testes frontend: `vitest`/`jest` + `testing-library`.
- Hooks (opcional): `pre-commit` para validar lint/format/testes.

## Observabilidade & Logs
- Métricas (prod): Prometheus + Grafana.
- Logs: Loki + Grafana Explore.
- Healthchecks: endpoints de liveness/readiness no backend.

## CI/CD
- GitHub Actions ou GitLab CI com estágios típicos:
  - `lint` → `test` → `build` → `docker push` → `deploy`
- Artefatos Docker publicados em registry.
- Gate de qualidade antes de deploy.

## Kubernetes (Produção)
- Manifests/Helm Charts em `infra/k8s/`.
- Boas práticas: ConfigMaps/Secrets, HPA, liveness/readiness, recursos, tolerations/affinity conforme SLA.
- Observabilidade integrada (ServiceMonitor/PodMonitor se usar Prometheus Operator).

## Roadmap
- Fase 1: Backend + Frontend Web (MVP conforme SRS)
- Fase 2: Melhorias de UX, relatórios avançados, integrações
- Fase 3: App Mobile com Flutter

## Contribuição
- Branching: `main` (estável), `develop` (integração), feature branches (`feature/<nome>`).
- Commits: Conventional Commits (ex.: `feat:`, `fix:`, `chore:`).
- PRs com descrição, prints (quando UI) e checklist de testes.
- Issues: use templates (bug/feature) quando disponíveis.

## Variáveis de Ambiente
Backend (exemplo):
```
DATABASE_URL=postgresql+psycopg2://invest:invest@localhost:5432/investcontrol
SECRET_KEY=change-me
ACCESS_TOKEN_EXPIRE_MINUTES=60
ALGORITHM=HS256
ENV=development
```

Frontend (exemplo):
```
VITE_API_BASE_URL=http://localhost:8000
```

## Licença
A definir.
