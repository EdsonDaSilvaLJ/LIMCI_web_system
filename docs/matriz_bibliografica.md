# Matriz bibliográfica da I.T.

Esta matriz registra a função de cada trabalho no relatório. Os resultados da literatura não devem ser apresentados como resultados produzidos neste projeto.

| Trabalho | Eixo | Evidência principal | Uso no relatório | Pontos a confirmar |
|---|---|---|---|---|
| Nascimento et al. — *Segmentation of the Glomerular Region in Pathological Kidney Slides* | Segmentação renal | Avalia U-Net e Sharp U-Net com backbones pré-treinados em 643 imagens renais e validação cruzada | Fundamentação e descrição da origem do módulo renal | Registrar páginas das métricas, limitações e melhor configuração |
| Niazi et al. — *Digital Pathology and Artificial Intelligence* | Patologia digital | Discute digitalização, WSI, aplicação de IA e desafios de integração clínica | Introdução, justificativa e limitações | Registrar páginas sobre supervisão humana e implantação |
| Tajbakhsh et al. — *Convolutional Neural Networks for Medical Image Analysis: Full Training or Fine Tuning?* | Transferência de aprendizado | Compara treinamento do zero e ajuste de redes pré-treinadas em tarefas médicas | Justificar VGG-19 e EfficientNet-B0 pré-treinadas | Registrar páginas das conclusões e limitações |
| Vogado et al. — *Diagnosing Leukemia in Blood Smear Images Using an Ensemble of Classifiers and Pre-Trained CNNs* | Classificação de leucemia | Emprega redes pré-treinadas e classificadores para imagens de esfregaço sanguíneo | Trabalhos relacionados e justificativa do segundo módulo | Confirmar dataset, divisão experimental e métricas |
| Chen et al. — *Classifying Microscopic Images as Acute Lymphoblastic Leukemia by ResNet Ensemble Model* | C-NMC 2019 | Aplica transfer learning à classificação de células normais e malignas da C-NMC | Comparação metodológica e discussão dos resultados | Registrar protocolo exato, métricas e análise dos erros |
| Loey et al. — *Deep Transfer Learning in Diagnosing Leukemia in Blood Cells* | Transferência em leucemia | Explora estratégias de transferência de aprendizado para classificação de células sanguíneas | Justificar backbone congelado seguido de fine-tuning | Confirmar dataset, augmentation, métricas e limitações |

## Síntese das leituras de 22/08

As leituras sustentam três decisões do projeto:

1. **Utilizar dados públicos:** a C-NMC 2019 oferece quantidade de imagens e identificação por indivíduos adequadas para uma prova de conceito reproduzível.
2. **Separar os dados por pacientes:** imagens do mesmo indivíduo não podem aparecer em treino, validação e teste, pois isso produziria uma avaliação excessivamente otimista.
3. **Utilizar transferência de aprendizado:** o backbone EfficientNet-B0 será iniciado com pesos da ImageNet, treinando primeiro a cabeça classificadora e realizando posteriormente fine-tuning parcial.

## Relação com a aplicação

- O módulo renal reutiliza um modelo de segmentação derivado do trabalho de Nascimento et al.
- O novo módulo de LLA-B realizará somente classificação binária de células previamente recortadas.
- Não haverá segmentação celular nem processamento de WSI na primeira entrega.
- O resultado do classificador será experimental: classe prevista, confiança e probabilidades, sem alegação de diagnóstico clínico.

## Dados auditados da C-NMC 2019

| Conjunto | Origem | Imagens | Pacientes |
|---|---|---:|---:|
| Treinamento | folds 0 e 1 | 7.108 | 42 |
| Validação | fold 2 | 3.553 | 31 |
| Teste | teste preliminar | 1.867 | 28 |

A auditoria automatizada confirmou zero pacientes compartilhados entre os três conjuntos.
