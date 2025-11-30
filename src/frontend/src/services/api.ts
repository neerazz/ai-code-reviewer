const API_BASE_URL = 'http://localhost:8000';

export const reviewCode = async (code: string) => {
  const response = await fetch(`${API_BASE_URL}/review`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ code }),
  });

  if (!response.ok) {
    throw new Error('Something went wrong with the review request.');
  }

  return response.json();
};
