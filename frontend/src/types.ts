export type ModuleStatus = "available" | "integration_pending";

export interface AnalysisModule {
  slug: string;
  name: string;
  task: "segmentation" | "classification";
  status: ModuleStatus;
  input_scope: string;
}

export interface LeukemiaPrediction {
  analysis_id: string;
  predicted_class: "normal" | "malignant";
  malignant_score: number;
  normal_score: number;
  threshold: number;
  inference_time_ms: number;
  experimental: boolean;
}

export interface RenalSegmentation {
  analysis_id: string;
  mask_url: string;
  overlay_url: string;
  mask_mean: number;
  mask_coverage: number;
  threshold: number;
  fold: number;
  inference_time_ms: number;
  experimental: boolean;
}
