# BokuLabs Setup

Complete setup guide for all BokuLabs private repos.

---

## Step 1 — Get Your GitHub PAT (Personal Access Token)

Do this **once** on any device with a browser.

1. Open: https://github.com/settings/tokens
2. Click **"Generate new token (classic)"**
3. Name: `bokulabs-setup` (or anything)
4. Expiration: **No expiration** (or 1 year)
5. Check scope: ✅ **repo** (full control of private repos)
6. Click **Generate token**
7. **Copy the token** (`ghp_xxxxxxxxxxxxx`)

> Save this token somewhere safe. You'll need it on every device.

---

## Step 2 — Install Git & Python

### Termux (Android)
```bash
pkg update && pkg upgrade -y
pkg install git python -y
pip install --upgrade pip
```

### PowerShell (Windows)
```powershell
# Install Git
winget install Git.Git

# Install Python
winget install Python.Python.3.12

# Restart PowerShell after install
```

### Linux (Ubuntu/Debian)
```bash
sudo apt update && sudo apt install git python3 python3-pip -y
```

### macOS
```bash
# Git comes pre-installed. If not:
xcode-select --install

# Python:
brew install python3
```

---

## Step 3 — Configure Git Credentials (one-time)

This saves your token so you never have to type it again.

```bash
git config --global credential.helper store
```

---

## Step 4 — Clone boku-setup

```bash
git clone https://github.com/BokuLabs/boku-setup.git ~/boku-setup
```

When prompted:
```
Username for 'https://github.com': BokuLabs
Password for 'https://BokuLabs@github.com': ghp_YOUR_TOKEN_HERE
```

> After this, credentials are saved. All future `git clone` / `git pull` for BokuLabs repos work without prompting.

---

## Step 5 — Run Setup

```bash
cd ~/boku-setup
python3 setup.py
```

This shows a menu:
```
  [1] 🔒 DorkParse - Google Dork Parser (Scrapfly Edition)
  [2] 🔒 Tempmail-CloudFlare - Temp Mail Bot
  [3] 🔒 bokuwatch - BokuWatch Streaming App
  [4] 🔒 cineflow-api - CineFlow HLS Proxy API
  [5] 🔒 infra - Infrastructure configs & scripts
  [6] 🌐 stripe-checker-edu - Stripe Payment Auth Checker
  [7] Clone ALL
  [0] Exit
```

Pick a number → it clones + installs deps automatically.

### Or clone specific repo directly:
```bash
python3 setup.py DorkParse
python3 setup.py bokuwatch
python3 setup.py --all
```

### Or save token first (no prompt):
```bash
python3 setup.py --token ghp_YOUR_TOKEN_HERE
python3 setup.py
```

---

## Step 6 — Run the Repos

After cloning:

```bash
# DorkParse (Google Dork Scanner)
cd ~/DorkParse
python3 main.py 'filetype:env "DB_PASSWORD"'
python3 main.py    # Interactive menu

# BokuKit (All-in-One Toolkit)
cd ~/bokukit
python3 bokukit.py    # Interactive menu

# TempMail Bot
cd ~/Tempmail-CloudFlare
python3 bot.py

# BokuWatch (Streaming App)
cd ~/bokuwatch
python3 app.py
# Open http://localhost:8080

# CineFlow API
cd ~/cineflow-api
python3 app.py
```

---

## Clone Any Private Repo (Manual)

After Step 3 (credential store), you can clone any BokuLabs repo:

```bash
git clone https://github.com/BokuLabs/REPO_NAME.git ~/REPO_NAME
```

If prompted for credentials:
- Username: `BokuLabs`
- Password: `ghp_YOUR_TOKEN`

Examples:
```bash
git clone https://github.com/BokuLabs/bokukit.git ~/bokukit
git clone https://github.com/BokuLabs/infra.git ~/infra
git clone https://github.com/BokuLabs/cineflow-api.git ~/cineflow-api
```

---

## Quick Reference

| What | Command |
|------|---------|
| Set credential store | `git config --global credential.helper store` |
| Clone any repo | `git clone https://github.com/BokuLabs/REPO.git ~/REPO` |
| Save token (setup.py) | `python3 setup.py --token ghp_XXX` |
| Clone all repos | `python3 setup.py --all` |
| Update a repo | `cd ~/REPO && git pull` |
| Check saved creds | `cat ~/.git-credentials` |

---

## Available Repos

| Repo | Description | Visibility |
|------|-------------|------------|
| boku-setup | This setup script | 🌐 Public |
| bokukit | All-in-One Security Toolkit | 🔒 Private |
| DorkParse | Google Dork Parser (Scrapfly) | 🔒 Private |
| Tempmail-CloudFlare | Temp Mail Bot (CF Routing) | 🔒 Private |
| bokuwatch | Streaming App (Flask + SPA) | 🔒 Private |
| cineflow-api | HLS Proxy API | 🔒 Private |
| infra | Infrastructure configs | 🔒 Private |
| stripe-checker-edu | Payment Auth Checker (Educational) | 🌐 Public |

---

## Troubleshooting

**"Authentication failed"**
→ Token expired or wrong. Generate new one at https://github.com/settings/tokens

**"Repository not found"**
→ Repo is private. Make sure you're using PAT (not password) and token has `repo` scope.

**git keeps asking for password**
→ Run: `git config --global credential.helper store`
→ Then clone once more, credentials will be saved.

**Termux: "python not found"**
→ Run: `pkg install python`

**Windows: "git not recognized"**
→ Restart PowerShell after installing Git. Or use Git Bash.

---

## Security

- **Never share your PAT** — it gives full access to your private repos
- **Never commit tokens** to repos
- **Revoke compromised tokens** at: https://github.com/settings/tokens
- Token stored in: `~/.git-credentials` (plaintext, chmod 600)

---

BokuLabs 2026
