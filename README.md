# LIMCI Web System

Protótipo desenvolvido no contexto de uma **Iniciação Tecnológica (I.T.)** para integrar modelos de visão computacional aplicados à análise de imagens patológicas.

## Escopo da primeira entrega

A aplicação será organizada como um monólito modular com dois módulos independentes:

- **Renal:** segmentação de glomérulos com U-Net/VGG-19, produzindo máscara, sobreposição e medidas derivadas.
- **LLA-B:** classificação binária de imagens recortadas de células sanguíneas em **normal** ou **maligna**, usando transferência de aprendizado com EfficientNet-B0.

O módulo de LLA-B utiliza imagens celulares já recortadas do conjunto público C-NMC 2019. A primeira versão não processa lâminas inteiras (WSI) e não substitui a avaliação de profissionais qualificados.

## Arquitetura prevista

- Frontend: React
- Backend: Django + Django Ninja
- Banco de dados: PostgreSQL
- Treinamento experimental: Google Colab
- Modelos: TensorFlow/Keras

## Estrutura do repositório

```text
backend/        API, persistência e módulos de inferência
frontend/       interface web
notebooks/      auditoria, treinamento e avaliação
docs/           arquitetura e documentação acadêmica
model_weights/  instruções; pesos não são versionados
```

## Experimento C-NMC 2019

A separação definida preserva os pacientes entre os conjuntos:

- treinamento: 7.108 imagens;
- validação: 3.553 imagens;
- teste preliminar: 1.867 imagens.

Datasets e pesos dos modelos não são armazenados neste repositório.

## Estado atual

O pipeline experimental da C-NMC 2019 e os endpoints de classificação de
LLA-B e segmentação renal estão implementados. A persistência é independente
por módulo e a interface React consome ambos. O módulo renal depende da
presença local do peso configurado e utiliza provisoriamente o fold 1.

A metodologia da integração renal, a atribuição das contribuições e as
limitações estão documentadas em [`docs/renal_integration.md`](docs/renal_integration.md).
Há três amostras de teste funcional em [`docs/samples/renal/`](docs/samples/renal/).
