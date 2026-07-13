import base64
from typing import Any
import httpx
from app.core.config import Settings

class GitHubService:
    API_ROOT = "https://api.github.com"
    def __init__(self, settings: Settings): self.settings = settings
    def _headers(self):
        headers = {"Accept":"application/vnd.github+json", "X-GitHub-Api-Version":"2022-11-28", "User-Agent":"ai-coding-agent"}
        if self.settings.github_token: headers["Authorization"] = f"Bearer {self.settings.github_token}"
        return headers
    async def _request(self, method: str, path: str, **kwargs) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.request(method, self.API_ROOT + path, headers=self._headers(), **kwargs)
            response.raise_for_status()
            return response.json()
    async def get_issue(self, owner: str, repo: str, number: int):
        return await self._request("GET", f"/repos/{owner}/{repo}/issues/{number}")
    async def get_repository_tree(self, owner: str, repo: str, ref: str = "HEAD"):
        data = await self._request("GET", f"/repos/{owner}/{repo}/git/trees/{ref}", params={"recursive":"1"})
        return data.get("tree", [])
    async def get_file(self, owner: str, repo: str, path: str, ref: str | None = None):
        data = await self._request("GET", f"/repos/{owner}/{repo}/contents/{path}", params={"ref":ref} if ref else None)
        return base64.b64decode(data.get("content", "")).decode("utf-8", errors="replace")
    async def create_branch(self, owner: str, repo: str, branch: str, from_ref: str):
        if not self.settings.allow_pr_creation: raise PermissionError("Pull request creation is disabled.")
        source = await self._request("GET", f"/repos/{owner}/{repo}/git/ref/heads/{from_ref}")
        await self._request("POST", f"/repos/{owner}/{repo}/git/refs", json={"ref":f"refs/heads/{branch}", "sha":source["object"]["sha"]})
    async def update_file(self, owner: str, repo: str, path: str, branch: str, content: str, message: str, sha: str | None = None):
        if not self.settings.allow_pr_creation: raise PermissionError("Pull request creation is disabled.")
        body = {"message":message, "content":base64.b64encode(content.encode()).decode(), "branch":branch}
        if sha: body["sha"] = sha
        return await self._request("PUT", f"/repos/{owner}/{repo}/contents/{path}", json=body)
    async def create_pull_request(self, owner: str, repo: str, title: str, body: str, head: str, base: str):
        if not self.settings.allow_pr_creation: raise PermissionError("Pull request creation is disabled.")
        data = await self._request("POST", f"/repos/{owner}/{repo}/pulls", json={"title":title,"body":body,"head":head,"base":base})
        return data["html_url"]
