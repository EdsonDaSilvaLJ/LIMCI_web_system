# Integração do módulo de segmentação renal

## Finalidade deste registro

Este documento registra as decisões, evidências e etapas técnicas usadas para integrar à plataforma LIMCI um modelo de segmentação glomerular. O texto foi organizado para servir como memória de implementação e como base para a futura redação do relatório da Iniciação Tecnológica.

## Escopo científico

O módulo recebe um recorte de tecido renal contendo uma região glomerular e produz uma máscara semântica binária. Ele localiza os pixels associados ao glomérulo, mas não classifica glomerulopatias, não determina se a estrutura é normal ou patológica e não processa uma WSI completa.

```text
Recorte renal -> RGB -> 224 x 224 -> normalização [0, 1]
              -> U-Net/VGG-19 -> máscara probabilística
              -> threshold 0,5 -> máscara binária e overlay
```

## Origem do modelo

Os pesos e os resultados experimentais são provenientes do trabalho de Débora Barros do Nascimento, intitulado *Segmentação da região glomerular em lâminas de exames patológicos do rim*, desenvolvido no LIMCI/UFPI sob orientação de Rodrigo de Melo Souza Veras.

O estudo original utilizou 45 imagens digitais fornecidas pelo Instituto Oswaldo Cruz (Fiocruz), nas colorações HE, PAMS e PAS. Foram produzidos 643 recortes de `1024 x 768` pixels, posteriormente redimensionados para `224 x 224`. A avaliação empregou validação cruzada estratificada com cinco folds.

No estudo original, a U-Net com backbone VGG-19 obteve, como média dos cinco folds:

| Métrica | Resultado original |
|---|---:|
| Dice | 95,45% ± 0,57% |
| Sensibilidade | 94,80% ± 0,94% |
| Especificidade | 98,83% ± 0,23% |
| Acurácia | 97,91% ± 0,15% |

Esses números não são resultados reproduzidos pela presente integração. Eles devem ser atribuídos ao trabalho original e não a um fold isolado.

## Inspeção dos arquivos de pesos

Foram disponibilizados cinco arquivos, `modelo_fold1.h5` a `modelo_fold5.h5`. A inspeção com `h5py` mostrou que os arquivos não possuem o atributo `model_config`; portanto, contêm pesos, mas não um modelo Keras completo.

Os cinco arquivos apresentam os mesmos grupos de camadas:

- encoder VGG-19, de `block1_conv1` a `block5_conv4`;
- quatro camadas `Conv2DTranspose`;
- quatro concatenações;
- quatro camadas `Dropout`;
- oito convoluções no decodificador e a saída `conv2d_8`.

A arquitetura de inferência foi reconstruída como uma U-Net com encoder VGG-19. Os cinco arquivos carregaram integralmente por meio de `load_weights()`:

| Fold | Entrada | Saída | Parâmetros | Compatível |
|---:|---|---|---:|---|
| 1 | `(None, 224, 224, 3)` | `(None, 224, 224, 1)` | 21.505.313 | Sim |
| 2 | `(None, 224, 224, 3)` | `(None, 224, 224, 1)` | 21.505.313 | Sim |
| 3 | `(None, 224, 224, 3)` | `(None, 224, 224, 1)` | 21.505.313 | Sim |
| 4 | `(None, 224, 224, 3)` | `(None, 224, 224, 1)` | 21.505.313 | Sim |
| 5 | `(None, 224, 224, 3)` | `(None, 224, 224, 1)` | 21.505.313 | Sim |

O carregamento comprova compatibilidade estrutural das camadas com pesos. Ele não recupera, sozinho, detalhes externos ao arquivo, como o pré-processamento, o threshold ou as métricas individuais.

## Escolha operacional do fold

O `fold 1` é usado provisoriamente na prova de conceito. Essa escolha não significa que ele apresentou o melhor desempenho; foi adotado como modelo operacional porque não foram identificadas métricas individuais que justificassem a seleção de outro fold.

Se as métricas individuais ou as máscaras de referência se tornarem disponíveis, os cinco modelos deverão ser comparados e a configuração deverá ser atualizada. Outra alternativa futura é calcular a média das máscaras dos cinco folds, avaliando antes o custo adicional de inferência.

Redação recomendada para o relatório:

> Para a validação funcional da integração, empregou-se provisoriamente o modelo correspondente ao primeiro fold da validação cruzada. Essa escolha não representa superioridade de desempenho. Os resultados quantitativos reportados para a U-Net/VGG-19 correspondem à média dos cinco folds no estudo original.

## Implementação no backend

O módulo foi mantido independente do classificador de leucemia:

```text
backend/apps/renal/
├── api.py                 endpoint Django Ninja
├── inference.py           predição, threshold, máscara e overlay
├── model_architecture.py  reconstrução da U-Net/VGG-19
├── model_loader.py        carregamento lazy e cache do fold
├── models.py              persistência de RenalAnalysis
├── preprocessing.py       RGB, resize bilinear e divisão por 255
├── schemas.py             contrato de resposta
├── services.py            armazenamento dos artefatos
└── tests/                 testes unitários e de API
```

O modelo é carregado uma única vez por processo. A API recebe `multipart/form-data` em `POST /api/v1/modules/renal/segment`, persiste a entrada, a máscara e o overlay, e retorna:

- identificador da análise;
- URLs da máscara e do overlay;
- cobertura segmentada;
- média da máscara probabilística;
- threshold;
- fold operacional;
- tempo de inferência;
- indicação de uso experimental.

Os valores de cobertura e probabilidade média não representam probabilidade de doença. A cobertura é apenas a proporção dos pixels classificados como região glomerular.

## Integração no frontend

A tela React consulta a disponibilidade do peso renal, aceita o upload do recorte e apresenta a máscara binária, o overlay, a cobertura e os metadados da inferência. O módulo só fica disponível quando o arquivo indicado por `RENAL_MODEL_PATH` existe no backend.

## Configuração reproduzível

```env
RENAL_MODEL_PATH=../model_weights/renal/modelo_fold1.h5
RENAL_MODEL_FOLD=1
RENAL_THRESHOLD=0.5
```

Depois de colocar o peso no caminho configurado:

```bash
cd backend
python manage.py migrate
python manage.py runserver
```

Em outro terminal:

```bash
cd frontend
npm install
npm run dev
```

## Limitações e próximos experimentos

- as amostras incluídas no repositório são figuras extraídas do relatório e servem somente para teste funcional;
- a integração ainda não reproduziu o Dice com máscaras de referência;
- o fold operacional não foi escolhido por comparação quantitativa individual;
- a imagem é redimensionada para `224 x 224`, portanto a máscara persistida possui essa resolução;
- o pipeline espera um recorte renal e não uma WSI;
- é necessário testar o peso real no mesmo ambiente TensorFlow usado em produção;
- uma avaliação futura deve usar imagens e máscaras verdadeiras não utilizadas no treinamento.

## Separação das contribuições

- **Trabalho de Nascimento:** base de imagens, treinamento, validação cruzada, pesos e resultados originais.
- **Presente Iniciação Tecnológica:** inspeção dos pesos, reconstrução compatível da arquitetura de inferência, integração Django Ninja/React, persistência, documentação e testes funcionais.
