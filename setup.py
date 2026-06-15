#!/usr/bin/env python3
"""
BokuLabs Repo Setup Script
Works on: Linux, macOS, Termux (Android), PowerShell (Windows)

Usage:
  python3 setup.py                    # Interactive - choose repo
  python3 setup.py DorkParse          # Clone specific repo
  python3 setup.py --all              # Clone all repos
  python3 setup.py --token <PAT>      # Save PAT first, then interactive
"""

import os
import sys
import subprocess
import json
import re
from pathlib import Path

GITHUB_USER = "BokuLabs"
GITHUB_API = "https://api.github.com"

REPOS = {
    "DorkParse": {
        "desc": "Google Dork Parser (Scrapfly Edition)",
        "deps": ["pip install colorama beautifulsoup4 lxml httpx scrapfly-sdk"],
        "run": "python3 main.py",
        "private": True,
    },
    "Tempmail-CloudFlare": {
        "desc": "Temp Mail Bot (Cloudflare Email Routing)",
        "deps": ["pip install aiogram httpx"],
        "run": "python3 bot.py",
        "private": True,
    },
    "bokuwatch": {
        "desc": "BokuWatch Streaming App",
        "deps": ["pip install flask"],
        "run": "python3 app.py",
        "private": True,
    },
    "cineflow-api": {
        "desc": "CineFlow HLS Proxy API",
        "deps": ["pip install flask requests"],
        "run": "python3 app.py",
        "private": True,
    },
    "infra": {
        "desc": "Infrastructure configs & scripts",
        "deps": [],
        "run": "# Configs only",
        "private": True,
    },
    "stripe-checker-edu": {
        "desc": "Stripe Payment Auth Checker (Educational)",
        "deps": ["pip install stripe"],
        "run": "python3 multi_checker.py",
        "private": False,
    },
}

# ─── Colors ───
try:
    from colorama import Fore, Style, init
    init()
    C_OK = Fore.GREEN
    C_ERR = Fore.RED
    C_INFO = Fore.CYAN
    C_WARN = Fore.YELLOW
    C_RESET = Style.RESET_ALL
    C_BOLD = Style.BRIGHT
except ImportError:
    C_OK = C_ERR = C_INFO = C_WARN = C_RESET = C_BOLD = ""


def is_termux():
    return "TERMUX_VERSION" in os.environ or "/com.termux" in os.environ.get("PREFIX", "")


def is_windows():
    return os.name == "nt"


def get_config_path():
    if is_termux():
        return Path.home() / ".boku-setup"
    elif is_windows():
        return Path(os.environ.get("APPDATA", "")) / "BokuLabs"
    else:
        return Path.home() / ".boku-setup"


def save_token(token):
    """Save PAT to config file."""
    config_dir = get_config_path()
    config_dir.mkdir(parents=True, exist_ok=True)
    config_file = config_dir / "config.json"

    config = {"token": token, "user": GITHUB_USER}
    with open(config_file, "w") as f:
        json.dump(config, f, indent=2)

    # Also configure git credential helper
    subprocess.run(["git", "config", "--global", "credential.helper", "store"], capture_output=True)

    # Write to git-credentials
    git_creds = Path.home() / ".git-credentials"
    cred_line = f"https://{GITHUB_USER}:{token}@github.com\n"

    existing = git_creds.read_text() if git_creds.exists() else ""
    if GITHUB_USER not in existing:
        with open(git_creds, "a") as f:
            f.write(cred_line)
    else:
        # Replace existing entry
        lines = existing.strip().split("\n")
        lines = [l for l in lines if GITHUB_USER not in l]
        lines.append(cred_line.strip())
        git_creds.write_text("\n".join(lines) + "\n")

    print(f"{C_OK}[+] Token saved to {config_file}{C_RESET}")
    print(f"{C_OK}[+] Git credentials configured{C_RESET}")


def load_token():
    """Load PAT from config."""
    config_dir = get_config_path()
    config_file = config_dir / "config.json"

    if config_file.exists():
        with open(config_file) as f:
            config = json.load(f)
        return config.get("token")

    # Fallback: check git-credentials
    git_creds = Path.home() / ".git-credentials"
    if git_creds.exists():
        content = git_creds.read_text()
        m = re.search(r':(ghp_[^@]+)@', content)
        if m:
            return m.group(1)

    return None


def list_repos(token):
    """List all repos from GitHub API."""
    try:
        import urllib.request
        req = urllib.request.Request(
            f"{GITHUB_API}/user/repos?per_page=100&sort=updated",
            headers={
                "Authorization": f"Bearer {token}",
                "Accept": "application/vnd.github+json",
                "User-Agent": "BokuLabs-Setup",
            }
        )
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read())
    except Exception as e:
        print(f"{C_ERR}[!] API error: {e}{C_RESET}")
        return []


