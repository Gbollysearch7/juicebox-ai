/**
 * Type definitions for Juicebox AI
 */

export const EntityType = {
  PERSON: "person",
  COMPANY: "company",
  RESEARCH_PAPER: "research_paper",
  ARTICLE: "article"
} as const;

export type EntityType = typeof EntityType[keyof typeof EntityType];

export const SearchStatus = {
  PENDING: "pending",
  IN_PROGRESS: "in_progress",
  COMPLETED: "completed",
  FAILED: "failed"
} as const;

export type SearchStatus = typeof SearchStatus[keyof typeof SearchStatus];

export interface CriteriaResult {
  description: string;
  passed: boolean;
  reasoning: string;
  references: string[];
}

export interface VerificationResult {
  passed: boolean;
  criteria_results: CriteriaResult[];
}

export interface EnrichmentResult {
  description: string;
  status: string;
  result?: any;
}

export interface CandidateProperties {
  name?: string;
  current_role?: string;
  current_company?: string;
  location?: string;
  linkedin_url?: string;
  email?: string;
  experience_years?: number;
  skills?: string[];
}

export interface Candidate {
  id: string;
  url: string;
  title: string;
  status: string;
  verification?: VerificationResult;
  properties: CandidateProperties;
  enrichments: EnrichmentResult[];
  score?: number;
  created_at?: string;
}

export interface SearchRequest {
  query: string;
  count: number;
  entity: EntityType;
  criteria: string[];
  exclude_criteria?: string[];
  enrichments: string[];
}

export interface SearchResponse {
  search_id: string;
  status: SearchStatus;
  query: string;
  count: number;
  created_at: string;
  message: string;
}

export interface SearchStatusResponse {
  search_id: string;
  status: SearchStatus;
  query: string;
  total_requested: number;
  total_found: number;
  candidates: Candidate[];
  progress_percent: number;
  estimated_time_remaining?: number;
}

export interface CandidateListResponse {
  total: number;
  candidates: Candidate[];
}

export interface HealthCheckResponse {
  status: string;
  version: string;
  timestamp: string;
}
