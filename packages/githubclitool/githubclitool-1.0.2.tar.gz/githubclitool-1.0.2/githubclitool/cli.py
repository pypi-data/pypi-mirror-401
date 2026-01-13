import argparse
import json
import os
import sys
import time
import re
from dataclasses import dataclass
from typing import Any, Dict, List, Optional
from githubclitool.tokenstore import GetToken, SaveToken

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
            "User-Agent": "ght/1.0.1"
        })

    def _Request(self, Method: str, Path: str, Params=None, JsonBody=None, Headers=None, Raw=False):
        Url = self.Config.ApiBase.rstrip("/") + "/" + Path.lstrip("/")
        H = self.Session.headers.copy()
        if Headers:
            H.update(Headers)
        R = self.Session.request(Method, Url, params=Params, json=JsonBody, headers=H, timeout=self.Timeout)
        if R.status_code == 204:
            return None
        if R.status_code >= 400:
            try:
                D = R.json()
            except:
                D = R.text
            raise GitHubError(R.status_code, str(D), D)
        if Raw:
            return R.content
        try:
            return R.json()
        except:
            return R.text

    def GetViewer(self):
        return self._Request("GET", "/user")

    def ListRepos(self, Scope):
        Out = []
        Page = 1
        while True:
            if Scope == "user":
                Path = "/user/repos"
                Params = {"per_page": 100, "page": Page}
            else:
                Org = Scope.split(":", 1)[1]
                Path = f"/orgs/{Org}/repos"
                Params = {"per_page": 100, "page": Page, "type": "all"}
            B = self._Request("GET", Path, Params=Params)
            if not B:
                break
            Out.extend(B)
            if len(B) < 100:
                break
            Page += 1
        return Out

    def CreateRepoUser(self, Name, Private, Desc, AutoInit, Gitignore, License):
        Body = {"name": Name, "private": Private, "description": Desc, "auto_init": AutoInit}
        if Gitignore:
            Body["gitignore_template"] = Gitignore
        if License:
            Body["license_template"] = License
        return self._Request("POST", "/user/repos", JsonBody=Body)

    def CreateRepoOrg(self, Org, Name, Private, Desc, AutoInit, Gitignore, License):
        Body = {"name": Name, "private": Private, "description": Desc, "auto_init": AutoInit}
        if Gitignore:
            Body["gitignore_template"] = Gitignore
        if License:
            Body["license_template"] = License
        return self._Request("POST", f"/orgs/{Org}/repos", JsonBody=Body)

    def DeleteRepo(self, Owner, Repo):
        self._Request("DELETE", f"/repos/{Owner}/{Repo}")

    def RenameRepo(self, Owner, Repo, NewName):
        return self._Request("PATCH", f"/repos/{Owner}/{Repo}", JsonBody={"name": NewName})

    def SetTopics(self, Owner, Repo, Topics):
        return self._Request(
            "PUT",
            f"/repos/{Owner}/{Repo}/topics",
            Headers={"Accept": "application/vnd.github+json"},
            JsonBody={"names": Topics}
        )

    def AddCollab(self, Owner, Repo, User, Perm):
        return self._Request("PUT", f"/repos/{Owner}/{Repo}/collaborators/{User}", JsonBody={"permission": Perm})

    def RemoveCollab(self, Owner, Repo, User):
        self._Request("DELETE", f"/repos/{Owner}/{Repo}/collaborators/{User}")

    def SetDefaultBranch(self, Owner, Repo, Branch):
        return self._Request("PATCH", f"/repos/{Owner}/{Repo}", JsonBody={"default_branch": Branch})

    def GetTree(self, Owner, Repo, Branch):
        Ref = self._Request("GET", f"/repos/{Owner}/{Repo}/git/ref/heads/{Branch}")
        Sha = Ref["object"]["sha"]
        Tree = self._Request("GET", f"/repos/{Owner}/{Repo}/git/trees/{Sha}", Params={"recursive": 1})
        return Tree.get("tree", [])

    def GetBlob(self, Owner, Repo, Sha):
        return self._Request("GET", f"/repos/{Owner}/{Repo}/git/blobs/{Sha}", Headers={"Accept": "application/vnd.github.raw"}, Raw=True)

def LoadToken(ArgToken):
    if ArgToken:
        SaveToken(ArgToken.strip())
        return ArgToken.strip()

    T=GetToken()
    if T:
        return T

    sys.stdout.write("GitHub Token not found. Paste token: ")
    sys.stdout.flush()
    T=sys.stdin.readline().strip()

    if not T:
        raise SystemExit("Token required")

    SaveToken(T)
    return T

def PrintJson(O):
    sys.stdout.write(json.dumps(O, indent=2, ensure_ascii=False) + "\n")

def ReadLine(P):
    sys.stdout.write(P)
    sys.stdout.flush()
    return sys.stdin.readline().strip()

