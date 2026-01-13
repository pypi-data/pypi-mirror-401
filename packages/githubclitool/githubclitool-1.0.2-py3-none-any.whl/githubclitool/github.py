import json
import time
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

import requests

@dataclass(frozen=True)
class GitHubConfig:
    Token: str
    ApiBase: str = "https://api.github.com"

class GitHubError(Exception):
    def __init__(self, StatusCode: int, Message: str, Details: Optional[Any] = None):
        super().__init__(Message)
        self.StatusCode = StatusCode
        self.Details = Details

class GitHubClient:
    def __init__(self, Config: GitHubConfig, Timeout: int = 30):
        self.Config = Config
        self.Timeout = Timeout
        self.Session = requests.Session()
        self.Session.headers.update({
            "Authorization": f"Bearer {self.Config.Token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "githubclitool/1.0.1"
        })

    def _ExtractError(self, Data: Any) -> str:
        if isinstance(Data, dict):
            M = Data.get("message")
            if M:
                return str(M)
            return json.dumps(Data, ensure_ascii=False)
        if isinstance(Data, list):
            return json.dumps(Data, ensure_ascii=False)
        return str(Data)

    def _Request(self, Method: str, Path: str, Params: Optional[Dict[str, Any]] = None, JsonBody: Optional[Dict[str, Any]] = None, Headers: Optional[Dict[str, str]] = None, Raw: bool = False) -> Any:
        Url = self.Config.ApiBase.rstrip("/") + "/" + Path.lstrip("/")
        H = self.Session.headers.copy()
        if Headers:
            H.update(Headers)
        Resp = self.Session.request(Method, Url, params=Params, json=JsonBody, headers=H, timeout=self.Timeout)
        if Resp.status_code == 204:
            return None
        if Resp.status_code == 403 and Resp.headers.get("X-RateLimit-Remaining") == "0":
            Reset = Resp.headers.get("X-RateLimit-Reset")
            if Reset and Reset.isdigit():
                Wait = max(1, int(Reset) - int(time.time()) + 1)
                time.sleep(Wait)
                Resp = self.Session.request(Method, Url, params=Params, json=JsonBody, headers=H, timeout=self.Timeout)
        if Resp.status_code >= 400:
            Ct = Resp.headers.get("Content-Type", "")
            Data = None
            if "application/json" in Ct:
                try:
                    Data = Resp.json()
                except Exception:
                    Data = Resp.text
            else:
                Data = Resp.text
            raise GitHubError(Resp.status_code, self._ExtractError(Data), Data)
        if Raw:
            return Resp.content
        Ct = Resp.headers.get("Content-Type", "")
        if "application/json" in Ct:
            try:
                return Resp.json()
            except Exception:
                return Resp.text
        return Resp.text

    def GetViewer(self) -> Dict[str, Any]:
        return self._Request("GET", "/user")

    def ListReposUser(self, PerPage: int = 100, Affiliation: str = "owner", Visibility: str = "all") -> List[Dict[str, Any]]:
        Items: List[Dict[str, Any]] = []
        Page = 1
        while True:
            Params = {
                "per_page": PerPage,
                "page": Page,
                "sort": "updated",
                "direction": "desc",
                "affiliation": Affiliation,
                "visibility": Visibility
            }
            Batch = self._Request("GET", "/user/repos", Params=Params)
            if not isinstance(Batch, list) or not Batch:
                break
            Items.extend(Batch)
            if len(Batch) < PerPage:
                break
            Page += 1
        return Items

    def GetRepo(self, Owner: str, Repo: str) -> Dict[str, Any]:
        return self._Request("GET", f"/repos/{Owner}/{Repo}")

    def GetRefSha(self, Owner: str, Repo: str, Branch: str) -> str:
        Data = self._Request("GET", f"/repos/{Owner}/{Repo}/git/ref/heads/{Branch}")
        Obj = (Data or {}).get("object", {})
        Sha = Obj.get("sha")
        if not Sha:
            raise GitHubError(500, "Missing branch sha", Data)
        return Sha

    def GetTreeRecursive(self, Owner: str, Repo: str, Sha: str) -> List[Dict[str, Any]]:
        Data = self._Request("GET", f"/repos/{Owner}/{Repo}/git/trees/{Sha}", Params={"recursive": "1"})
        Tree = (Data or {}).get("tree", [])
        if not isinstance(Tree, list):
            return []
        return Tree

    def GetBlobRaw(self, Owner: str, Repo: str, BlobSha: str) -> bytes:
        return self._Request("GET", f"/repos/{Owner}/{Repo}/git/blobs/{BlobSha}", Headers={"Accept": "application/vnd.github.raw"}, Raw=True)
