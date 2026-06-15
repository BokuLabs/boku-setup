# BokuLabs Setup

One-command setup for all BokuLabs private repos.

## Quick Start

### Termux (Android)
```bash
pkg install python git
git clone https://BokuLabs:<YOUR_PAT>@github.com/BokuLabs/boku-setup.git ~/boku-setup
cd ~/boku-setup && python3 setup.py
```

### PowerShell (Windows)
```powershell
winget install Python.Python.3.12 Git.Git
git clone https://BokuLabs:<YOUR_PAT>@github.com/BokuLabs/boku-setup.git ~\boku-setup
cd ~\boku-setup; python setup.py
```

### Linux / macOS
```bash
git clone https://BokuLabs:<YOUR_PAT>@github.com/BokuLabs/boku-setup.git ~/boku-setup
cd ~/boku-setup && python3 setup.py
```

## Getting a PAT (Personal Access Token)

1. Go to: https://github.com/settings/tokens
2. Click **Generate new token (classic)**
3. Check **repo** scope (full control of private repos)
4. Copy the token

```bash
# Save token for future use
python3 setup.py --token ghp_XXXXXXXXXXXX

# Or set as env variable
export BOKU_TOKEN=ghp_XXXXXXXXXXXX
```

## Usage

```bash
# Interactive menu
python3 setup.py

# Clone specific repo
python3 setup.py DorkParse

# Clone all repos
python3 setup.py --all
```

## Available Repos

| Repo | Description | Visibility |
|------|-------------|------------|
| DorkParse | Google Dork Parser (Scrapfly) | 🔒 Private |
| Tempmail-CloudFlare | Temp Mail Bot | 🔒 Private |
| bokuwatch | Streaming App | 🔒 Private |
| cineflow-api | HLS Proxy API | 🔒 Private |
| infra | Infrastructure configs | 🔒 Private |
| stripe-checker-edu | Payment Auth Checker | 🌐 Public |

## After Cloning

```bash
# DorkParse
cd ~/DorkParse && python3 main.py 'filetype:env "DB_PASSWORD"'

# TempMail Bot
cd ~/Tempmail-CloudFlare && python3 bot.py

# BokuWatch
cd ~/bokuwatch && python3 app.py
```
