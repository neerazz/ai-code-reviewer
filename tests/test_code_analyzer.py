"""
Tests for Code Analyzer Service
"""
import pytest
from backend.services.code_analyzer import CodeAnalyzer


@pytest.fixture
def analyzer():
    """Create CodeAnalyzer instance"""
    return CodeAnalyzer()


def test_detect_language_python(analyzer):
    """Test Python language detection"""
    assert analyzer._detect_language("test.py") == "python"
    assert analyzer._detect_language("script.py") == "python"


def test_detect_language_javascript(analyzer):
    """Test JavaScript language detection"""
    assert analyzer._detect_language("app.js") == "javascript"
    assert analyzer._detect_language("component.jsx") == "javascript"


def test_detect_language_typescript(analyzer):
    """Test TypeScript language detection"""
    assert analyzer._detect_language("app.ts") == "typescript"
    assert analyzer._detect_language("component.tsx") == "typescript"


def test_detect_language_unsupported(analyzer):
    """Test unsupported file type"""
    assert analyzer._detect_language("readme.txt") is None
    assert analyzer._detect_language("image.png") is None


@pytest.mark.asyncio
async def test_analyze_python_file(analyzer):
    """Test analyzing Python file"""
    code = '''
def hello():
    print("Hello World")

# TODO: Add more features
'''

    result = await analyzer.analyze_file(
        file_path="test.py",
        content=code,
    )

    assert result["language"] == "python"
    assert result["lines_of_code"] > 0
    assert "static_analysis" in result


def test_calculate_complexity(analyzer):
    """Test complexity calculation"""
    code = '''
def test():
    # Comment
    pass


'''

    complexity = analyzer._calculate_complexity(code)

    assert complexity["total_lines"] > 0
    assert complexity["code_lines"] >= 0
    assert complexity["comment_lines"] >= 0
    assert complexity["blank_lines"] >= 0


def test_should_exclude(analyzer):
    """Test file exclusion"""
    exclude_patterns = ["*/node_modules/*", "*/__pycache__/*"]

    assert analyzer._should_exclude("node_modules/test.js", exclude_patterns)
    assert analyzer._should_exclude("src/__pycache__/test.pyc", exclude_patterns)
    assert not analyzer._should_exclude("src/main.py", exclude_patterns)
