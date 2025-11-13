import React, { useState } from 'react';
import CodeInputForm from './components/CodeInputForm';
import ReviewResult from './components/ReviewResult';
import { reviewCode } from './services/api';
import './App.css';

function App() {
  const [code, setCode] = useState('');
  const [review, setReview] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setReview(null);
    setLoading(true);

    try {
      const data = await reviewCode(code);
      setReview(data);
    } catch (err) {
      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError('An unknown error occurred.');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleClear = () => {
    setCode('');
    setReview(null);
    setError(null);
  };

  return (
    <div className="bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 min-h-screen text-white">
      <div className="max-w-6xl mx-auto p-8">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-5xl font-bold mb-4 bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent">
            AI Code Reviewer
          </h1>
          <p className="text-gray-400 text-lg">
            Intelligent code analysis powered by AI and static analysis
          </p>
        </div>

        {/* Main Content */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Left Panel - Code Input */}
          <div>
            <CodeInputForm
              code={code}
              setCode={setCode}
              handleSubmit={handleSubmit}
              handleClear={handleClear}
              loading={loading}
            />
          </div>

          {/* Right Panel - Results */}
          <div>
            {loading && (
              <div className="bg-gray-800 p-8 rounded-lg shadow-xl border border-gray-700">
                <div className="flex flex-col items-center justify-center">
                  <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-blue-500 mb-4"></div>
                  <p className="text-gray-400 text-lg">Analyzing your code...</p>
                  <p className="text-gray-500 text-sm mt-2">This may take a few seconds</p>
                </div>
              </div>
            )}

            {error && !loading && (
              <div className="bg-red-900/30 border border-red-700 p-6 rounded-lg shadow-xl">
                <h2 className="text-2xl font-bold mb-4 text-red-400 flex items-center">
                  <span className="mr-2">⚠️</span> Error
                </h2>
                <p className="text-red-300">{error}</p>
              </div>
            )}

            {review && !loading && <ReviewResult review={review} />}

            {!review && !error && !loading && (
              <div className="bg-gray-800 p-8 rounded-lg shadow-xl border border-gray-700">
                <div className="text-center text-gray-400">
                  <div className="text-6xl mb-4">💻</div>
                  <p className="text-lg">Paste your code and click "Review Code" to get started</p>
                  <div className="mt-6 text-sm text-gray-500">
                    <p className="mb-2">Features:</p>
                    <ul className="space-y-1">
                      <li>✓ Multi-language support</li>
                      <li>✓ Security vulnerability detection</li>
                      <li>✓ Performance optimization suggestions</li>
                      <li>✓ Code quality metrics</li>
                    </ul>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Footer */}
        <div className="mt-12 text-center text-gray-500 text-sm">
          <p>Powered by AI &amp; Static Analysis | Version 1.0.0</p>
        </div>
      </div>
    </div>
  );
}

export default App;
