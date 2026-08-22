# Backend

API do protótipo construída com Django e Django Ninja.

## Estrutura atual

```text
backend/
├── config/
└── apps/
    └── core/
```

Os módulos `renal`, `leukemia` e `analyses` serão adicionados nas próximas etapas. Cada módulo clínico manterá separados seus schemas, pré-processamento, carregamento do modelo e inferência.

## Execução local

A partir da pasta `backend/`:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py runserver
```

A documentação interativa ficará em:

```text
http://127.0.0.1:8000/api/v1/docs
```

## Endpoints disponíveis

```text
GET /api/v1/health
GET /api/v1/modules
```

## Testes

```bash
python manage.py check
python manage.py test
```
