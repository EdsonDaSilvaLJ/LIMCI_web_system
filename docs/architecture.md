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
| PostgreSQL | Metadados das análises e resultados estruturados |

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
6. o resultado e o tempo de inferência são registrados em `Analysis`;
7. a API retorna classe, scores e aviso de uso experimental.
