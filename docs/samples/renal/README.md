# Amostras para teste funcional do módulo renal

As três amostras representam as colorações histológicas usadas no trabalho original:

| Arquivo | Coloração | Dimensão extraída |
|---|---|---:|
| `renal_sample_he.jpg` | HE | 291 x 203 |
| `renal_sample_pams.jpg` | PAMS | 272 x 205 |
| `renal_sample_pas.jpg` | PAS | 272 x 205 |

Por restrição de redistribuição, as imagens não são versionadas neste repositório. Elas podem ser extraídas da Figura 1 do relatório final de Débora Barros do Nascimento, *Segmentação da região glomerular em lâminas de exames patológicos do rim*. O relatório informa que a base original foi fornecida pelo Instituto Oswaldo Cruz (Fiocruz).

## Gerar as amostras no Google Colab

Execute a célula abaixo e selecione o PDF do relatório quando solicitado. O código extrai somente as três imagens histológicas da página que contém a Figura 1 e cria os arquivos dentro de `docs/samples/renal/`.

```python
!pip -q install pymupdf

from pathlib import Path

import fitz
from google.colab import files

uploaded = files.upload()
pdf_name = next(iter(uploaded))

output_dir = Path("docs/samples/renal")
output_dir.mkdir(parents=True, exist_ok=True)

document = fitz.open(stream=uploaded[pdf_name], filetype="pdf")
page = document[2]  # página 3 do PDF: Figura 1

names = [
    "renal_sample_he.jpg",
    "renal_sample_pams.jpg",
    "renal_sample_pas.jpg",
]

samples = []

for image_info in page.get_images(full=True):
    xref = image_info[0]
    extracted = document.extract_image(xref)
    width = extracted["width"]
    height = extracted["height"]

    # Descarta logotipos e mantém somente HE, PAMS e PAS.
    if width >= 250 and height >= 180:
        samples.append(extracted)

assert len(samples) == 3, (
    f"Esperadas 3 amostras na Figura 1; encontradas {len(samples)}."
)

for name, sample in zip(names, samples):
    destination = output_dir / name
    destination.write_bytes(sample["image"])
    print(name, sample["width"], "x", sample["height"])

document.close()
```

Uso recomendado: validar upload, pré-processamento, inferência, máscara e overlay na prova de conceito. Esses arquivos possuem resolução reduzida por terem sido extraídos do PDF e não devem ser usados para recalcular ou reivindicar as métricas do estudo original.

Exemplo de teste direto da API:

```bash
curl -X POST \
  -F "file=@docs/samples/renal/renal_sample_he.jpg" \
  http://127.0.0.1:8000/api/v1/modules/renal/segment
```
