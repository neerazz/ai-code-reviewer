"""
GitHub integration service
"""
from typing import Dict, List, Any, Optional
from github import Github, GithubException
from config.settings import settings
from backend.utils.logger import get_logger

logger = get_logger(__name__)


class GitHubService:
    """Service for GitHub integration"""

    def __init__(self):
        if settings.GITHUB_TOKEN:
            self.client = Github(settings.GITHUB_TOKEN)
        else:
            self.client = None
            logger.warning("GitHub token not configured")

    def get_pull_request(self, repo_name: str, pr_number: int) -> Optional[Dict[str, Any]]:
        """
        Get pull request details

        Args:
            repo_name: Repository name (owner/repo)
            pr_number: Pull request number

        Returns:
            PR details
        """
        if not self.client:
            return None

        try:
            repo = self.client.get_repo(repo_name)
            pr = repo.get_pull(pr_number)

            return {
                "number": pr.number,
                "title": pr.title,
                "description": pr.body,
                "state": pr.state,
                "author": pr.user.login,
                "created_at": pr.created_at.isoformat(),
                "updated_at": pr.updated_at.isoformat(),
                "head_sha": pr.head.sha,
                "base_branch": pr.base.ref,
                "head_branch": pr.head.ref,
                "files_changed": pr.changed_files,
                "additions": pr.additions,
                "deletions": pr.deletions,
            }

        except GithubException as e:
            logger.error(f"Error getting PR: {str(e)}")
            return None

    def get_pr_files(self, repo_name: str, pr_number: int) -> List[Dict[str, Any]]:
        """
        Get files changed in a pull request

        Args:
            repo_name: Repository name
            pr_number: Pull request number

        Returns:
            List of changed files
        """
        if not self.client:
            return []

        try:
            repo = self.client.get_repo(repo_name)
            pr = repo.get_pull(pr_number)

            files = []
            for file in pr.get_files():
                files.append({
                    "filename": file.filename,
                    "status": file.status,
                    "additions": file.additions,
                    "deletions": file.deletions,
                    "changes": file.changes,
                    "patch": file.patch,
                    "raw_url": file.raw_url,
                })

            return files

        except GithubException as e:
            logger.error(f"Error getting PR files: {str(e)}")
            return []

    def get_file_content(self, repo_name: str, file_path: str, ref: str = "main") -> Optional[str]:
        """
        Get file content from repository

        Args:
            repo_name: Repository name
            file_path: Path to file
            ref: Branch/commit reference

        Returns:
            File content
        """
        if not self.client:
            return None

        try:
            repo = self.client.get_repo(repo_name)
            content = repo.get_contents(file_path, ref=ref)
            return content.decoded_content.decode("utf-8")

        except GithubException as e:
            logger.error(f"Error getting file content: {str(e)}")
            return None

    def create_review_comment(
        self,
        repo_name: str,
        pr_number: int,
        commit_id: str,
        file_path: str,
        line: int,
        comment: str,
    ) -> bool:
        """
        Create a review comment on a PR

        Args:
            repo_name: Repository name
            pr_number: Pull request number
            commit_id: Commit SHA
            file_path: File path
            line: Line number
            comment: Comment text

        Returns:
            Success status
        """
        if not self.client:
            return False

        try:
            repo = self.client.get_repo(repo_name)
            pr = repo.get_pull(pr_number)

            pr.create_review_comment(
                body=comment,
                commit=repo.get_commit(commit_id),
                path=file_path,
                line=line,
            )

            return True

        except GithubException as e:
            logger.error(f"Error creating review comment: {str(e)}")
            return False

    def create_issue(
        self,
        repo_name: str,
        title: str,
        body: str,
        labels: Optional[List[str]] = None,
    ) -> Optional[int]:
        """
        Create an issue for technical debt

        Args:
            repo_name: Repository name
            title: Issue title
            body: Issue body
            labels: Labels to add

        Returns:
            Issue number if successful
        """
        if not self.client:
            return None

        try:
            repo = self.client.get_repo(repo_name)
            issue = repo.create_issue(
                title=title,
                body=body,
                labels=labels or [],
            )

            return issue.number

        except GithubException as e:
            logger.error(f"Error creating issue: {str(e)}")
            return None

    def get_repository_languages(self, repo_name: str) -> Dict[str, int]:
        """Get programming languages used in repository"""
        if not self.client:
            return {}

        try:
            repo = self.client.get_repo(repo_name)
            return repo.get_languages()

        except GithubException as e:
            logger.error(f"Error getting repository languages: {str(e)}")
            return {}


# Singleton instance
github_service = GitHubService()
