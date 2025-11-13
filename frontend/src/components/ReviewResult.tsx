import React from 'react';

interface Props {
  review: {
    review: string;
    suggestions: string[];
  };
}

const ReviewResult: React.FC<Props> = ({ review }) => {
  return (
    <div className="mt-8 bg-gray-800 p-6 rounded-lg">
      <h2 className="text-2xl font-bold mb-4">Review Results</h2>
      <p className="mb-4">{review.review}</p>
      <h3 className="text-xl font-bold mb-2">Suggestions:</h3>
      <ul className="list-disc list-inside">
        {review.suggestions.map((suggestion, index) => (
          <li key={index}>{suggestion}</li>
        ))}
      </ul>
    </div>
  );
};

export default ReviewResult;
