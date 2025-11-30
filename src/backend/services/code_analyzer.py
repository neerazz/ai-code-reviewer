"""
Code Analyzer Service for static code analysis.
Provides language detection and basic static analysis.
"""
from typing import Dict, Any, Optional, List
import re
from utils.logger import setup_logger

logger = setup_logger(__name__)


class CodeAnalyzer:
    """Service for performing static code analysis."""

    # Language detection patterns
    LANGUAGE_PATTERNS = {
        'python': [r'def\s+\w+\(', r'import\s+\w+', r'from\s+\w+\s+import', r'class\s+\w+:', r'if\s+__name__\s+=='],
        'javascript': [r'function\s+\w+\(', r'const\s+\w+\s*=', r'let\s+\w+\s*=', r'var\s+\w+\s*=', r'=>', r'require\('],
        'typescript': [r'interface\s+\w+', r'type\s+\w+\s*=', r':\s*(string|number|boolean)', r'function\s+\w+\(.*\):\s*\w+'],
        'java': [r'public\s+class', r'private\s+\w+\s+\w+', r'public\s+static\s+void\s+main'],
        'go': [r'func\s+\w+\(', r'package\s+\w+', r'import\s+\(', r':=', r'type\s+\w+\s+struct'],
        'rust': [r'fn\s+\w+\(', r'let\s+mut', r'impl\s+\w+', r'struct\s+\w+', r'use\s+\w+::'],
        'c': [r'#include\s*<', r'int\s+main\s*\(', r'printf\(', r'void\s+\w+\('],
        'cpp': [r'#include\s*<', r'std::', r'namespace\s+\w+', r'class\s+\w+'],
        'ruby': [r'def\s+\w+', r'end$', r'require\s+', r'@\w+\s*='],
        'php': [r'<\?php', r'\$\w+\s*=', r'function\s+\w+\(', r'echo\s+'],
        'sql': [r'SELECT\s+', r'FROM\s+', r'WHERE\s+', r'INSERT\s+INTO', r'CREATE\s+TABLE'],
        'html': [r'<html', r'<div', r'<body', r'<!DOCTYPE'],
        'css': [r'\.\w+\s*{', r'#\w+\s*{', r':\s*\w+;'],
    }

    def detect_language(self, code: str) -> str:
        """
        Detect programming language from code snippet.

        Args:
            code: Code snippet to analyze

        Returns:
            Detected language name or 'unknown'
        """
        scores = {}

        for lang, patterns in self.LANGUAGE_PATTERNS.items():
            score = 0
            for pattern in patterns:
                if re.search(pattern, code, re.MULTILINE | re.IGNORECASE):
                    score += 1
            if score > 0:
                scores[lang] = score

        if not scores:
            return 'unknown'

        # Return language with highest score
        detected_lang = max(scores.items(), key=lambda x: x[1])[0]
        logger.info(f"Detected language: {detected_lang} (score: {scores[detected_lang]})")
        return detected_lang

    def analyze(self, code: str, language: Optional[str] = None) -> Dict[str, Any]:
        """
        Perform static code analysis.

        Args:
            code: Code snippet to analyze
            language: Programming language (if known)

        Returns:
            Analysis results including metrics and issues
        """
        if not language:
            language = self.detect_language(code)

        # Calculate basic metrics
        metrics = self._calculate_metrics(code)

        # Detect common issues
        issues = self._detect_issues(code, language)

        # Calculate complexity score
        complexity_score = self._calculate_complexity(code, language)

        return {
            "language": language,
            "metrics": metrics,
            "issues": issues,
            "complexity_score": complexity_score,
            "quality_score": self._calculate_quality_score(metrics, issues, complexity_score)
        }

    def _calculate_metrics(self, code: str) -> Dict[str, int]:
        """Calculate basic code metrics."""
        lines = code.split('\n')

        return {
            "total_lines": len(lines),
            "code_lines": len([l for l in lines if l.strip() and not l.strip().startswith(('#', '//', '/*'))]),
            "comment_lines": len([l for l in lines if l.strip().startswith(('#', '//', '/*'))]),
            "blank_lines": len([l for l in lines if not l.strip()]),
            "max_line_length": max([len(l) for l in lines]) if lines else 0,
            "avg_line_length": sum([len(l) for l in lines]) // len(lines) if lines else 0
        }

    def _detect_issues(self, code: str, language: str) -> List[Dict[str, Any]]:
        """Detect common code issues."""
        issues = []

        # Security issues
        security_patterns = {
            'hardcoded_password': r'password\s*=\s*["\'].*["\']',
            'hardcoded_secret': r'(secret|api_key|token)\s*=\s*["\'].*["\']',
            'sql_injection': r'(execute|query)\s*\(\s*["\'].*\+.*["\']',
            'eval_usage': r'eval\s*\(',
        }

        for issue_type, pattern in security_patterns.items():
            matches = re.finditer(pattern, code, re.IGNORECASE)
            for match in matches:
                issues.append({
                    "type": "security",
                    "severity": "high",
                    "issue": issue_type.replace('_', ' ').title(),
                    "line": code[:match.start()].count('\n') + 1,
                    "message": f"Potential {issue_type.replace('_', ' ')} detected"
                })

        # Code quality issues
        if any(line for line in code.split('\n') if len(line) > 120):
            issues.append({
                "type": "style",
                "severity": "low",
                "issue": "Long Lines",
                "message": "Some lines exceed 120 characters"
            })

        # Detect TODO/FIXME
        for i, line in enumerate(code.split('\n'), 1):
            if 'TODO' in line or 'FIXME' in line:
                issues.append({
                    "type": "maintenance",
                    "severity": "medium",
                    "issue": "Unfinished Code",
                    "line": i,
                    "message": "TODO/FIXME comment found"
                })

        # Language-specific checks
        if language == 'python':
            issues.extend(self._check_python_issues(code))
        elif language in ['javascript', 'typescript']:
            issues.extend(self._check_javascript_issues(code))

        return issues

    def _check_python_issues(self, code: str) -> List[Dict[str, Any]]:
        """Python-specific issue detection."""
        issues = []

        # Check for bare except
        if re.search(r'except\s*:', code):
            issues.append({
                "type": "best_practice",
                "severity": "medium",
                "issue": "Bare Except",
                "message": "Avoid bare 'except:' clauses. Specify exception types."
            })

        # Check for mutable default arguments
        if re.search(r'def\s+\w+\([^)]*=\s*(\[\]|\{\})', code):
            issues.append({
                "type": "bug",
                "severity": "high",
                "issue": "Mutable Default Argument",
                "message": "Mutable default arguments can cause unexpected behavior"
            })

        return issues

    def _check_javascript_issues(self, code: str) -> List[Dict[str, Any]]:
        """JavaScript/TypeScript-specific issue detection."""
        issues = []

        # Check for var usage
        if re.search(r'\bvar\s+\w+', code):
            issues.append({
                "type": "best_practice",
                "severity": "low",
                "issue": "Var Usage",
                "message": "Consider using 'let' or 'const' instead of 'var'"
            })

        # Check for == instead of ===
        if re.search(r'==(?!=)', code) and '===' not in code:
            issues.append({
                "type": "best_practice",
                "severity": "medium",
                "issue": "Loose Equality",
                "message": "Use '===' instead of '==' for type-safe comparison"
            })

        return issues

    def _calculate_complexity(self, code: str, language: str) -> int:
        """
        Calculate code complexity score (simplified cyclomatic complexity).

        Returns:
            Complexity score (1-10, where 1 is simple and 10 is complex)
        """
        complexity = 1

        # Count control flow statements
        control_patterns = [
            r'\bif\b', r'\belse\b', r'\belif\b', r'\bfor\b', r'\bwhile\b',
            r'\bswitch\b', r'\bcase\b', r'\bcatch\b', r'\b&&\b', r'\|\|'
        ]

        for pattern in control_patterns:
            complexity += len(re.findall(pattern, code, re.IGNORECASE))

        # Normalize to 1-10 scale
        normalized = min(10, max(1, complexity // 5 + 1))

        return normalized

    def _calculate_quality_score(
        self,
        metrics: Dict[str, int],
        issues: List[Dict[str, Any]],
        complexity: int
    ) -> int:
        """
        Calculate overall code quality score (0-100).

        Args:
            metrics: Code metrics
            issues: Detected issues
            complexity: Complexity score

        Returns:
            Quality score from 0 (poor) to 100 (excellent)
        """
        score = 100

        # Penalize for issues
        severity_penalties = {
            'high': 15,
            'medium': 8,
            'low': 3
        }

        for issue in issues:
            penalty = severity_penalties.get(issue.get('severity', 'low'), 5)
            score -= penalty

        # Penalize for high complexity
        if complexity > 7:
            score -= (complexity - 7) * 5

        # Penalize for very long lines
        if metrics['max_line_length'] > 120:
            score -= 10

        # Bonus for comments
        if metrics['total_lines'] > 0:
            comment_ratio = metrics['comment_lines'] / metrics['total_lines']
            if 0.1 <= comment_ratio <= 0.3:
                score += 10

        # Ensure score is between 0 and 100
        return max(0, min(100, score))


# Global instance
_code_analyzer: Optional[CodeAnalyzer] = None


def get_code_analyzer() -> CodeAnalyzer:
    """
    Get or create the CodeAnalyzer instance (Singleton pattern).

    Returns:
        CodeAnalyzer: The code analyzer instance
    """
    global _code_analyzer
    if _code_analyzer is None:
        _code_analyzer = CodeAnalyzer()
    return _code_analyzer
