import React, { useState } from 'react';
import CodeInputForm from './components/CodeInputForm';
import ReviewResult from './components/ReviewResult';
import { reviewCode } from './services/api';
import './App.css';

function App(): JSX.Element {
  const [code, setCode] = useState('');
  const [review, setReview] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    try {
      const data = await reviewCode(code);
      setReview(data);
    } catch (err) {
      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError('An unknown error occurred.');
      }
    }
  };

  return (
    <div className="bg-gray-900 min-h-screen text-white p-8">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-4xl font-bold mb-8 text-center">AI Code Reviewer</h1>
        <CodeInputForm
          code={code}
          setCode={setCode}
          handleSubmit={handleSubmit}
        />
        {error && (
          <div className="mt-8 bg-red-800 p-6 rounded-lg">
            <h2 className="text-2xl font-bold mb-4">Error</h2>
            <p>{error}</p>
          </div>
        )}
        {review && <ReviewResult review={review} />}
      </div>
    </div>
  );
}

export default App;
