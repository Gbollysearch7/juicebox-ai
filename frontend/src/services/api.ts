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

  constructor(baseURL: string = 'http://localhost:8000') {
    this.client = axios.create({
      baseURL,
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
   */
  async pollSearchStatus(
    searchId: string,
    onProgress?: (status: SearchStatusResponse) => void,
    interval: number = 3000
  ): Promise<SearchStatusResponse> {
    return new Promise((resolve, reject) => {
      const poll = setInterval(async () => {
        try {
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
    });
  }
}

// Export singleton instance
export const apiClient = new JuiceboxAPIClient();

// Export class for custom instances
export default JuiceboxAPIClient;
