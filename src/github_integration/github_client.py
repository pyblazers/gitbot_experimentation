"""
GitHub integration for AI agents.
"""
from typing import Optional, List, Dict, Any
from github import Github, Repository, Issue, PullRequest
from git import Repo
import os


class GitHubClient:
    """GitHub client for repository operations."""
    
    def __init__(self, token: str):
        """Initialize GitHub client with access token."""
        self.github = Github(token)
        self.user = self.github.get_user()
    
    def get_repository(self, repo_name: str) -> Repository.Repository:
        """Get a repository by name (format: owner/repo)."""
        return self.github.get_repo(repo_name)
    
    def list_repositories(self) -> List[Repository.Repository]:
        """List all repositories accessible to the user."""
        return list(self.user.get_repos())
    
    def get_issues(self, repo_name: str, state: str = "open") -> List[Issue.Issue]:
        """Get issues from a repository."""
        repo = self.get_repository(repo_name)
        return list(repo.get_issues(state=state))
    
    def get_pull_requests(self, repo_name: str, state: str = "open") -> List[PullRequest.PullRequest]:
        """Get pull requests from a repository."""
        repo = self.get_repository(repo_name)
        return list(repo.get_pulls(state=state))
    
    def create_issue(self, repo_name: str, title: str, body: str, 
                     labels: Optional[List[str]] = None) -> Issue.Issue:
        """Create a new issue in a repository."""
        repo = self.get_repository(repo_name)
        return repo.create_issue(title=title, body=body, labels=labels or [])
    
    def comment_on_issue(self, repo_name: str, issue_number: int, comment: str):
        """Add a comment to an issue."""
        repo = self.get_repository(repo_name)
        issue = repo.get_issue(issue_number)
        issue.create_comment(comment)
    
    def comment_on_pull_request(self, repo_name: str, pr_number: int, comment: str):
        """Add a comment to a pull request."""
        repo = self.get_repository(repo_name)
        pr = repo.get_pull(pr_number)
        pr.create_issue_comment(comment)
    
    def get_file_content(self, repo_name: str, file_path: str, ref: str = "main") -> str:
        """Get the content of a file from a repository."""
        repo = self.get_repository(repo_name)
        content = repo.get_contents(file_path, ref=ref)
        return content.decoded_content.decode('utf-8')
    
    def create_pull_request(self, repo_name: str, title: str, body: str, 
                           head: str, base: str = "main") -> PullRequest.PullRequest:
        """Create a new pull request."""
        repo = self.get_repository(repo_name)
        return repo.create_pull(title=title, body=body, head=head, base=base)
    
    def get_repository_info(self, repo_name: str) -> Dict[str, Any]:
        """Get comprehensive information about a repository."""
        repo = self.get_repository(repo_name)
        return {
            "name": repo.name,
            "full_name": repo.full_name,
            "description": repo.description,
            "url": repo.html_url,
            "stars": repo.stargazers_count,
            "forks": repo.forks_count,
            "open_issues": repo.open_issues_count,
            "default_branch": repo.default_branch,
            "language": repo.language,
            "topics": repo.get_topics(),
        }


class GitOperations:
    """Git operations for local repository management."""
    
    @staticmethod
    def clone_repository(repo_url: str, local_path: str) -> Repo:
        """Clone a repository to a local path."""
        return Repo.clone_from(repo_url, local_path)
    
    @staticmethod
    def open_repository(local_path: str) -> Repo:
        """Open an existing local repository."""
        return Repo(local_path)
    
    @staticmethod
    def get_current_branch(repo: Repo) -> str:
        """Get the current branch name."""
        return repo.active_branch.name
    
    @staticmethod
    def create_branch(repo: Repo, branch_name: str):
        """Create a new branch."""
        repo.git.checkout('-b', branch_name)
    
    @staticmethod
    def commit_changes(repo: Repo, message: str):
        """Commit all changes with a message."""
        repo.git.add(A=True)
        repo.index.commit(message)
    
    @staticmethod
    def push_changes(repo: Repo, branch: Optional[str] = None):
        """Push changes to remote."""
        if branch:
            repo.git.push('origin', branch)
        else:
            repo.git.push()
    
    @staticmethod
    def pull_changes(repo: Repo):
        """Pull changes from remote."""
        repo.git.pull()
    
    @staticmethod
    def get_diff(repo: Repo, ref1: str = "HEAD", ref2: Optional[str] = None) -> str:
        """Get diff between refs."""
        if ref2:
            return repo.git.diff(ref1, ref2)
        return repo.git.diff(ref1)
