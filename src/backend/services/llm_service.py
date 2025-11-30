"""
LLM Service for AI-powered code analysis.
Supports multiple LLM providers (Anthropic Claude, OpenAI).
"""
from typing import Dict, Any, Optional
import anthropic
import openai
from config.settings import get_settings
from utils.logger import setup_logger

logger = setup_logger(__name__)
settings = get_settings()


class LLMService:
    """Service for interacting with Large Language Models."""

    def __init__(self):
        """Initialize the LLM service with configured provider."""
        self.provider = settings.llm_provider
        self.model = settings.llm_model
        self.temperature = settings.llm_temperature
        self.max_tokens = settings.llm_max_tokens

        if self.provider == "anthropic":
            if not settings.anthropic_api_key:
                logger.warning("Anthropic API key not configured, using mock responses")
                self.client = None
            else:
                self.client = anthropic.Anthropic(api_key=settings.anthropic_api_key)
        elif self.provider == "openai":
            if not settings.openai_api_key:
                logger.warning("OpenAI API key not configured, using mock responses")
                self.client = None
            else:
                openai.api_key = settings.openai_api_key
                self.client = openai
        else:
            logger.error(f"Unknown LLM provider: {self.provider}")
            self.client = None

    def analyze_code(
        self,
        code: str,
        language: Optional[str] = None,
        context: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Analyze code using the configured LLM.

        Args:
            code: The code snippet to analyze
            language: Programming language (optional)
            context: Additional context for analysis (optional)

        Returns:
            Dict containing analysis results with review and suggestions
        """
        if not self.client:
            return self._mock_analysis(code)

        try:
            prompt = self._build_analysis_prompt(code, language, context)

            if self.provider == "anthropic":
                return self._analyze_with_anthropic(prompt)
            elif self.provider == "openai":
                return self._analyze_with_openai(prompt)
            else:
                return self._mock_analysis(code)

        except Exception as e:
            logger.error(f"Error during LLM analysis: {str(e)}")
            return {
                "review": f"Error analyzing code: {str(e)}",
                "suggestions": ["Please check your API key and try again."],
                "error": True
            }

    def _build_analysis_prompt(
        self,
        code: str,
        language: Optional[str],
        context: Optional[str]
    ) -> str:
        """Build the analysis prompt for the LLM."""
        prompt = f"""You are an expert code reviewer. Analyze the following code and provide:

1. A comprehensive code review covering:
   - Code quality and readability
   - Potential bugs or issues
   - Security vulnerabilities
   - Performance considerations
   - Best practices

2. Specific, actionable suggestions for improvement

Code to review:
```{language or 'text'}
{code}
```
"""
        if context:
            prompt += f"\nAdditional context: {context}\n"

        prompt += """
Please provide your analysis in a structured format:
- Start with an overall assessment
- List specific issues found
- Provide concrete suggestions for improvement
"""
        return prompt

    def _analyze_with_anthropic(self, prompt: str) -> Dict[str, Any]:
        """Analyze code using Anthropic Claude."""
        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            response_text = message.content[0].text
            return self._parse_llm_response(response_text)

        except Exception as e:
            logger.error(f"Anthropic API error: {str(e)}")
            raise

    def _analyze_with_openai(self, prompt: str) -> Dict[str, Any]:
        """Analyze code using OpenAI GPT."""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert code reviewer."},
                    {"role": "user", "content": prompt}
                ],
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )

            response_text = response.choices[0].message.content
            return self._parse_llm_response(response_text)

        except Exception as e:
            logger.error(f"OpenAI API error: {str(e)}")
            raise

    def _parse_llm_response(self, response_text: str) -> Dict[str, Any]:
        """
        Parse LLM response into structured format.

        Args:
            response_text: Raw text response from LLM

        Returns:
            Structured analysis results
        """
        # Split response into review and suggestions
        lines = response_text.strip().split('\n')

        review_parts = []
        suggestions = []
        in_suggestions = False

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Check if we're entering suggestions section
            if any(keyword in line.lower() for keyword in ['suggestion', 'recommendation', 'improve']):
                in_suggestions = True
                continue

            if in_suggestions:
                # Extract suggestions (lines starting with -, *, numbers, or bullet points)
                if line.startswith(('-', '*', '"')) or (line[0].isdigit() and line[1:3] in ['. ', ') ']):
                    suggestions.append(line.lstrip('-*"0123456789. )'))
                elif line:
                    suggestions.append(line)
            else:
                review_parts.append(line)

        review = '\n'.join(review_parts) if review_parts else response_text

        if not suggestions:
            # If no suggestions were parsed, create a default one
            suggestions = ["Consider reviewing the code analysis above for improvements."]

        return {
            "review": review,
            "suggestions": suggestions[:10],  # Limit to top 10 suggestions
            "error": False
        }

    def _mock_analysis(self, code: str) -> Dict[str, Any]:
        """
        Provide mock analysis when LLM is not available.

        Args:
            code: The code to analyze

        Returns:
            Mock analysis results
        """
        logger.info("Using mock analysis (LLM not configured)")

        # Basic static analysis
        lines = code.strip().split('\n')
        num_lines = len(lines)

        suggestions = []

        # Simple heuristics
        if num_lines > 50:
            suggestions.append("Consider breaking this code into smaller functions for better maintainability.")

        if 'TODO' in code or 'FIXME' in code:
            suggestions.append("Address TODO/FIXME comments before production deployment.")

        if '# ' not in code and '//' not in code and '/*' not in code:
            suggestions.append("Add comments to explain complex logic and improve code documentation.")

        if 'password' in code.lower() or 'secret' in code.lower() or 'api_key' in code.lower():
            suggestions.append("�  SECURITY: Avoid hardcoding sensitive information. Use environment variables.")

        if not suggestions:
            suggestions = [
                "Ensure proper error handling is implemented.",
                "Add unit tests to verify functionality.",
                "Consider adding type hints for better code clarity."
            ]

        return {
            "review": f"""=� Code Analysis (Mock Mode - Configure API key for AI-powered analysis)

**Code Statistics:**
- Lines of code: {num_lines}
- Analysis: Basic structure detected

**Note:** For comprehensive AI-powered analysis including security vulnerabilities,
performance optimization, and best practice recommendations, please configure your
LLM API key in the .env file.

To enable AI analysis:
1. Copy .env.example to .env
2. Add your ANTHROPIC_API_KEY or OPENAI_API_KEY
3. Restart the application
""",
            "suggestions": suggestions,
            "mock": True,
            "error": False
        }


# Global instance
_llm_service: Optional[LLMService] = None


def get_llm_service() -> LLMService:
    """
    Get or create the LLM service instance (Singleton pattern).

    Returns:
        LLMService: The LLM service instance
    """
    global _llm_service
    if _llm_service is None:
        _llm_service = LLMService()
    return _llm_service
