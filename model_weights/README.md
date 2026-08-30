# Pesos dos modelos

Os pesos não são versionados neste repositório devido ao tamanho dos arquivos.

Estrutura local esperada:

```text
model_weights/
├── renal/
│   └── modelo_fold1.h5
└── leukemia/
    └── leukemia_efficientnet_b0.keras
```

Cada modelo deverá ter sua origem, versão, checksum e configuração de pré-processamento documentadas antes da integração.

O modelo de leucemia foi exportado com TensorFlow 2.20.0. O backend carrega o
arquivo completo `.keras` de forma lazy e utiliza a configuração versionada em
`docs/results/leukemia/inference_config.json`.

O modelo renal é um arquivo de pesos, não um modelo completo. O backend
reconstrói a U-Net/VGG-19 e executa `load_weights()`. O caminho, o número do
fold e o threshold são configurados por `RENAL_MODEL_PATH`,
`RENAL_MODEL_FOLD` e `RENAL_THRESHOLD`. O fold 1 é operacional e provisório;
não foi declarado como o melhor fold.