def clone_repo(repo_name, token=None):
    """Clone a single repo."""
    url = f"https://{GITHUB_USER}:{token}@github.com/{GITHUB_USER}/{repo_name}.git"
    target = Path.home() / repo_name

    if target.exists():
        print(f"{C_WARN}[~] {repo_name} already exists at {target}{C_RESET}")
        # Try pulling instead
        subprocess.run(["git", "-C", str(target), "pull"], capture_output=True)
        return True

    print(f"{C_INFO}[>] Cloning {repo_name}...{C_RESET}")
    result = subprocess.run(
        ["git", "clone", url, str(target)],
        capture_output=True, text=True
    )

    if result.returncode == 0:
        print(f"{C_OK}[+] Cloned to {target}{C_RESET}")
        return True
    else:
        print(f"{C_ERR}[!] Clone failed: {result.stderr.strip()}{C_RESET}")
        return False


def setup_deps(repo_name):
    """Install dependencies for a repo."""
    info = REPOS.get(repo_name, {})
    deps = info.get("deps", [])

    if not deps:
        print(f"{C_INFO}[~] No dependencies for {repo_name}{C_RESET}")
        return

    target = Path.home() / repo_name
    req_file = target / "requirements.txt"

    if req_file.exists():
        print(f"{C_INFO}[>] Installing from requirements.txt...{C_RESET}")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", str(req_file), "-q"])
    else:
        for dep in deps:
            print(f"{C_INFO}[>] {dep}{C_RESET}")
            subprocess.run(dep.split(), capture_output=True)


def show_repo_info(repo_name):
    """Show repo info and run instructions."""
    info = REPOS.get(repo_name, {})
    if not info:
        return

    print(f"\n{C_BOLD}{'='*50}")
    print(f"  {repo_name}")
    print(f"  {info['desc']}")
    print(f"{'='*50}{C_RESET}")

    vis = "🔒 Private" if info.get("private") else "🌐 Public"
    print(f"  Visibility: {vis}")

    if info["deps"]:
        print(f"  Dependencies: {', '.join(d.split()[-1] for d in info['deps'])}")

    print(f"\n  {C_BOLD}Run:{C_RESET}")
    print(f"    cd ~/{repo_name}")
    print(f"    {info['run']}")

    if repo_name == "DorkParse":
        print(f"\n  {C_BOLD}Examples:{C_RESET}")
        print(f"    python3 main.py 'filetype:env \"DB_PASSWORD\"'")
        print(f"    python3 main.py 'intitle:\"index of\" \".env\"' --bing")
        print(f"    python3 main.py  # Interactive menu")


def main():
    print(f"""
{C_BOLD}{C_INFO}
  ╔╗ ┌─┐┌─┐┬ ┬  ╔═╗┌─┐┌─┐┌┬┐┌─┐┌─┐
  ╠╩╗│ ││ ┬│││  ╚═╗├┤ ├─┤ ││├┤ ├┤ 
  ╚═╝└─┘└─┘└┴┘  ╚═╝└─┘┴ ┴─┴┘└─┘└─┘
{C_RESET}
  Private repo setup for Termux, PowerShell, Linux
""")

    # Check for --token argument
    if "--token" in sys.argv:
        idx = sys.argv.index("--token")
        if idx + 1 < len(sys.argv):
            save_token(sys.argv[idx + 1])
            return

    # Load or ask for token
    token = load_token()
    if not token:
        print(f"{C_WARN}[!] No GitHub token found.{C_RESET}")
        print(f"\n  To create a PAT (Personal Access Token):")
        print(f"  1. Go to: https://github.com/settings/tokens")
        print(f"  2. Click 'Generate new token (classic)'")
        print(f"  3. Check 'repo' scope (full control of private repos)")
        print(f"  4. Copy the token")
        print(f"\n  Then run: python3 setup.py --token ghp_XXXXXXXXXX")
        print(f"  Or set env: export BOKU_TOKEN=ghp_XXXXXXXXXX")
        return

    # --all flag
    if "--all" in sys.argv:
        for name in REPOS:
            clone_repo(name, token)
        return

    # Specific repo from args
    for arg in sys.argv[1:]:
        if not arg.startswith("-") and arg in REPOS:
            clone_repo(arg, token)
            setup_deps(arg)
            show_repo_info(arg)
            return

    # Interactive menu
    print(f"{C_INFO}Available repos:{C_RESET}\n")
    repo_names = list(REPOS.keys())
    for i, name in enumerate(repo_names, 1):
        info = REPOS[name]
        vis = "🔒" if info.get("private") else "🌐"
        print(f"  {C_BOLD}[{i}]{C_RESET} {vis} {name} - {info['desc']}")

    print(f"  {C_BOLD}[{len(repo_names)+1}]{C_RESET} Clone ALL")
    print(f"  {C_BOLD}[0]{C_RESET} Exit")

    choice = input(f"\n{C_INFO}Choice: {C_RESET}").strip()

    try:
        idx = int(choice) - 1
        if idx == len(repo_names):
            for name in REPOS:
                clone_repo(name, token)
                setup_deps(name)
        elif 0 <= idx < len(repo_names):
            name = repo_names[idx]
            clone_repo(name, token)
            setup_deps(name)
            show_repo_info(name)
    except (ValueError, IndexError):
        print(f"{C_ERR}[!] Invalid choice{C_RESET}")


if __name__ == "__main__":
    main()
