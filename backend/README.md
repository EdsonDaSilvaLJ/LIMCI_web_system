# Backend

API do protótipo construída com Django e Django Ninja.

## Estrutura atual

```text
backend/
├── config/
└── apps/
    ├── analyses/
    ├── core/
    ├── leukemia/
    └── renal/
```

O módulo de leucemia mantém separados seus schemas, pré-processamento,
carregamento do modelo e inferência. O módulo renal está reservado para a
integração posterior dos pesos da U-Net/VGG-19.

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
POST /api/v1/modules/leukemia/predict
```

## Artefatos do módulo de leucemia

O backend espera os seguintes arquivos na raiz do repositório:

```text
model_weights/leukemia/leukemia_efficientnet_b0.keras
docs/results/leukemia/inference_config.json
```

O modelo não deve ser versionado. O arquivo de configuração deve conter o
tamanho de entrada `[224, 224]` e o threshold experimental de inferência.

Teste manual:

```bash
curl -X POST \
  http://127.0.0.1:8000/api/v1/modules/leukemia/predict \
  -F "file=@/caminho/para/celula.bmp"
```

O endpoint aceita uma imagem recortada de uma única célula. O retorno é
experimental e não constitui diagnóstico clínico.

## Testes

```bash
python manage.py check
python manage.py test
```
