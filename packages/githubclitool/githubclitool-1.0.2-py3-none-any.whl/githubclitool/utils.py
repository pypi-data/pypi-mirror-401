import json
import os
import sys
from typing import Any, Optional

def LoadToken(ArgToken: Optional[str]) -> str:
    if ArgToken:
        return ArgToken.strip()
    Env = os.getenv("GITHUB_TOKEN") or os.getenv("GH_TOKEN")
    if Env:
        return Env.strip()
    raise SystemExit("Missing token. Use --token or set GITHUB_TOKEN/GH_TOKEN")

def PrintJson(Obj: Any) -> None:
    sys.stdout.write(json.dumps(Obj, ensure_ascii=False, indent=2) + "\n")

def ReadLine(Prompt: str) -> str:
    sys.stdout.write(Prompt)
    sys.stdout.flush()
    return sys.stdin.readline().strip()
