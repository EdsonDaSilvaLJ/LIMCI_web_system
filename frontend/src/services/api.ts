import type { AnalysisModule, LeukemiaPrediction } from "../types";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "";

async function readJson<T>(response: Response): Promise<T> {
  const payload = await response.json().catch(() => null);

  if (!response.ok) {
    const detail = payload?.detail;
    throw new Error(
      typeof detail === "string"
        ? detail
        : "Não foi possível concluir a solicitação.",
    );
  }

  return payload as T;
}

export async function fetchModules(): Promise<AnalysisModule[]> {
  const response = await fetch(`${API_BASE_URL}/api/v1/modules`);
  return readJson<AnalysisModule[]>(response);
}

export async function classifyLeukemia(
  image: File,
): Promise<LeukemiaPrediction> {
  const body = new FormData();
  body.append("file", image);

  const response = await fetch(
    `${API_BASE_URL}/api/v1/modules/leukemia/predict`,
    { method: "POST", body },
  );

  return readJson<LeukemiaPrediction>(response);
}
