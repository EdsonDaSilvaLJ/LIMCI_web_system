# Pesos dos modelos

Os pesos não são versionados neste repositório devido ao tamanho dos arquivos.

Estrutura local esperada:

```text
model_weights/
├── renal/
└── leukemia/
    └── leukemia_efficientnet_b0.keras
```

Cada modelo deverá ter sua origem, versão, checksum e configuração de pré-processamento documentadas antes da integração.

O modelo de leucemia foi exportado com TensorFlow 2.20.0. O backend carrega o
arquivo completo `.keras` de forma lazy e utiliza a configuração versionada em
`docs/results/leukemia/inference_config.json`.
