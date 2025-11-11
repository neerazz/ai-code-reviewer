"""
Code Analysis Service
Multi-language static analysis and pattern detection
"""
from typing import Dict, List, Any, Optional
import re
import ast
import os
from pathlib import Path
from config.settings import settings
from backend.services.llm_service import llm_service
from backend.utils.logger import get_logger

logger = get_logger(__name__)


class CodeAnalyzer:
    """Service for analyzing code across multiple languages"""

    LANGUAGE_EXTENSIONS = {
        "python": [".py"],
        "javascript": [".js", ".jsx"],
        "typescript": [".ts", ".tsx"],
        "java": [".java"],
        "go": [".go"],
        "rust": [".rs"],
        "c++": [".cpp", ".cc", ".cxx", ".hpp", ".h"],
        "c#": [".cs"],
    }

    def __init__(self):
        self.max_file_size = settings.MAX_FILE_SIZE_MB * 1024 * 1024

    async def analyze_file(
        self,
        file_path: str,
        content: str,
        context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Analyze a single file

        Args:
            file_path: Path to file
            content: File content
            context: Additional context

        Returns:
            Analysis results
        """
        # Detect language
        language = self._detect_language(file_path)
        if not language:
            return {"error": "Unsupported file type"}

        # Check file size
        if len(content.encode("utf-8")) > self.max_file_size:
            return {"error": f"File too large (max {settings.MAX_FILE_SIZE_MB}MB)"}

        # Perform static analysis
        static_analysis = self._static_analysis(content, language)

        # Get LLM review
        llm_review = await llm_service.review_code(
            code=content,
            file_path=file_path,
            language=language,
            context=context,
        )

        # Detect patterns
        patterns = await llm_service.detect_patterns(
            code=content,
            language=language,
        )

        return {
            "file_path": file_path,
            "language": language,
            "lines_of_code": len(content.splitlines()),
            "static_analysis": static_analysis,
            "llm_review": llm_review,
            "patterns": patterns,
        }

    async def analyze_directory(
        self,
        directory_path: str,
        exclude_patterns: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        Analyze all code files in a directory

        Args:
            directory_path: Path to directory
            exclude_patterns: Patterns to exclude (e.g., "*/tests/*")

        Returns:
            Analysis results for all files
        """
        if exclude_patterns is None:
            exclude_patterns = ["*/node_modules/*", "*/.venv/*", "*/venv/*", "*/__pycache__/*"]

        results = []
        total_files = 0
        total_lines = 0

        for root, _, files in os.walk(directory_path):
            for file in files:
                file_path = os.path.join(root, file)

                # Check if should be excluded
                if self._should_exclude(file_path, exclude_patterns):
                    continue

                # Check if supported language
                if not self._detect_language(file_path):
                    continue

                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()

                    analysis = await self.analyze_file(file_path, content)
                    results.append(analysis)

                    total_files += 1
                    total_lines += analysis.get("lines_of_code", 0)

                except Exception as e:
                    logger.error(f"Error analyzing {file_path}: {str(e)}")
                    results.append({"file_path": file_path, "error": str(e)})

        return {
            "total_files": total_files,
            "total_lines": total_lines,
            "files": results,
        }

    def _detect_language(self, file_path: str) -> Optional[str]:
        """Detect programming language from file extension"""
        ext = Path(file_path).suffix.lower()
        for lang, extensions in self.LANGUAGE_EXTENSIONS.items():
            if ext in extensions:
                return lang
        return None

    def _static_analysis(self, content: str, language: str) -> Dict[str, Any]:
        """Perform static analysis based on language"""
        if language == "python":
            return self._analyze_python(content)
        elif language in ["javascript", "typescript"]:
            return self._analyze_javascript(content)
        else:
            return self._generic_analysis(content)

    def _analyze_python(self, content: str) -> Dict[str, Any]:
        """Python-specific static analysis"""
        issues = []

        try:
            # Parse AST
            tree = ast.parse(content)

            # Check for common issues
            for node in ast.walk(tree):
                # Check for bare except
                if isinstance(node, ast.ExceptHandler) and node.type is None:
                    issues.append({
                        "line": node.lineno,
                        "severity": "warning",
                        "category": "best_practice",
                        "title": "Bare except clause",
                        "description": "Using bare 'except:' can catch system exits and keyboard interrupts",
                    })

                # Check for TODO comments
                if isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant):
                    if "TODO" in str(node.value.value):
                        issues.append({
                            "line": node.lineno,
                            "severity": "info",
                            "category": "technical_debt",
                            "title": "TODO comment found",
                            "description": str(node.value.value),
                        })

        except SyntaxError as e:
            issues.append({
                "line": e.lineno,
                "severity": "error",
                "category": "syntax",
                "title": "Syntax Error",
                "description": str(e),
            })

        return {
            "issues": issues,
            "complexity": self._calculate_complexity(content),
        }

    def _analyze_javascript(self, content: str) -> Dict[str, Any]:
        """JavaScript/TypeScript static analysis"""
        issues = []

        # Check for console.log (should not be in production)
        for i, line in enumerate(content.splitlines(), 1):
            if "console.log" in line and "//" not in line.split("console.log")[0]:
                issues.append({
                    "line": i,
                    "severity": "warning",
                    "category": "best_practice",
                    "title": "Console.log found",
                    "description": "Remove console.log before production",
                })

            # Check for var usage (should use let/const)
            if re.search(r'\bvar\s+\w+', line):
                issues.append({
                    "line": i,
                    "severity": "info",
                    "category": "code_style",
                    "title": "Use let or const instead of var",
                    "description": "var has function scope, use let or const for block scope",
                })

        return {
            "issues": issues,
            "complexity": self._calculate_complexity(content),
        }

    def _generic_analysis(self, content: str) -> Dict[str, Any]:
        """Generic analysis for any language"""
        issues = []

        # Check for common issues
        for i, line in enumerate(content.splitlines(), 1):
            # Check for hardcoded credentials
            if re.search(r'(password|secret|api_key|token)\s*=\s*["\'].+["\']', line, re.I):
                issues.append({
                    "line": i,
                    "severity": "critical",
                    "category": "security",
                    "title": "Potential hardcoded credentials",
                    "description": "Credentials should not be hardcoded",
                })

            # Check for TODO/FIXME
            if re.search(r'(TODO|FIXME|XXX|HACK)', line, re.I):
                issues.append({
                    "line": i,
                    "severity": "info",
                    "category": "technical_debt",
                    "title": "Technical debt marker",
                    "description": line.strip(),
                })

        return {
            "issues": issues,
            "complexity": self._calculate_complexity(content),
        }

    def _calculate_complexity(self, content: str) -> Dict[str, int]:
        """Calculate basic complexity metrics"""
        lines = content.splitlines()
        return {
            "total_lines": len(lines),
            "code_lines": len([l for l in lines if l.strip() and not l.strip().startswith("#")]),
            "comment_lines": len([l for l in lines if l.strip().startswith("#")]),
            "blank_lines": len([l for l in lines if not l.strip()]),
        }

    def _should_exclude(self, file_path: str, exclude_patterns: List[str]) -> bool:
        """Check if file should be excluded based on patterns"""
        from fnmatch import fnmatch
        for pattern in exclude_patterns:
            if fnmatch(file_path, pattern):
                return True
        return False


# Singleton instance
code_analyzer = CodeAnalyzer()
