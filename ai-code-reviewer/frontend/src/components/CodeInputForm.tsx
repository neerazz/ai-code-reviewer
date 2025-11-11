import React from 'react';

interface Props {
  code: string;
  setCode: (code: string) => void;
  handleSubmit: (e: React.FormEvent) => void;
}

const CodeInputForm: React.FC<Props> = ({ code, setCode, handleSubmit }) => {
  return (
    <form onSubmit={handleSubmit}>
      <textarea
        data-testid="code-input"
        className="w-full h-64 bg-gray-800 text-white p-4 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        value={code}
        onChange={(e) => setCode(e.target.value)}
        placeholder="Paste your code here..."
      />
      <button
        type="submit"
        className="mt-4 bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-lg w-full"
      >
        Review Code
      </button>
    </form>
  );
};

export default CodeInputForm;