SecretRules = [
    re.compile(r"ghp_[A-Za-z0-9]{36}"),
    re.compile(r"github_pat_[A-Za-z0-9_]{80,}"),
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"-----BEGIN (RSA|OPENSSH|EC|DSA) PRIVATE KEY-----"),
]

def ScanAccount(Client, Limit):
    Repos = Client.ListRepos("user")[:Limit]
    Findings = []
    for R in Repos:
        Owner, Repo = R["full_name"].split("/", 1)
        Branch = R.get("default_branch", "main")
        try:
            Tree = Client.GetTree(Owner, Repo, Branch)
        except:
            continue
        for F in Tree:
            if F["type"] != "blob" or F.get("size", 0) > 200000:
                continue
            try:
                Raw = Client.GetBlob(Owner, Repo, F["sha"]).decode("utf-8", "ignore")
            except:
                continue
            for Rule in SecretRules:
                if Rule.search(Raw):
                    Findings.append({"repo": f"{Owner}/{Repo}", "path": F["path"], "rule": Rule.pattern})
    return Findings

def BuildParser():
    P = argparse.ArgumentParser(prog="ght")
    P.add_argument("--token")
    Sub = P.add_subparsers(dest="cmd", required=True)

    Me = Sub.add_parser("me")
    Me.add_argument("--account", action="store_true")
    Me.add_argument("--secretscanner", action="store_true")
    Me.add_argument("--yes", action="store_true")
    Me.add_argument("--limit-repos", type=int, default=100)

    L = Sub.add_parser("list")
    L.add_argument("--scope", default="user")

    C = Sub.add_parser("create")
    C.add_argument("name")
    C.add_argument("--org")
    C.add_argument("--private", action="store_true")
    C.add_argument("--public", action="store_true")
    C.add_argument("--desc", default="")
    C.add_argument("--no-init", action="store_true")
    C.add_argument("--gitignore")
    C.add_argument("--license")

    D = Sub.add_parser("delete")
    D.add_argument("owner", nargs="?")
    D.add_argument("repo", nargs="?")
    D.add_argument("--yes", action="store_true")

    R = Sub.add_parser("rename")
    R.add_argument("owner")
    R.add_argument("repo")
    R.add_argument("newName")

    T = Sub.add_parser("topics")
    T.add_argument("owner")
    T.add_argument("repo")
    T.add_argument("topics", nargs="*")

    A = Sub.add_parser("add-collab")
    A.add_argument("owner")
    A.add_argument("repo")
    A.add_argument("user")
    A.add_argument("--perm", default="push")

    Rc = Sub.add_parser("remove-collab")
    Rc.add_argument("owner")
    Rc.add_argument("repo")
    Rc.add_argument("user")

    Db = Sub.add_parser("default-branch")
    Db.add_argument("owner")
    Db.add_argument("repo")
    Db.add_argument("branch")

    return P

def Main():
    Args = BuildParser().parse_args()
    Client = GitHubClient(GitHubConfig(LoadToken(Args.token)))

    if Args.cmd == "me":
        Out = {}
        V = Client.GetViewer()
        if Args.account or not Args.secretscanner:
            Out["account"] = V
        if Args.secretscanner:
            if not Args.yes:
                if ReadLine("Type SCAN: ") != "SCAN":
                    return
            F = ScanAccount(Client, Args.limit_repos)
            Out["secrets_found"] = len(F)
            Out["findings"] = F
        PrintJson(Out)
        return

    if Args.cmd == "list":
        PrintJson(Client.ListRepos(Args.scope))
        return

    if Args.cmd == "create":
        Private = Args.private and not Args.public
        AutoInit = not Args.no_init
        if Args.org:
            R = Client.CreateRepoOrg(Args.org, Args.name, Private, Args.desc, AutoInit, Args.gitignore, Args.license)
        else:
            R = Client.CreateRepoUser(Args.name, Private, Args.desc, AutoInit, Args.gitignore, Args.license)
        PrintJson(R)
        return

    if Args.cmd == "delete":
        if not Args.yes:
            if ReadLine(f"Type {Args.owner}/{Args.repo}: ") != f"{Args.owner}/{Args.repo}":
                return
        Client.DeleteRepo(Args.owner, Args.repo)
        return

    if Args.cmd == "rename":
        PrintJson(Client.RenameRepo(Args.owner, Args.repo, Args.newName))
        return

    if Args.cmd == "topics":
        PrintJson(Client.SetTopics(Args.owner, Args.repo, Args.topics))
        return

    if Args.cmd == "add-collab":
        PrintJson(Client.AddCollab(Args.owner, Args.repo, Args.user, Args.perm))
        return

    if Args.cmd == "remove-collab":
        Client.RemoveCollab(Args.owner, Args.repo, Args.user)
        return

    if Args.cmd == "default-branch":
        PrintJson(Client.SetDefaultBranch(Args.owner, Args.repo, Args.branch))
        return

if __name__ == "__main__":
    Main()