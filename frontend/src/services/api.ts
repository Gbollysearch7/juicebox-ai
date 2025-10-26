/**
 * API client for Juicebox AI Backend
 */
import axios from 'axios';
import type { AxiosInstance } from 'axios';
import type {
  SearchRequest,
  SearchResponse,
  SearchStatusResponse,
  CandidateListResponse,
  Candidate,
  HealthCheckResponse
} from '../types';

class JuiceboxAPIClient {
  private client: AxiosInstance;

  constructor(baseURL?: string) {
    // Use environment variable if available, fallback to localhost
    const apiURL = baseURL || import.meta.env.VITE_API_URL || 'http://localhost:8000';

    this.client = axios.create({
      baseURL: apiURL,
      headers: {
        'Content-Type': 'application/json',
      },
      timeout: 30000, // 30 seconds
    });
  }

  /**
   * Health check
   */
  async healthCheck(): Promise<HealthCheckResponse> {
    const response = await this.client.get<HealthCheckResponse>('/health');
    return response.data;
  }

  /**
   * Create a new candidate search
   */
  async createSearch(request: SearchRequest): Promise<SearchResponse> {
    const response = await this.client.post<SearchResponse>(
      '/api/v1/search',
      request
    );
    return response.data;
  }

  /**
   * Get search status and results
   */
  async getSearchStatus(searchId: string): Promise<SearchStatusResponse> {
    const response = await this.client.get<SearchStatusResponse>(
      `/api/v1/search/${searchId}`
    );
    return response.data;
  }

  /**
   * List all searches
   */
  async listSearches(): Promise<SearchStatusResponse[]> {
    const response = await this.client.get<SearchStatusResponse[]>(
      '/api/v1/search'
    );
    return response.data;
  }

  /**
   * Get all candidates with optional filters
   */
  async getCandidates(params?: {
    search_id?: string;
    min_score?: number;
    verified_only?: boolean;
  }): Promise<CandidateListResponse> {
    const response = await this.client.get<CandidateListResponse>(
      '/api/v1/candidates',
      { params }
    );
    return response.data;
  }

  /**
   * Get a specific candidate by ID
   */
  async getCandidate(candidateId: string): Promise<Candidate> {
    const response = await this.client.get<Candidate>(
      `/api/v1/candidates/${candidateId}`
    );
    return response.data;
  }

  /**
   * Poll search status until completed
   * Returns a cancellable promise with abort capability
   */
  async pollSearchStatus(
    searchId: string,
    onProgress?: (status: SearchStatusResponse) => void,
    interval: number = 3000,
    maxRetries: number = 200 // ~10 minutes max with 3s interval
  ): Promise<SearchStatusResponse> {
    let retryCount = 0;

    return new Promise((resolve, reject) => {
      const poll = setInterval(async () => {
        try {
          retryCount++;

          if (retryCount > maxRetries) {
            clearInterval(poll);
            reject(new Error('Search timeout: exceeded maximum retry attempts'));
            return;
          }

          const status = await this.getSearchStatus(searchId);

          if (onProgress) {
            onProgress(status);
          }

          if (status.status === 'completed') {
            clearInterval(poll);
            resolve(status);
          } else if (status.status === 'failed') {
            clearInterval(poll);
            reject(new Error('Search failed'));
          }
        } catch (error) {
          clearInterval(poll);
          reject(error);
        }
      }, interval);

      // Store interval ID for potential cleanup
      (poll as any).searchId = searchId;
    });
  }

  /**
   * Create cancellable polling with AbortController support
   */
  pollSearchStatusCancellable(
    searchId: string,
    onProgress?: (status: SearchStatusResponse) => void,
    interval: number = 3000,
    signal?: AbortSignal
  ): { promise: Promise<SearchStatusResponse>; cancel: () => void } {
    let intervalId: ReturnType<typeof setInterval> | null = null;
    let cancelled = false;

    const cancel = () => {
      cancelled = true;
      if (intervalId) {
        clearInterval(intervalId);
      }
    };

    // Listen to abort signal if provided
    if (signal) {
      signal.addEventListener('abort', cancel);
    }

    const promise = new Promise<SearchStatusResponse>((resolve, reject) => {
      intervalId = setInterval(async () => {
        if (cancelled) {
          if (intervalId) clearInterval(intervalId);
          reject(new Error('Polling cancelled'));
          return;
        }

        try {
          const status = await this.getSearchStatus(searchId);

          if (onProgress && !cancelled) {
            onProgress(status);
          }

          if (status.status === 'completed') {
            if (intervalId) clearInterval(intervalId);
            resolve(status);
          } else if (status.status === 'failed') {
            if (intervalId) clearInterval(intervalId);
            reject(new Error('Search failed'));
          }
        } catch (error) {
          if (intervalId) clearInterval(intervalId);
          reject(error);
        }
      }, interval);
    });

    return { promise, cancel };
  }
}

// Export singleton instance
export const apiClient = new JuiceboxAPIClient();

// Export class for custom instances
export default JuiceboxAPIClient;
