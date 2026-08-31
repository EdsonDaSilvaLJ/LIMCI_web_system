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
          <span className="brand-mark" aria-hidden="true">
            <svg viewBox="0 0 32 32"><path d="M8 7.5h5.5v17H8zM18.5 7.5H24v17h-5.5zM13.5 13.25h5v5.5h-5z" /></svg>
          </span>
          <span><strong>LIMCI</strong><small>apoio à análise anatomopatológica</small></span>
        </a>
        <div className="header-meta">
          <span className="header-status"><i />Sistema experimental</span>
          <span className="research-badge">Iniciação Tecnológica · UFPI</span>
        </div>
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
              <p className="eyebrow">{renalActive ? "MÓDULO RIM · SEGMENTAÇÃO" : "MÓDULO LEUCEMIA LLA-B · CLASSIFICAÇÃO"}</p>
              <h1>{renalActive ? "Módulo Rim" : "Módulo Leucemia LLA-B"}</h1>
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
                  {isSubmitting ? "Processando…" : "Processar imagem"}
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
        <div className="hero-content">
          <p className="eyebrow">PLATAFORMA EXPERIMENTAL · LIMCI</p>
          <h1>Aplicação LIMCI</h1>
          <p className="hero-subtitle">Sistema de Apoio a Patologistas por Meio da Análise Automatizada de Imagens</p>
          <p className="hero-copy">Recursos computacionais organizados em módulos especializados para apoiar a avaliação de imagens anatomopatológicas.</p>
          <a className="hero-link" href="#modulos">Conhecer os módulos <span aria-hidden="true">↓</span></a>
        </div>
        <div className="hero-visual" aria-hidden="true">
          <div className="visual-grid" />
          <div className="sample sample-one"><span /></div>
          <div className="sample sample-two"><span /><i /></div>
          <div className="focus-ring"><span>2</span><small>módulos<br />especializados</small></div>
          <span className="visual-caption">IMAGEM · ESTRUTURA · EVIDÊNCIA</span>
        </div>
      </section>
      <section className="modules-section" id="modulos" aria-labelledby="modules-title">
        <div className="section-heading">
          <div><p className="eyebrow">ÁREAS DE PROCESSAMENTO</p><h2 id="modules-title">Escolha um módulo</h2><p>Selecione a área correspondente ao tipo de imagem que deseja processar.</p></div>
          <span className="api-state"><i className={modulesError ? "offline" : "online"} />{modulesError ? "API indisponível" : "API conectada"}</span>
        </div>
        {modulesError && <p className="inline-error">{modulesError}</p>}
        <div className="module-grid">
          <ModuleCard icon="blood" iconClass="blood-icon" task="CLASSIFICAÇÃO CELULAR" number="01" available={leukemiaAvailable} title="Módulo Leucemia LLA-B" description="Classificação binária de uma célula sanguínea previamente recortada em padrão normal ou maligno." onClick={() => onSelect("leukemia")} />
          <ModuleCard icon="renal" iconClass="renal-icon" task="SEGMENTAÇÃO GLOMERULAR" number="02" available={renalAvailable} title="Módulo Rim" description="Segmentação de estruturas glomerulares com geração de máscara binária e imagem de sobreposição." onClick={() => onSelect("renal")} />
        </div>
      </section>
    </>
  );
}

function ModuleCard({ icon, iconClass, task, number, available, title, description, onClick }: {
  icon: "blood" | "renal";
  iconClass: string;
  task: string;
  number: string;
  available: boolean;
  title: string;
  description: string;
  onClick: () => void;
}) {
  return (
    <article className={`module-card ${available ? "available-card" : "pending-card"}`}>
      <div className="card-top">
        <div className={`module-icon ${iconClass}`} aria-hidden="true"><ModuleIcon type={icon} /></div>
        <span className="module-number">{number}</span>
      </div>
      <div className="module-meta"><span>{task}</span><span className={`status ${available ? "available" : "pending"}`}><i />{available ? "Disponível" : "Modelo ausente"}</span></div>
      <h3>{title}</h3><p>{description}</p>
      <button className={available ? "primary-button" : "secondary-button"} type="button" disabled={!available} onClick={onClick}>
        {available ? <>Acessar módulo <span aria-hidden="true">→</span></> : "Integração indisponível"}
      </button>
    </article>
  );
}

function ModuleIcon({ type }: { type: "blood" | "renal" }) {
  if (type === "blood") {
    return <svg viewBox="0 0 48 48"><circle cx="24" cy="24" r="14" /><circle className="icon-detail" cx="24" cy="24" r="6" /><path d="M15 11l-3-3m21 29 3 3M37 15l3-3M11 33l-3 3" /></svg>;
  }
  return <svg viewBox="0 0 48 48"><path d="M25.5 8.5C16.8 8.5 11 15.4 11 24.6c0 8.8 4.9 14.9 11.5 14.9 4.8 0 7-3.4 7-7.2 0-3.5-2-6.6-2-10.2 0-4 2.1-6.6 5.8-7.6-1.9-3.7-4.5-6-7.8-6Z" /><path className="icon-detail" d="M33.2 14.5c3.5.2 5.8 3.3 5.8 7.5 0 4.8-2.4 8.3-6.3 9.9M18 20c2.8 1.1 4.8 3.8 4.8 7" /></svg>;
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
