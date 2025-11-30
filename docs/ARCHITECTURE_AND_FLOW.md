# Application Architecture and Execution Flow

This document provides a detailed technical deep-dive into the application's execution flow, tracing calls from entry points down to individual functions.

## Table of Contents

1. [Backend Execution Flow](#backend-execution-flow)
2. [Frontend Execution Flow](#frontend-execution-flow)
3. [Data Flow & Interactions](#data-flow--interactions)

---

## Backend Execution Flow

### 1. Entry Point: `src/backend/api/main.py`

The backend is a FastAPI application. The entry point is `main.py`.

**Initialization Sequence:**

1. `FastAPI` app created.
2. CORS middleware configured.
3. `review.router` included.

### 2. Review Endpoint: `POST /review`

**File:** `src/backend/api/routers/review.py`

**Flow:**

1. **Input Validation**: Checks if `code` is empty.
2. **Static Analysis**: Calls `CodeAnalyzer.analyze(code, language)`.
    - Detects language if not provided.
    - Calculates metrics (lines, complexity).
    - Identifies syntax/style issues.
    - Computes quality score.
3. **AI Analysis**: Calls `LLMService.analyze_code(code, language, context)`.
    - Uses LLM (Claude/GPT) to review code.
    - Returns natural language review and suggestions.
4. **Result Aggregation**:
    - Combines static issues and AI suggestions.
    - Formats a markdown review summary.
    - Returns JSON response with `review`, `suggestions`, `quality_score`, `metrics`.

---

## Frontend Execution Flow

### 1. Entry Point: `src/frontend/src/index.tsx`

The frontend is a React application.

- **Initialization**: `ReactDOM.createRoot` renders `<App />` into `#root`.

### 2. Main Component: `frontend/src/App.tsx`

**Responsibilities:**

- **State Management**:
  - `code`: User input string.
  - `review`: Analysis result object.
  - `loading`: Boolean flag for API request status.
  - `error`: Error message string.
- **Event Handling**:
  - `handleSubmit`: Calls `reviewCode` API service.
  - `handleClear`: Resets state.

### 3. Components

#### `CodeInputForm`

- **Location**: `src/frontend/src/components/CodeInputForm.tsx`
- **Purpose**: Textarea for code input.
- **Props**: `code`, `setCode`, `handleSubmit`, `handleClear`, `loading`.

#### `ReviewResult`

- **Location**: `src/frontend/src/components/ReviewResult.tsx`
- **Purpose**: Displays the analysis results.
- **Features**:
  - Renders markdown review.
  - Shows quality score and metrics.
  - Lists suggestions.

### 4. API Service: `src/frontend/src/services/api.ts`

**Function**: `reviewCode(code: str)`

- **Endpoint**: `POST /review` (configured via `API_URL`).
- **Payload**: `{ code: "...", language: "..." }`.
- **Response**: Returns JSON data matching `ReviewResponse` schema.

---

## Data Flow & Interactions

### JSON Payloads

#### Request: `POST /review`

```json
{
  "code": "def hello(): print('world')",
  "language": "python",
  "context": "optional context"
}
```

#### Response: `200 OK`

```json
{
  "review": "Markdown formatted review...",
  "suggestions": [
    "Suggestion 1",
    "Suggestion 2"
  ],
  "quality_score": 85,
  "language": "python",
  "metrics": {
    "total_lines": 1,
    "code_lines": 1,
    "comment_lines": 0,
    "blank_lines": 0,
    "max_line_length": 26,
    "avg_line_length": 26
  },
  "issues_count": 0
}
```

### Error Handling

- **400 Bad Request**: If `code` is empty.
- **500 Internal Server Error**: If analysis fails (e.g., LLM error).
  - The frontend displays a generic error message or the specific error details if available.
