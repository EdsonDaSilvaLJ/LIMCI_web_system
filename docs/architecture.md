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
