import { useEffect, useMemo, useRef, useState } from "react";

import { classifyLeukemia, fetchModules } from "./services/api";
import type { AnalysisModule, LeukemiaPrediction } from "./types";

const MAX_FILE_SIZE = 10 * 1024 * 1024;
const ACCEPTED_EXTENSIONS = ["bmp", "png", "jpg", "jpeg"];

function formatPercent(value: number) {
  return new Intl.NumberFormat("pt-BR", {
    style: "percent",
    maximumFractionDigits: 1,
  }).format(value);
}

function formatTime(milliseconds: number) {
  return milliseconds < 1000
    ? `${milliseconds.toFixed(0)} ms`
    : `${(milliseconds / 1000).toFixed(2)} s`;
}

function App() {
  const [modules, setModules] = useState<AnalysisModule[]>([]);
  const [modulesError, setModulesError] = useState("");
  const [activeModule, setActiveModule] = useState<string | null>(null);
  const [file, setFile] = useState<File | null>(null);
  const [result, setResult] = useState<LeukemiaPrediction | null>(null);
  const [error, setError] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const previewUrl = useMemo(
    () => (file ? URL.createObjectURL(file) : null),
    [file],
  );

  useEffect(() => {
    fetchModules()
      .then(setModules)
      .catch((requestError: Error) => setModulesError(requestError.message));
  }, []);

  useEffect(
    () => () => {
      if (previewUrl) URL.revokeObjectURL(previewUrl);
    },
    [previewUrl],
  );

  function selectFile(selectedFile?: File) {
    setError("");
    setResult(null);

    if (!selectedFile) return;

    const extension = selectedFile.name.split(".").pop()?.toLowerCase() ?? "";
    if (!ACCEPTED_EXTENSIONS.includes(extension)) {
      setFile(null);
      setError("Escolha uma imagem BMP, PNG, JPG ou JPEG.");
      return;
    }

    if (selectedFile.size > MAX_FILE_SIZE) {
      setFile(null);
      setError("A imagem deve possuir no máximo 10 MB.");
      return;
    }

    setFile(selectedFile);
  }

  async function submitAnalysis() {
    if (!file) {
      setError("Selecione uma imagem celular antes de analisar.");
      return;
    }

    setError("");
    setIsSubmitting(true);

    try {
      setResult(await classifyLeukemia(file));
    } catch (requestError) {
      setError(
        requestError instanceof Error
          ? requestError.message
          : "Não foi possível processar a imagem.",
      );
    } finally {
      setIsSubmitting(false);
    }
  }

  function resetAnalysis() {
    setFile(null);
    setResult(null);
    setError("");
    if (fileInputRef.current) fileInputRef.current.value = "";
  }

  const leukemiaModule = modules.find((module) => module.slug === "leukemia");

  return (
    <div className="app-shell">
      <header className="site-header">
        <a className="brand" href="#inicio" onClick={() => setActiveModule(null)}>
          <span className="brand-mark" aria-hidden="true">LI</span>
          <span>
            <strong>LIMCI</strong>
            <small>análise computacional de imagens</small>
          </span>
        </a>
        <span className="research-badge">Iniciação Tecnológica · UFPI</span>
      </header>

      <main id="inicio">
        {activeModule !== "leukemia" ? (
          <ModulesPage
            modulesError={modulesError}
            leukemiaAvailable={leukemiaModule?.status === "available"}
            onSelectLeukemia={() => setActiveModule("leukemia")}
          />
        ) : (
          <section className="analysis-page">
            <button className="back-button" type="button" onClick={() => setActiveModule(null)}>
              ← Voltar aos módulos
            </button>

            <div className="analysis-heading">
              <p className="eyebrow">CLASSIFICAÇÃO · LLA-B</p>
              <h1>Análise de célula sanguínea</h1>
              <p>Envie uma imagem de uma única célula, já recortada da lâmina.</p>
            </div>

            <div className="analysis-layout">
              <div className="upload-panel">
                <label className={`drop-zone ${file ? "has-file" : ""}`}>
                  <input
                    ref={fileInputRef}
                    type="file"
                    accept=".bmp,.png,.jpg,.jpeg,image/bmp,image/png,image/jpeg"
                    onChange={(event) => selectFile(event.target.files?.[0])}
                  />
                  {previewUrl ? (
                    <img src={previewUrl} alt="Pré-visualização da célula selecionada" />
                  ) : (
                    <>
                      <span className="upload-symbol" aria-hidden="true">↑</span>
                      <strong>Selecione uma imagem celular</strong>
                      <span>BMP, PNG ou JPEG · máximo de 10 MB</span>
                    </>
                  )}
                </label>

                {file && (
                  <div className="file-row">
                    <span>
                      <strong>{file.name}</strong>
                      <small>{(file.size / 1024).toFixed(1)} KB</small>
                    </span>
                    <button type="button" onClick={resetAnalysis}>Remover</button>
                  </div>
                )}

                {error && <p className="inline-error" role="alert">{error}</p>}

                <button
                  className="primary-button analyze-button"
                  type="button"
                  disabled={!file || isSubmitting}
                  onClick={submitAnalysis}
                >
                  {isSubmitting ? "Processando…" : "Executar análise experimental"}
                </button>
              </div>

              <ResultPanel result={result} onReset={resetAnalysis} />
            </div>
          </section>
        )}
      </main>

      <footer>
        <strong>Uso exclusivamente experimental.</strong>
        <span>O resultado não substitui avaliação profissional ou diagnóstico clínico.</span>
      </footer>
    </div>
  );
}

