"""
Migration Engine for automated code migrations
"""
from typing import Dict, List, Any, Optional
from backend.services.llm_service import llm_service
from backend.utils.logger import get_logger
import re

logger = get_logger(__name__)


class MigrationEngine:
    """Engine for automated code migrations"""

    # Predefined migration templates
    MIGRATION_TEMPLATES = {
        "react_class_to_hooks": {
            "source": "react_class_components",
            "target": "react_hooks",
            "language": "javascript",
            "description": "Convert React class components to functional components with hooks",
        },
        "python2_to_python3": {
            "source": "python2",
            "target": "python3",
            "language": "python",
            "description": "Migrate Python 2 code to Python 3",
        },
        "jquery_to_vanilla": {
            "source": "jquery",
            "target": "vanilla_js",
            "language": "javascript",
            "description": "Replace jQuery with vanilla JavaScript",
        },
    }

    async def migrate_code(
        self,
        code: str,
        migration_type: str,
        language: str,
        source_version: Optional[str] = None,
        target_version: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Migrate code from one framework/version to another

        Args:
            code: Source code
            migration_type: Type of migration
            language: Programming language
            source_version: Source version/framework
            target_version: Target version/framework

        Returns:
            Migration results with transformed code
        """
        # Get template if exists
        template = self.MIGRATION_TEMPLATES.get(migration_type)

        if template:
            source = template["source"]
            target = template["target"]
        else:
            source = source_version or "unknown"
            target = target_version or "unknown"

        # Use LLM to suggest migration
        result = await llm_service.suggest_migration(
            code=code,
            source_framework=source,
            target_framework=target,
            language=language,
        )

        # Apply any post-processing
        if "transformed_code" in result:
            result["transformed_code"] = self._post_process_migration(
                result["transformed_code"],
                migration_type,
            )

        return result

    async def analyze_migration_scope(
        self,
        files: List[Dict[str, str]],
        migration_type: str,
    ) -> Dict[str, Any]:
        """
        Analyze the scope of a migration across multiple files

        Args:
            files: List of files with path and content
            migration_type: Type of migration

        Returns:
            Migration scope analysis
        """
        total_files = len(files)
        files_to_migrate = []
        estimated_effort = 0

        for file_info in files:
            # Check if file needs migration
            needs_migration = await self._needs_migration(
                file_info["content"],
                migration_type,
            )

            if needs_migration:
                complexity = self._estimate_complexity(file_info["content"])
                files_to_migrate.append({
                    "path": file_info["path"],
                    "complexity": complexity,
                    "estimated_hours": complexity * 0.5,  # Rough estimate
                })
                estimated_effort += complexity * 0.5

        return {
            "total_files": total_files,
            "files_to_migrate": len(files_to_migrate),
            "files": files_to_migrate,
            "estimated_effort_hours": estimated_effort,
            "migration_type": migration_type,
        }

    async def _needs_migration(self, code: str, migration_type: str) -> bool:
        """Check if code needs migration"""
        if migration_type == "react_class_to_hooks":
            # Check for React class components
            return bool(re.search(r'class\s+\w+\s+extends\s+React\.Component', code))

        elif migration_type == "python2_to_python3":
            # Check for Python 2 specific syntax
            patterns = [
                r'print\s+[^(]',  # print without parentheses
                r'\.iteritems\(\)',  # dict.iteritems()
                r'xrange\(',  # xrange
            ]
            return any(re.search(pattern, code) for pattern in patterns)

        elif migration_type == "jquery_to_vanilla":
            # Check for jQuery usage
            return bool(re.search(r'\$\(', code) or 'jQuery' in code)

        return True  # Default: assume needs migration

    def _estimate_complexity(self, code: str) -> int:
        """Estimate migration complexity (1-10)"""
        lines = len(code.splitlines())

        if lines < 50:
            return 1
        elif lines < 100:
            return 2
        elif lines < 200:
            return 3
        elif lines < 500:
            return 5
        else:
            return 8

    def _post_process_migration(self, code: str, migration_type: str) -> str:
        """Post-process migrated code"""
        if migration_type == "python2_to_python3":
            # Add Python 3 specific imports if needed
            if "print(" in code and "from __future__ import print_function" not in code:
                # Already Python 3, no future import needed
                pass

        return code

    def get_migration_template(self, migration_type: str) -> Optional[Dict[str, Any]]:
        """Get migration template by type"""
        return self.MIGRATION_TEMPLATES.get(migration_type)

    def list_available_migrations(self) -> List[Dict[str, Any]]:
        """List all available migration templates"""
        return [
            {"type": key, **value}
            for key, value in self.MIGRATION_TEMPLATES.items()
        ]


# Singleton instance
migration_engine = MigrationEngine()
