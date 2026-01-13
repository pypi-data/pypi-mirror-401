import argparse
import sys
from typing import Any, Dict, Optional

from .github import GitHubClient, GitHubConfig, GitHubError
from .secretscanner import ScanAccount
from .utils import LoadToken, PrintJson, ReadLine

def BuildParser() -> argparse.ArgumentParser:
    P = argparse.ArgumentParser(prog="ght", add_help=True)
    P.add_argument("--token", default=None)
    P.add_argument("--timeout", type=int, default=30)
    Sub = P.add_subparsers(dest="cmd", required=True)

    Me = Sub.add_parser("me")
    Me.add_argument("--account", action="store_true")
    Me.add_argument("--secretscanner", action="store_true")
    Me.add_argument("--yes", action="store_true")
    Me.add_argument("--affiliation", default="owner", choices=["owner", "collaborator", "organization_member", "all"])
    Me.add_argument("--visibility", default="all", choices=["all", "public", "private"])
    Me.add_argument("--limit-repos", type=int, default=200)
    Me.add_argument("--max-files", type=int, default=350)
    Me.add_argument("--max-bytes", type=int, default=200000)

    return P

def Main() -> None:
    Parser = BuildParser()
    Args = Parser.parse_args()
    Token = LoadToken(Args.token)
    Client = GitHubClient(GitHubConfig(Token=Token), Timeout=Args.timeout)

    try:
        if Args.cmd == "me":
            Out: Dict[str, Any] = {"ok": True}
            Viewer = Client.GetViewer()

            if Args.account or (not Args.secretscanner):
                Out["account"] = {
                    "login": Viewer.get("login"),
                    "id": Viewer.get("id"),
                    "html_url": Viewer.get("html_url"),
                    "name": Viewer.get("name"),
                    "email": Viewer.get("email")
                }

            if Args.secretscanner:
                if not Args.yes:
                    Gate = ReadLine("Type SCAN to continue: ")
                    if Gate != "SCAN":
                        raise SystemExit("Canceled")
                Result = ScanAccount(
                    Client,
                    Affiliation=Args.affiliation,
                    Visibility=Args.visibility,
                    LimitRepos=Args.limit_repos,
                    MaxFiles=Args.max_files,
                    MaxBytes=Args.max_bytes
                )
                Out["secretscanner"] = Result
                Out["secrets_found"] = len(Result.get("findings", []))

            PrintJson(Out)
            return

        raise SystemExit("Unknown command")
    except GitHubError as E:
        PrintJson({"error": True, "status": E.StatusCode, "message": str(E), "details": E.Details})
        sys.exit(2)

if __name__ == "__main__":
    Main()