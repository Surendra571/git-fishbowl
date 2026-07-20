"""
Client module for git-fishbowl.
Handles asynchronous, zero-dependency network fetching from the GitHub API.
"""

import asyncio
import json
import urllib.error
import urllib.request


class FishbowlClient:
    def __init__(self, target_repo: str, token: str = None):
        self.target_repo = target_repo
        self.token = token
        self.base_url = f"https://api.github.com/repos/{target_repo}"

    def _build_request(self, endpoint: str) -> urllib.request.Request:
        """
        Constructs a safe Request object with the required headers.
        """
        url = f"{self.base_url}/{endpoint}"
        headers = {
            "Accept": "application/vnd.github+json",
            "User-Agent": "git-fishbowl-cli",
        }
        if self.token:
            headers["Authorization"] = f"token {self.token}"

        return urllib.request.Request(url, headers=headers)

    def _fetch_sync(self, endpoint: str) -> list:
        """
        Synchronous I/O execution block for hitting the API.
        """
        req = self._build_request(endpoint)
        try:
            with urllib.request.urlopen(req) as response:
                return json.loads(response.read().decode("utf-8"))
        except (urllib.error.HTTPError, urllib.error.URLError):
            # Return empty structure on failure to prevent pipeline crash
            return []

    async def fetch_data(self) -> tuple[list, list]:
        """
        Concurrently executes network requests for issues and pull requests
        without blocking the main event loop.
        """
        loop = asyncio.get_running_loop()

        # GitHub returns up to 100 items per page; split across two tasks
        issues_task = loop.run_in_executor(
            None, self._fetch_sync, "issues?state=open&per_page=100"
        )
        pulls_task = loop.run_in_executor(
            None, self._fetch_sync, "pulls?state=open&per_page=100"
        )

        raw_issues, raw_pulls = await asyncio.gather(issues_task, pulls_task)
        return raw_issues, raw_pulls