function ModulesPage({
  modulesError,
  leukemiaAvailable,
  onSelectLeukemia,
}: {
  modulesError: string;
  leukemiaAvailable: boolean;
  onSelectLeukemia: () => void;
}) {
  return (
    <>
      <section className="hero">
        <p className="eyebrow">PLATAFORMA EXPERIMENTAL MODULAR</p>
        <h1>Modelos de visão computacional em uma interface acessível.</h1>
        <p className="hero-copy">
          Uma prova de conceito para integrar tarefas distintas de análise de
          imagens patológicas sem misturar seus dados e resultados.
        </p>
      </section>

      <section className="modules-section" aria-labelledby="modules-title">
        <div className="section-heading">
          <div>
            <p className="eyebrow">MÓDULOS</p>
            <h2 id="modules-title">Escolha uma análise</h2>
          </div>
          <span className="api-state">
            <i className={modulesError ? "offline" : "online"} />
            {modulesError ? "API indisponível" : "API conectada"}
          </span>
        </div>

        {modulesError && <p className="inline-error">{modulesError}</p>}

        <div className="module-grid">
          <article className="module-card available-card">
            <div className="module-icon blood-icon" aria-hidden="true">●</div>
            <div className="module-meta">
              <span>CLASSIFICAÇÃO</span>
              <span className="status available">Disponível</span>
            </div>
            <h3>Leucemia LLA-B</h3>
            <p>
              Classificação binária de uma célula sanguínea previamente
              recortada em normal ou maligna.
            </p>
            <button
              className="primary-button"
              type="button"
              disabled={!leukemiaAvailable}
              onClick={onSelectLeukemia}
            >
              Iniciar análise <span aria-hidden="true">→</span>
            </button>
          </article>

          <article className="module-card pending-card">
            <div className="module-icon renal-icon" aria-hidden="true">◒</div>
            <div className="module-meta">
              <span>SEGMENTAÇÃO</span>
              <span className="status pending">Em integração</span>
            </div>
            <h3>Estruturas renais</h3>
            <p>
              Segmentação glomerular com U-Net/VGG-19 para geração de máscara
              e sobreposição.
            </p>
            <button className="secondary-button" type="button" disabled>
              Integração pendente
            </button>
          </article>
        </div>
      </section>
    </>
  );
}

function ResultPanel({
  result,
  onReset,
}: {
  result: LeukemiaPrediction | null;
  onReset: () => void;
}) {
  return (
    <aside className="result-panel" aria-live="polite">
      {result ? (
        <>
          <p className="eyebrow">RESULTADO DO MODELO</p>
          <div className={`result-label ${result.predicted_class}`}>
            <span aria-hidden="true">{result.predicted_class === "malignant" ? "!" : "✓"}</span>
            <div>
              <small>Classe prevista</small>
              <strong>
                {result.predicted_class === "malignant"
                  ? "Padrão maligno"
                  : "Padrão normal"}
              </strong>
            </div>
          </div>

          <div className="score-list">
            <ScoreBar label="Score maligno" value={result.malignant_score} tone="malignant" />
            <ScoreBar label="Score normal" value={result.normal_score} tone="normal" />
          </div>

          <dl className="result-details">
            <div><dt>Threshold</dt><dd>{result.threshold.toFixed(2)}</dd></div>
            <div><dt>Inferência</dt><dd>{formatTime(result.inference_time_ms)}</dd></div>
            <div><dt>ID da análise</dt><dd>{result.analysis_id.slice(0, 8)}…</dd></div>
          </dl>

          <button className="secondary-button" type="button" onClick={onReset}>
            Analisar outra imagem
          </button>
        </>
      ) : (
        <div className="empty-result">
          <span aria-hidden="true">◎</span>
          <h2>O resultado aparecerá aqui</h2>
          <p>Os dois scores serão exibidos após o processamento.</p>
        </div>
      )}
    </aside>
  );
}

function ScoreBar({
  label,
  value,
  tone,
}: {
  label: string;
  value: number;
  tone: "malignant" | "normal";
}) {
  return (
    <div className="score-item">
      <div><span>{label}</span><strong>{formatPercent(value)}</strong></div>
      <div className="score-track">
        <span className={tone} style={{ width: `${value * 100}%` }} />
      </div>
    </div>
  );
}

export default App;
