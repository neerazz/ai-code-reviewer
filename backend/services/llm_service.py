"""
LLM Service for code review using Claude or OpenAI
"""
from typing import Optional, List, Dict, Any
from anthropic import Anthropic
from openai import OpenAI
import json
from config.settings import settings
from backend.utils.logger import get_logger

logger = get_logger(__name__)


class LLMService:
    """Service for interacting with LLMs"""

    def __init__(self):
        self.provider = settings.LLM_PROVIDER
        self.model = settings.LLM_MODEL
        self.temperature = settings.LLM_TEMPERATURE
        self.max_tokens = settings.LLM_MAX_TOKENS

        if self.provider == "anthropic":
            self.client = Anthropic(api_key=settings.ANTHROPIC_API_KEY)
        elif self.provider == "openai":
            self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        else:
            raise ValueError(f"Unsupported LLM provider: {self.provider}")

    async def review_code(
        self,
        code: str,
        file_path: str,
        language: str,
        context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Review code and return findings

        Args:
            code: The code to review
            file_path: Path to the file
            language: Programming language
            context: Additional context (PR description, related files, etc.)

        Returns:
            Dictionary with review findings
        """
        prompt = self._build_review_prompt(code, file_path, language, context)

        try:
            if self.provider == "anthropic":
                response = await self._call_anthropic(prompt)
            else:
                response = await self._call_openai(prompt)

            return self._parse_review_response(response)

        except Exception as e:
            logger.error(f"Error reviewing code: {str(e)}")
            raise

    async def suggest_migration(
        self,
        code: str,
        source_framework: str,
        target_framework: str,
        language: str,
    ) -> Dict[str, Any]:
        """
        Suggest code migration from one framework to another

        Args:
            code: Source code
            source_framework: Source framework/version
            target_framework: Target framework/version
            language: Programming language

        Returns:
            Migration suggestions and transformed code
        """
        prompt = self._build_migration_prompt(
            code, source_framework, target_framework, language
        )

        try:
            if self.provider == "anthropic":
                response = await self._call_anthropic(prompt)
            else:
                response = await self._call_openai(prompt)

            return self._parse_migration_response(response)

        except Exception as e:
            logger.error(f"Error suggesting migration: {str(e)}")
            raise

    async def detect_patterns(
        self,
        code: str,
        language: str,
        custom_patterns: Optional[List[Dict[str, Any]]] = None,
    ) -> List[Dict[str, Any]]:
        """
        Detect code patterns and anti-patterns

        Args:
            code: Code to analyze
            language: Programming language
            custom_patterns: Custom patterns to check for

        Returns:
            List of detected patterns
        """
        prompt = self._build_pattern_detection_prompt(code, language, custom_patterns)

        try:
            if self.provider == "anthropic":
                response = await self._call_anthropic(prompt)
            else:
                response = await self._call_openai(prompt)

            return self._parse_pattern_response(response)

        except Exception as e:
            logger.error(f"Error detecting patterns: {str(e)}")
            raise

    async def _call_anthropic(self, prompt: str) -> str:
        """Call Anthropic API"""
        message = self.client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            messages=[{"role": "user", "content": prompt}],
        )
        return message.content[0].text

    async def _call_openai(self, prompt: str) -> str:
        """Call OpenAI API"""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=self.temperature,
            max_tokens=self.max_tokens,
        )
        return response.choices[0].message.content

    def _build_review_prompt(
        self,
        code: str,
        file_path: str,
        language: str,
        context: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Build prompt for code review"""
        return f"""You are an expert code reviewer. Analyze the following {language} code and provide a detailed review.

File: {file_path}

Code:
```{language}
{code}
```

{f"Context: {json.dumps(context, indent=2)}" if context else ""}

Please provide a comprehensive review covering:
1. Security vulnerabilities (OWASP guidelines)
2. Performance issues
3. Code quality and maintainability
4. Best practices violations
5. Potential bugs
6. Suggestions for improvement

Return your response as a JSON object with the following structure:
{{
    "overall_score": <0-100>,
    "security_score": <0-100>,
    "performance_score": <0-100>,
    "quality_score": <0-100>,
    "issues": [
        {{
            "line": <line_number>,
            "severity": "critical|error|warning|info",
            "category": "security|performance|quality|bugs|style",
            "title": "Short title",
            "description": "Detailed description",
            "suggestion": "How to fix it",
            "confidence": <0-1>
        }}
    ],
    "summary": "Overall summary of the review"
}}
"""

    def _build_migration_prompt(
        self,
        code: str,
        source_framework: str,
        target_framework: str,
        language: str,
    ) -> str:
        """Build prompt for code migration"""
        return f"""You are an expert in code migration and refactoring. Help migrate the following code.

Language: {language}
Source: {source_framework}
Target: {target_framework}

Code:
```{language}
{code}
```

Please provide:
1. Analysis of what needs to be migrated
2. Step-by-step migration plan
3. Transformed code
4. Breaking changes and potential issues
5. Testing recommendations

Return your response as a JSON object with this structure:
{{
    "migration_complexity": "low|medium|high",
    "estimated_effort_hours": <number>,
    "breaking_changes": ["list of breaking changes"],
    "migration_steps": ["step 1", "step 2", ...],
    "transformed_code": "The migrated code",
    "test_recommendations": ["test suggestion 1", ...],
    "notes": "Additional notes and warnings"
}}
"""

    def _build_pattern_detection_prompt(
        self,
        code: str,
        language: str,
        custom_patterns: Optional[List[Dict[str, Any]]] = None,
    ) -> str:
        """Build prompt for pattern detection"""
        custom_patterns_str = ""
        if custom_patterns:
            custom_patterns_str = f"\n\nAlso check for these custom patterns:\n{json.dumps(custom_patterns, indent=2)}"

        return f"""You are an expert at detecting code patterns and anti-patterns. Analyze the following {language} code.

Code:
```{language}
{code}
```
{custom_patterns_str}

Identify:
1. Design patterns used
2. Anti-patterns
3. Code smells
4. Architectural patterns
5. Common mistakes

Return as JSON:
{{
    "patterns": [
        {{
            "name": "Pattern name",
            "type": "design_pattern|anti_pattern|code_smell",
            "line": <line_number>,
            "confidence": <0-1>,
            "description": "What was found",
            "impact": "critical|high|medium|low",
            "recommendation": "What to do about it"
        }}
    ]
}}
"""

    def _parse_review_response(self, response: str) -> Dict[str, Any]:
        """Parse LLM review response"""
        try:
            # Try to extract JSON from response
            start = response.find("{")
            end = response.rfind("}") + 1
            if start >= 0 and end > start:
                json_str = response[start:end]
                return json.loads(json_str)
            return {"error": "Could not parse response", "raw_response": response}
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing review response: {str(e)}")
            return {"error": str(e), "raw_response": response}

    def _parse_migration_response(self, response: str) -> Dict[str, Any]:
        """Parse LLM migration response"""
        return self._parse_review_response(response)

    def _parse_pattern_response(self, response: str) -> List[Dict[str, Any]]:
        """Parse LLM pattern detection response"""
        parsed = self._parse_review_response(response)
        return parsed.get("patterns", [])


# Singleton instance
llm_service = LLMService()
