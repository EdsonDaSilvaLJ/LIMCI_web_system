# Frontend

Interface React + TypeScript da prova de conceito.

## Execução local

Com o backend disponível em `http://127.0.0.1:8000`:

```bash
npm install
npm run dev
```

Abra `http://127.0.0.1:5173`. Durante o desenvolvimento, o Vite encaminha
requisições iniciadas por `/api` para o backend Django.

## Escopo atual

- catálogo de módulos obtido pela API;
- upload e pré-visualização de imagem celular;
- classificação experimental de LLA-B;
- apresentação dos scores e do tempo de inferência;
- módulo renal identificado como integração pendente.

O frontend não apresenta o resultado como diagnóstico clínico.
