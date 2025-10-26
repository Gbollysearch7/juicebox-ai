import type { Candidate } from '../types';
import {
  MapPin,
  Briefcase,
  Building2,
  CheckCircle2,
  XCircle,
  Star,
  ExternalLink,
  Linkedin,
  Mail
} from 'lucide-react';

interface CandidateCardProps {
  candidate: Candidate;
  onClick?: () => void;
}

export function CandidateCard({ candidate, onClick }: CandidateCardProps) {
  const { properties, verification, score } = candidate;

  const getScoreColor = (score?: number) => {
    if (!score) return 'bg-gray-100 text-gray-600';
    if (score >= 80) return 'bg-green-100 text-green-700';
    if (score >= 60) return 'bg-yellow-100 text-yellow-700';
    return 'bg-red-100 text-red-700';
  };

  const getScoreLabel = (score?: number) => {
    if (!score) return 'N/A';
    if (score >= 80) return 'Excellent Match';
    if (score >= 60) return 'Good Match';
    return 'Partial Match';
  };

  return (
    <div
      onClick={onClick}
      className="card hover:shadow-md transition-shadow cursor-pointer group"
    >
      {/* Header */}
      <div className="flex items-start justify-between mb-4">
        <div className="flex-1">
          <h3 className="text-xl font-semibold text-gray-900 group-hover:text-primary-600 transition-colors">
            {properties.name || 'Unknown Candidate'}
          </h3>
          {properties.current_role && (
            <p className="text-gray-600 mt-1 flex items-center gap-2">
              <Briefcase className="h-4 w-4" />
              {properties.current_role}
            </p>
          )}
        </div>

        {/* Score Badge */}
        {score !== undefined && (
          <div className="flex flex-col items-end gap-1">
            <div className={`px-3 py-1 rounded-full text-sm font-medium ${getScoreColor(score)}`}>
              <div className="flex items-center gap-1">
                <Star className="h-3 w-3 fill-current" />
                {Math.round(score)}
              </div>
            </div>
            <span className="text-xs text-gray-500">{getScoreLabel(score)}</span>
          </div>
        )}
      </div>

      {/* Company and Location */}
      <div className="flex flex-wrap gap-4 mb-4 text-sm text-gray-600">
        {properties.current_company && (
          <div className="flex items-center gap-2">
            <Building2 className="h-4 w-4" />
            {properties.current_company}
          </div>
        )}
        {properties.location && (
          <div className="flex items-center gap-2">
            <MapPin className="h-4 w-4" />
            {properties.location}
          </div>
        )}
      </div>

      {/* Skills */}
      {properties.skills && properties.skills.length > 0 && (
        <div className="mb-4">
          <div className="flex flex-wrap gap-2">
            {properties.skills.slice(0, 5).map((skill, idx) => (
              <span
                key={idx}
                className="px-2 py-1 bg-primary-50 text-primary-700 text-xs rounded-md"
              >
                {skill}
              </span>
            ))}
            {properties.skills.length > 5 && (
              <span className="px-2 py-1 bg-gray-100 text-gray-600 text-xs rounded-md">
                +{properties.skills.length - 5} more
              </span>
            )}
          </div>
        </div>
      )}

      {/* Verification Status */}
      {verification && (
        <div className="mb-4 p-3 bg-gray-50 rounded-lg">
          <div className="flex items-center gap-2 mb-2">
            {verification.passed ? (
              <>
                <CheckCircle2 className="h-4 w-4 text-green-600" />
                <span className="text-sm font-medium text-green-700">
                  Verified ({verification.criteria_results.filter(c => c.passed).length}/{verification.criteria_results.length})
                </span>
              </>
            ) : (
              <>
                <XCircle className="h-4 w-4 text-red-600" />
                <span className="text-sm font-medium text-red-700">
                  Partial Match ({verification.criteria_results.filter(c => c.passed).length}/{verification.criteria_results.length})
                </span>
              </>
            )}
          </div>
        </div>
      )}

      {/* Contact Links */}
      <div className="flex gap-3 pt-4 border-t border-gray-200">
        {properties.linkedin_url && (
          <a
            href={properties.linkedin_url}
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center gap-2 text-sm text-primary-600 hover:text-primary-700 transition-colors"
            onClick={(e) => e.stopPropagation()}
          >
            <Linkedin className="h-4 w-4" />
            LinkedIn
            <ExternalLink className="h-3 w-3" />
          </a>
        )}
        {properties.email && (
          <a
            href={`mailto:${properties.email}`}
            className="flex items-center gap-2 text-sm text-primary-600 hover:text-primary-700 transition-colors"
            onClick={(e) => e.stopPropagation()}
          >
            <Mail className="h-4 w-4" />
            Email
          </a>
        )}
        {!properties.linkedin_url && !properties.email && candidate.url && (
          <a
            href={candidate.url}
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center gap-2 text-sm text-primary-600 hover:text-primary-700 transition-colors"
            onClick={(e) => e.stopPropagation()}
          >
            View Profile
            <ExternalLink className="h-3 w-3" />
          </a>
        )}
      </div>
    </div>
  );
}
