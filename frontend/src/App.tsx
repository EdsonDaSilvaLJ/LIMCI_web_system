import { useEffect, useMemo, useRef, useState } from "react";

import { classifyLeukemia, fetchModules, segmentRenalImage } from "./services/api";
import type { AnalysisModule, LeukemiaPrediction, RenalSegmentation } from "./types";

const MAX_FILE_SIZE = 10 * 1024 * 1024;
const ACCEPTED_EXTENSIONS = ["bmp", "png", "jpg", "jpeg"];
type ModuleSlug = "leukemia" | "renal";

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
  const [activeModule, setActiveModule] = useState<ModuleSlug | null>(null);
  const [file, setFile] = useState<File | null>(null);
  const [leukemiaResult, setLeukemiaResult] = useState<LeukemiaPrediction | null>(null);
  const [renalResult, setRenalResult] = useState<RenalSegmentation | null>(null);
  const [error, setError] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const previewUrl = useMemo(() => (file ? URL.createObjectURL(file) : null), [file]);

  useEffect(() => {
    fetchModules().then(setModules).catch((requestError: Error) => {
      setModulesError(requestError.message);
    });
  }, []);

  useEffect(() => () => {
    if (previewUrl) URL.revokeObjectURL(previewUrl);
  }, [previewUrl]);

  function resetAnalysis() {
    setFile(null);
    setLeukemiaResult(null);
    setRenalResult(null);
    setError("");
    if (fileInputRef.current) fileInputRef.current.value = "";
  }

  function openModule(slug: ModuleSlug) {
    resetAnalysis();
    setActiveModule(slug);
  }

  function selectFile(selectedFile?: File) {
    setError("");
    setLeukemiaResult(null);
    setRenalResult(null);
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
    if (!file || !activeModule) {
      setError("Selecione uma imagem antes de analisar.");
      return;
    }

    setError("");
    setIsSubmitting(true);
    try {
      if (activeModule === "leukemia") {
        setLeukemiaResult(await classifyLeukemia(file));
      } else {
        setRenalResult(await segmentRenalImage(file));
      }
    } catch (requestError) {
      setError(requestError instanceof Error
        ? requestError.message
        : "Não foi possível processar a imagem.");
    } finally {
      setIsSubmitting(false);
    }
  }

  const availability = Object.fromEntries(
    modules.map((module) => [module.slug, module.status === "available"]),
  );
  const renalActive = activeModule === "renal";

  return (
    <div className="app-shell">
      <header className="site-header">
        <a className="brand" href="#inicio" onClick={() => setActiveModule(null)}>
          <span className="brand-mark" aria-hidden="true">LI</span>
          <span><strong>LIMCI</strong><small>análise computacional de imagens</small></span>
        </a>
        <span className="research-badge">Iniciação Tecnológica · UFPI</span>
      </header>

      <main id="inicio">
        {!activeModule ? (
          <ModulesPage
            modulesError={modulesError}
            leukemiaAvailable={Boolean(availability.leukemia)}
            renalAvailable={Boolean(availability.renal)}
            onSelect={openModule}
          />
        ) : (
          <section className="analysis-page">
            <button className="back-button" type="button" onClick={() => setActiveModule(null)}>
              ← Voltar aos módulos
            </button>
            <div className="analysis-heading">
              <p className="eyebrow">{renalActive ? "SEGMENTAÇÃO · GLOMÉRULO" : "CLASSIFICAÇÃO · LLA-B"}</p>
              <h1>{renalActive ? "Segmentação de estrutura renal" : "Análise de célula sanguínea"}</h1>
              <p>{renalActive
                ? "Envie um recorte histológico renal contendo uma região glomerular."
                : "Envie uma imagem de uma única célula, já recortada da lâmina."}</p>
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
                    <img src={previewUrl} alt="Pré-visualização da imagem selecionada" />
                  ) : (
                    <>
                      <span className="upload-symbol" aria-hidden="true">↑</span>
                      <strong>{renalActive ? "Selecione um recorte renal" : "Selecione uma imagem celular"}</strong>
                      <span>BMP, PNG ou JPEG · máximo de 10 MB</span>
                    </>
                  )}
                </label>
                {file && (
                  <div className="file-row">
                    <span><strong>{file.name}</strong><small>{(file.size / 1024).toFixed(1)} KB</small></span>
                    <button type="button" onClick={resetAnalysis}>Remover</button>
                  </div>
                )}
                {error && <p className="inline-error" role="alert">{error}</p>}
                <button className="primary-button analyze-button" type="button" disabled={!file || isSubmitting} onClick={submitAnalysis}>
                  {isSubmitting ? "Processando…" : "Executar análise experimental"}
                </button>
              </div>

              {renalActive
                ? <RenalResultPanel result={renalResult} onReset={resetAnalysis} />
                : <LeukemiaResultPanel result={leukemiaResult} onReset={resetAnalysis} />}
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

function ModulesPage({ modulesError, leukemiaAvailable, renalAvailable, onSelect }: {
  modulesError: string;
  leukemiaAvailable: boolean;
  renalAvailable: boolean;
  onSelect: (slug: ModuleSlug) => void;
}) {
  return (
    <>
      <section className="hero">
        <p className="eyebrow">PLATAFORMA EXPERIMENTAL MODULAR</p>
        <h1>Modelos de visão computacional em uma interface acessível.</h1>
        <p className="hero-copy">Uma prova de conceito para integrar tarefas distintas de análise de imagens patológicas sem misturar seus dados e resultados.</p>
      </section>
      <section className="modules-section" aria-labelledby="modules-title">
        <div className="section-heading">
          <div><p className="eyebrow">MÓDULOS</p><h2 id="modules-title">Escolha uma análise</h2></div>
          <span className="api-state"><i className={modulesError ? "offline" : "online"} />{modulesError ? "API indisponível" : "API conectada"}</span>
        </div>
        {modulesError && <p className="inline-error">{modulesError}</p>}
        <div className="module-grid">
          <ModuleCard icon="●" iconClass="blood-icon" task="CLASSIFICAÇÃO" available={leukemiaAvailable} title="Leucemia LLA-B" description="Classificação binária de uma célula sanguínea previamente recortada em normal ou maligna." onClick={() => onSelect("leukemia")} />
          <ModuleCard icon="◒" iconClass="renal-icon" task="SEGMENTAÇÃO" available={renalAvailable} title="Estruturas renais" description="Segmentação glomerular com U-Net/VGG-19 para geração de máscara e sobreposição." onClick={() => onSelect("renal")} />
        </div>
      </section>
    </>
  );
}

function ModuleCard({ icon, iconClass, task, available, title, description, onClick }: {
  icon: string;
  iconClass: string;
  task: string;
  available: boolean;
  title: string;
  description: string;
  onClick: () => void;
}) {
  return (
    <article className={`module-card ${available ? "available-card" : "pending-card"}`}>
      <div className={`module-icon ${iconClass}`} aria-hidden="true">{icon}</div>
      <div className="module-meta"><span>{task}</span><span className={`status ${available ? "available" : "pending"}`}>{available ? "Disponível" : "Modelo ausente"}</span></div>
      <h3>{title}</h3><p>{description}</p>
      <button className={available ? "primary-button" : "secondary-button"} type="button" disabled={!available} onClick={onClick}>
        {available ? <>Iniciar análise <span aria-hidden="true">→</span></> : "Integração indisponível"}
      </button>
    </article>
  );
}

function LeukemiaResultPanel({ result, onReset }: { result: LeukemiaPrediction | null; onReset: () => void }) {
  return (
    <aside className="result-panel" aria-live="polite">
      {result ? <>
        <p className="eyebrow">RESULTADO DO MODELO</p>
        <div className={`result-label ${result.predicted_class}`}><span aria-hidden="true">{result.predicted_class === "malignant" ? "!" : "✓"}</span><div><small>Classe prevista</small><strong>{result.predicted_class === "malignant" ? "Padrão maligno" : "Padrão normal"}</strong></div></div>
        <div className="score-list"><ScoreBar label="Score maligno" value={result.malignant_score} tone="malignant" /><ScoreBar label="Score normal" value={result.normal_score} tone="normal" /></div>
        <ResultDetails threshold={result.threshold} time={result.inference_time_ms} id={result.analysis_id} />
        <button className="secondary-button" type="button" onClick={onReset}>Analisar outra imagem</button>
      </> : <EmptyResult text="Os dois scores serão exibidos após o processamento." />}
    </aside>
  );
}

function RenalResultPanel({ result, onReset }: { result: RenalSegmentation | null; onReset: () => void }) {
  return (
    <aside className="result-panel renal-result-panel" aria-live="polite">
      {result ? <>
        <p className="eyebrow">RESULTADO DA SEGMENTAÇÃO</p>
        <div className="renal-images">
          <figure><img src={result.mask_url} alt="Máscara binária do glomérulo" /><figcaption>Máscara binária</figcaption></figure>
          <figure><img src={result.overlay_url} alt="Máscara sobreposta ao recorte renal" /><figcaption>Sobreposição</figcaption></figure>
        </div>
        <dl className="result-details">
          <div><dt>Cobertura segmentada</dt><dd>{formatPercent(result.mask_coverage)}</dd></div>
          <div><dt>Probabilidade média</dt><dd>{formatPercent(result.mask_mean)}</dd></div>
          <div><dt>Threshold</dt><dd>{result.threshold.toFixed(2)}</dd></div>
          <div><dt>Modelo operacional</dt><dd>Fold {result.fold}</dd></div>
          <div><dt>Inferência</dt><dd>{formatTime(result.inference_time_ms)}</dd></div>
          <div><dt>ID da análise</dt><dd>{result.analysis_id.slice(0, 8)}…</dd></div>
        </dl>
        <button className="secondary-button" type="button" onClick={onReset}>Analisar outra imagem</button>
      </> : <EmptyResult text="A máscara e a sobreposição aparecerão após o processamento." />}
    </aside>
  );
}

function EmptyResult({ text }: { text: string }) {
  return <div className="empty-result"><span aria-hidden="true">◎</span><h2>O resultado aparecerá aqui</h2><p>{text}</p></div>;
}

function ResultDetails({ threshold, time, id }: { threshold: number; time: number; id: string }) {
  return <dl className="result-details"><div><dt>Threshold</dt><dd>{threshold.toFixed(2)}</dd></div><div><dt>Inferência</dt><dd>{formatTime(time)}</dd></div><div><dt>ID da análise</dt><dd>{id.slice(0, 8)}…</dd></div></dl>;
}

function ScoreBar({ label, value, tone }: { label: string; value: number; tone: "malignant" | "normal" }) {
  return <div className="score-item"><div><span>{label}</span><strong>{formatPercent(value)}</strong></div><div className="score-track"><span className={tone} style={{ width: `${value * 100}%` }} /></div></div>;
}

export default App;
