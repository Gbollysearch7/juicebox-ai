import { useState } from 'react';
import { SearchBox } from '../components/SearchBox';
import { CandidateCard } from '../components/CandidateCard';
import { LoadingState } from '../components/LoadingState';
import { apiClient } from '../services/api';
import { EntityType } from '../types';
import type { SearchStatusResponse } from '../types';
import { Filter, SlidersHorizontal, Users, TrendingUp } from 'lucide-react';

export function SearchPage() {
  const [isSearching, setIsSearching] = useState(false);
  const [searchResult, setSearchResult] = useState<SearchStatusResponse | null>(null);
  const [minScore, setMinScore] = useState<number>(0);
  const [verifiedOnly, setVerifiedOnly] = useState(false);
  const [showFilters, setShowFilters] = useState(false);

  const handleSearch = async (query: string) => {
    setIsSearching(true);
    setSearchResult(null);

    try {
      // Create search
      const response = await apiClient.createSearch({
        query,
        count: 10,
        entity: EntityType.PERSON,
        criteria: [
          `Matches the description: ${query}`,
          'Currently employed or recently active in their field',
        ],
        enrichments: [
          'Find their LinkedIn profile',
          'Extract current role and company',
          'Identify key skills and experience',
        ],
      });

      // Poll for results
      await apiClient.pollSearchStatus(
        response.search_id,
        (status) => {
          setSearchResult(status);
        },
        3000
      );
    } catch (error) {
      console.error('Search failed:', error);
      alert('Search failed. Please try again.');
    } finally {
      setIsSearching(false);
    }
  };

  const filteredCandidates = searchResult?.candidates.filter((candidate) => {
    if (minScore > 0 && (!candidate.score || candidate.score < minScore)) {
      return false;
    }
    if (verifiedOnly && (!candidate.verification || !candidate.verification.passed)) {
      return false;
    }
    return true;
  }) || [];

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="h-10 w-10 bg-gradient-to-br from-primary-500 to-primary-600 rounded-xl flex items-center justify-center">
                <Users className="h-6 w-6 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-gray-900">Juicebox AI</h1>
                <p className="text-sm text-gray-600">AI-Powered Recruiting</p>
              </div>
            </div>

            {searchResult && (
              <div className="flex items-center gap-4 text-sm">
                <div className="flex items-center gap-2">
                  <TrendingUp className="h-4 w-4 text-green-600" />
                  <span className="font-medium">{searchResult.total_found} candidates found</span>
                </div>
                <button
                  onClick={() => setShowFilters(!showFilters)}
                  className="flex items-center gap-2 px-3 py-2 rounded-lg hover:bg-gray-100 transition-colors"
                >
                  <SlidersHorizontal className="h-4 w-4" />
                  Filters
                </button>
              </div>
            )}
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Search Box */}
        <div className="mb-8">
          <SearchBox
            onSearch={handleSearch}
            isLoading={isSearching}
            placeholder="e.g., Senior ML Engineers at AI startups in San Francisco with 5+ years experience"
          />

          {/* Example Queries */}
          {!searchResult && !isSearching && (
            <div className="mt-6">
              <p className="text-sm text-gray-600 mb-3">Try these examples:</p>
              <div className="flex flex-wrap gap-2">
                {[
                  'Senior Software Engineers with React and Node.js experience',
                  'VP of Engineering at Series B startups',
                  'ML Engineers with computer vision expertise',
                  'Product Managers in fintech with B2B SaaS experience',
                ].map((example, idx) => (
                  <button
                    key={idx}
                    onClick={() => handleSearch(example)}
                    className="px-4 py-2 bg-white border border-gray-200 rounded-lg text-sm hover:border-primary-300 hover:bg-primary-50 transition-colors"
                  >
                    {example}
                  </button>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Filters Panel */}
        {showFilters && searchResult && (
          <div className="card mb-6">
            <div className="flex items-center gap-2 mb-4">
              <Filter className="h-5 w-5 text-gray-600" />
              <h3 className="font-semibold">Filters</h3>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Minimum Score: {minScore}
                </label>
                <input
                  type="range"
                  min="0"
                  max="100"
                  value={minScore}
                  onChange={(e) => setMinScore(Number(e.target.value))}
                  className="w-full"
                />
              </div>

              <div className="flex items-center">
                <input
                  type="checkbox"
                  id="verified"
                  checked={verifiedOnly}
                  onChange={(e) => setVerifiedOnly(e.target.checked)}
                  className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
                />
                <label htmlFor="verified" className="ml-2 text-sm text-gray-700">
                  Show verified candidates only
                </label>
              </div>
            </div>
          </div>
        )}

        {/* Loading State */}
        {isSearching && (
          <LoadingState
            message={`Searching for candidates... ${searchResult ? `Found ${searchResult.total_found} so far` : ''}`}
            progress={searchResult?.progress_percent}
          />
        )}

        {/* Results */}
        {searchResult && !isSearching && (
          <div>
            <div className="mb-6">
              <h2 className="text-xl font-semibold text-gray-900">
                {filteredCandidates.length} Candidate{filteredCandidates.length !== 1 ? 's' : ''}
                {minScore > 0 || verifiedOnly ? ' (filtered)' : ''}
              </h2>
              <p className="text-gray-600 mt-1">
                Search: "{searchResult.query}"
              </p>
            </div>

            {filteredCandidates.length > 0 ? (
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {filteredCandidates.map((candidate) => (
                  <CandidateCard
                    key={candidate.id}
                    candidate={candidate}
                    onClick={() => {
                      // Could open a modal with more details
                      console.log('Clicked candidate:', candidate);
                    }}
                  />
                ))}
              </div>
            ) : (
              <div className="text-center py-12">
                <p className="text-gray-600">
                  No candidates match your filters. Try adjusting them.
                </p>
              </div>
            )}
          </div>
        )}

        {/* Empty State */}
        {!searchResult && !isSearching && (
          <div className="text-center py-16">
            <div className="inline-flex items-center justify-center h-20 w-20 bg-primary-100 rounded-full mb-4">
              <Users className="h-10 w-10 text-primary-600" />
            </div>
            <h2 className="text-2xl font-semibold text-gray-900 mb-2">
              Find Your Perfect Candidates
            </h2>
            <p className="text-gray-600 max-w-md mx-auto">
              Describe the candidates you're looking for in natural language.
              Our AI will search, verify, and rank the best matches for you.
            </p>
          </div>
        )}
      </main>
    </div>
  );
}
