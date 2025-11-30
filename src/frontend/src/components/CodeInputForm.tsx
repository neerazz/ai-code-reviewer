import React from 'react';

interface Props {
  code: string;
  setCode: (code: string) => void;
  handleSubmit: (e: React.FormEvent) => void;
  handleClear: () => void;
  loading: boolean;
}

const CodeInputForm: React.FC<Props> = ({ code, setCode, handleSubmit, handleClear, loading }) => {
  return (
    <div className="bg-gray-800 p-6 rounded-lg shadow-xl border border-gray-700">
      <form onSubmit={handleSubmit}>
        <label className="block text-sm font-semibold text-gray-300 mb-2">
          Code Input
        </label>
        <textarea
          data-testid="code-input"
          className="w-full h-96 bg-gray-900 text-white p-4 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 font-mono text-sm border border-gray-600"
          value={code}
          onChange={(e) => setCode(e.target.value)}
          placeholder="Paste your code here...

Example (Python):
def calculate_sum(a, b):
    password = '12345'  # security issue
    return a + b

Or try JavaScript, TypeScript, Java, Go, etc."
          disabled={loading}
        />
        <div className="mt-4 flex gap-3">
          <button
            type="submit"
            disabled={!code.trim() || loading}
            className="flex-1 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white font-bold py-3 px-6 rounded-lg transition-all disabled:opacity-50 disabled:cursor-not-allowed shadow-lg"
          >
            {loading ? 'Analyzing...' : 'Review Code'}
          </button>
          <button
            type="button"
            onClick={handleClear}
            disabled={!code || loading}
            className="bg-gray-700 hover:bg-gray-600 text-white font-bold py-3 px-6 rounded-lg transition-all disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Clear
          </button>
        </div>
      </form>
    </div>
  );
};

export default CodeInputForm;
