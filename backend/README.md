# Backend

API do protótipo construída com Django e Django Ninja.

Estrutura planejada:

```text
backend/
├── config/
└── apps/
    ├── analyses/
    ├── renal/
    └── leukemia/
```

Cada módulo clínico manterá separados seus schemas, pré-processamento, carregamento do modelo e inferência. Os primeiros endpoints serão `GET /api/v1/health` e `GET /api/v1/modules`.
