import React from 'react';

interface Props {
  review: {
    review: string;
    suggestions: string[];
    quality_score?: number;
    language?: string;
    metrics?: {
      total_lines: number;
      code_lines: number;
      comment_lines: number;
      blank_lines: number;
      max_line_length: number;
      avg_line_length: number;
    };
    issues_count?: number;
  };
}

const ReviewResult: React.FC<Props> = ({ review }) => {
  const getScoreColor = (score: number) => {
    if (score >= 80) return 'text-green-400';
    if (score >= 60) return 'text-yellow-400';
    return 'text-red-400';
  };

  const getScoreGradient = (score: number) => {
    if (score >= 80) return 'from-green-600 to-green-400';
    if (score >= 60) return 'from-yellow-600 to-yellow-400';
    return 'from-red-600 to-red-400';
  };

  return (
    <div className="bg-gray-800 p-6 rounded-lg shadow-xl border border-gray-700">
      <h2 className="text-3xl font-bold mb-6 flex items-center">
        <span className="mr-3">📊</span> Review Results
      </h2>

      {/* Quality Score Card */}
      {review.quality_score !== undefined && (
        <div className={`mb-6 p-6 rounded-lg bg-gradient-to-r ${getScoreGradient(review.quality_score)}`}>
          <div className="text-center">
            <div className={`text-6xl font-bold ${getScoreColor(review.quality_score)}`}>
              {review.quality_score}
            </div>
            <div className="text-white text-lg font-semibold mt-2">Code Quality Score</div>
            <div className="text-white/80 text-sm mt-1">
              {review.language && `Language: ${review.language.charAt(0).toUpperCase() + review.language.slice(1)}`}
            </div>
          </div>
        </div>
      )}

      {/* Review Text */}
      <div className="mb-6">
        <div className="prose prose-invert max-w-none">
          <div className="bg-gray-900 p-4 rounded-lg border border-gray-600">
            <pre className="whitespace-pre-wrap text-sm text-gray-300 font-sans">
              {review.review}
            </pre>
          </div>
        </div>
      </div>

      {/* Suggestions */}
      {review.suggestions && review.suggestions.length > 0 && (
        <div className="mb-6">
          <h3 className="text-xl font-bold mb-3 flex items-center">
            <span className="mr-2">💡</span> Suggestions ({review.suggestions.length})
          </h3>
          <div className="space-y-2">
            {review.suggestions.map((suggestion, index) => (
              <div
                key={index}
                className="bg-gray-900 p-3 rounded-lg border-l-4 border-blue-500 hover:bg-gray-850 transition-colors"
              >
                <p className="text-gray-300 text-sm">{suggestion}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Metrics Grid */}
      {review.metrics && (
        <div className="grid grid-cols-2 gap-4 mt-6">
          <div className="bg-gray-900 p-4 rounded-lg border border-gray-600">
            <div className="text-gray-400 text-sm">Total Lines</div>
            <div className="text-2xl font-bold text-white">{review.metrics.total_lines}</div>
          </div>
          <div className="bg-gray-900 p-4 rounded-lg border border-gray-600">
            <div className="text-gray-400 text-sm">Code Lines</div>
            <div className="text-2xl font-bold text-white">{review.metrics.code_lines}</div>
          </div>
          <div className="bg-gray-900 p-4 rounded-lg border border-gray-600">
            <div className="text-gray-400 text-sm">Comments</div>
            <div className="text-2xl font-bold text-white">{review.metrics.comment_lines}</div>
          </div>
          <div className="bg-gray-900 p-4 rounded-lg border border-gray-600">
            <div className="text-gray-400 text-sm">Issues Found</div>
            <div className="text-2xl font-bold text-white">{review.issues_count || 0}</div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ReviewResult;
