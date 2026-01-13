import re
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

from .github import GitHubClient, GitHubError

@dataclass(frozen=True)
class SecretRule:
    Name: str
    Pattern: re.Pattern

def BuildRules() -> List[SecretRule]:
    return [
        SecretRule("AWSAccessKeyId", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
        SecretRule("AWSSecretKey", re.compile(r"(?i)\baws(.{0,20})?(secret|access)[_-]?key(.{0,20})?['\"=:\s]{1,6}([0-9a-zA-Z/+]{40})\b")),
        SecretRule("GitHubTokenClassic", re.compile(r"\bghp_[A-Za-z0-9]{36}\b")),
        SecretRule("GitHubTokenFineGrained", re.compile(r"\bgithub_pat_[A-Za-z0-9_]{80,}\b")),
        SecretRule("SlackToken", re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}\b")),
        SecretRule("PrivateKeyBlock", re.compile(r"-----BEGIN (RSA|EC|OPENSSH|DSA|PRIVATE) KEY-----")),
        SecretRule("JWT", re.compile(r"\beyJ[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,}\b")),
        SecretRule("GenericApiKeyAssign", re.compile(r"(?i)\b(api[_-]?key|secret|token|password)\b.{0,20}['\"=:\s]{1,6}([A-Za-z0-9_\-]{16,})")),
    ]

def MaskSecret(S: str) -> str:
    S = S.strip()
    if len(S) <= 8:
        return "*" * len(S)
    return f"{S[:4]}***{S[-4:]}"

def ExtractMatches(Rule: SecretRule, Text: str) -> List[str]:
    Out: List[str] = []
    for M in Rule.Pattern.finditer(Text):
        G = None
        if M.lastindex:
            G = M.group(M.lastindex) if M.lastindex >= 1 else M.group(0)
        else:
            G = M.group(0)
        if G:
            Out.append(G)
    return Out

def ShouldScanPath(Path: str) -> bool:
    P = Path.lower()
    if P.endswith((".png", ".jpg", ".jpeg", ".gif", ".webp", ".mp4", ".mov", ".avi", ".zip", ".rar", ".7z", ".pdf")):
        return False
    if P.endswith((".lock", ".min.js", ".min.css")):
        return False
    return True

def IsHighSignalPath(Path: str) -> bool:
    P = Path.lower()
    if any(x in P for x in [".env", "config", "secret", "token", "credential", "private", "id_rsa", ".pem", ".key"]):
        return True
    if P.endswith((".py", ".js", ".ts", ".json", ".yml", ".yaml", ".toml", ".ini", ".env", ".sh", ".ps1", ".cfg", ".conf")):
        return True
    return False

def ScanRepo(Client: GitHubClient, Owner: str, Repo: str, MaxFiles: int = 350, MaxBytes: int = 200_000) -> List[Dict[str, Any]]:
    RepoInfo = Client.GetRepo(Owner, Repo)
    Branch = RepoInfo.get("default_branch") or "main"
    Sha = Client.GetRefSha(Owner, Repo, Branch)
    Tree = Client.GetTreeRecursive(Owner, Repo, Sha)

    Files: List[Dict[str, Any]] = []
    for N in Tree:
        if N.get("type") != "blob":
            continue
        Path = str(N.get("path", ""))
        Size = int(N.get("size") or 0)
        if not Path or not ShouldScanPath(Path):
            continue
        if Size <= 0 or Size > MaxBytes:
            continue
        Score = 2 if IsHighSignalPath(Path) else 1
        Files.append({"path": Path, "sha": N.get("sha"), "size": Size, "score": Score})

    Files.sort(key=lambda x: (-x["score"], x["size"], x["path"]))
    Files = Files[:MaxFiles]

    Rules = BuildRules()
    Findings: List[Dict[str, Any]] = []

    for F in Files:
        BlobSha = F.get("sha")
        if not BlobSha:
            continue
        try:
            Raw = Client.GetBlobRaw(Owner, Repo, BlobSha)
        except GitHubError:
            continue
        if not Raw:
            continue
        try:
            Text = Raw.decode("utf-8", errors="ignore")
        except Exception:
            continue
        if not Text.strip():
            continue

        for Rule in Rules:
            Matches = ExtractMatches(Rule, Text)
            if not Matches:
                continue
            Samples = []
            Seen = set()
            for V in Matches:
                MV = MaskSecret(V)
                if MV in Seen:
                    continue
                Seen.add(MV)
                Samples.append(MV)
                if len(Samples) >= 3:
                    break
            Findings.append({
                "repo": f"{Owner}/{Repo}",
                "path": F["path"],
                "rule": Rule.Name,
                "samples": Samples
            })

    return Findings

def ScanAccount(Client: GitHubClient, Affiliation: str = "owner", Visibility: str = "all", LimitRepos: int = 200, MaxFiles: int = 350, MaxBytes: int = 200_000) -> Dict[str, Any]:
    Repos = Client.ListReposUser(Affiliation=Affiliation, Visibility=Visibility)
    if LimitRepos > 0:
        Repos = Repos[:LimitRepos]

    AllFindings: List[Dict[str, Any]] = []
    Failed: List[Dict[str, Any]] = []

    for R in Repos:
        Full = str(R.get("full_name", "")).strip()
        if not Full or "/" not in Full:
            continue
        Owner, Repo = Full.split("/", 1)
        try:
            Fs = ScanRepo(Client, Owner, Repo, MaxFiles=MaxFiles, MaxBytes=MaxBytes)
            AllFindings.extend(Fs)
        except GitHubError as E:
            Failed.append({"repo": Full, "status": E.StatusCode, "message": str(E)})

    return {"repos_scanned": len(Repos), "findings": AllFindings, "failed": Failed}
