# Arquitetura inicial

## Objetivo

Integrar, em uma única aplicação acadêmica, dois modelos com tarefas diferentes e interfaces padronizadas.

## Componentes

| Componente | Responsabilidade |
|---|---|
| React | Upload, pré-visualização e apresentação dos resultados |
| Django Ninja | API HTTP, validação, persistência e roteamento |
| Módulo renal | Segmentação de imagem renal com U-Net/VGG-19 |
| Módulo LLA-B | Classificação de célula recortada com EfficientNet-B0 |
| PostgreSQL | Metadados e resultados próprios de cada módulo |

Cada módulo mantém sua própria entidade de análise. Não existe uma tabela
polimórfica central: o módulo de LLA-B usa `LeukemiaAnalysis` e o módulo renal
usa `RenalAnalysis`.

## Limites da primeira entrega

- o sistema recebe imagens ou regiões de interesse, não WSI;
- o classificador de LLA-B recebe uma célula já recortada;
- não haverá segmentação celular antes da classificação nesta etapa;
- os resultados têm finalidade experimental e não representam diagnóstico clínico.

## Fluxo implementado para LLA-B

1. a API recebe o upload de uma imagem celular;
2. o arquivo é validado e convertido para RGB;
3. a imagem é redimensionada para `224 × 224` e mantida no intervalo
   `0–255`, pois a EfficientNet-B0 possui reescala interna;
4. o modelo é carregado uma única vez por processo;
5. o score de malignidade é comparado ao threshold configurado;
6. o resultado e o tempo de inferência são registrados em
   `LeukemiaAnalysis`;
7. a API retorna classe, scores e aviso de uso experimental.

## Fluxo implementado para segmentação renal

1. a API recebe um recorte histológico renal;
2. o arquivo é validado, convertido para RGB e redimensionado para `224 x 224`;
3. os pixels são convertidos para `float32` e divididos por 255;
4. a U-Net/VGG-19 é reconstruída e o fold configurado é carregado uma única vez por processo;
5. a saída probabilística é convertida em máscara binária com threshold 0,5;
6. são gerados máscara PNG e overlay vermelho;
7. entrada, artefatos e metadados são registrados em `RenalAnalysis`;
8. a API retorna URLs, cobertura, fold e tempo de inferência.

Os detalhes metodológicos e as limitações estão registrados em
[`renal_integration.md`](renal_integration.md).
