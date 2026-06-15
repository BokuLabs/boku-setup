# ─── PowerShell Quick Setup for BokuLabs ───
# Run: irm https://raw.githubusercontent.com/BokuLabs/infra/master/powershell-setup.ps1 | iex

Write-Host ""
Write-Host "  ╔╗ ┌─┐┌─┐┬ ┬  PowerShell Setup" -ForegroundColor Cyan
Write-Host "  ╠╩╗│ ││ ┬│││  ─────────────────" -ForegroundColor Cyan
Write-Host "  ╚═╝└─┘└─┘└┴┘" -ForegroundColor Cyan
Write-Host ""

# Check Python
$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) {
    Write-Host "[!] Python not found. Install from https://python.org" -ForegroundColor Red
    Write-Host "    Or: winget install Python.Python.3.12" -ForegroundColor Yellow
    exit 1
}

# Check Git
$git = Get-Command git -ErrorAction SilentlyContinue
if (-not $git) {
    Write-Host "[!] Git not found. Install from https://git-scm.com" -ForegroundColor Red
    Write-Host "    Or: winget install Git.Git" -ForegroundColor Yellow
    exit 1
}

# Get token
$configDir = "$env:APPDATA\BokuLabs"
$configFile = "$configDir\config.json"
$token = $null

if (Test-Path $configFile) {
    $config = Get-Content $configFile | ConvertFrom-Json
    $token = $config.token
}

if (-not $token) {
    Write-Host "No GitHub token found." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Create a PAT at: https://github.com/settings/tokens"
    Write-Host "Required scope: repo"
    Write-Host ""
    $token = Read-Host "Enter your PAT"
    
    if ([string]::IsNullOrEmpty($token)) {
        Write-Host "[!] No token. Exiting." -ForegroundColor Red
        exit 1
    }
    
    # Save config
    New-Item -ItemType Directory -Force -Path $configDir | Out-Null
    @{token=$token; user="BokuLabs"} | ConvertTo-Json | Set-Content $configFile
    
    # Configure git credentials
    git config --global credential.helper store
    "https://BokuLabs:${token}@github.com" | Out-File -Append "$env:USERPROFILE\.git-credentials" -Encoding utf8
    
    Write-Host "[+] Token saved" -ForegroundColor Green
}

# Clone repos
$repos = @("DorkParse", "Tempmail-CloudFlare", "bokuwatch", "cineflow-api", "infra")
$homeDir = $env:USERPROFILE

Write-Host ""
Write-Host "Available repos:" -ForegroundColor Cyan
for ($i = 0; $i -lt $repos.Count; $i++) {
    Write-Host "  [$($i+1)] $($repos[$i])"
}
Write-Host "  [$($repos.Count+1)] Clone ALL"
Write-Host "  [0] Exit"
Write-Host ""

$choice = Read-Host "Choice"

if ($choice -eq "0") { exit }

$toClone = @()
if ($choice -eq ($repos.Count + 1).ToString()) {
    $toClone = $repos
} elseif ([int]$choice -ge 1 -and [int]$choice -le $repos.Count) {
    $toClone = @($repos[[int]$choice - 1])
} else {
    Write-Host "[!] Invalid" -ForegroundColor Red
    exit 1
}

foreach ($repo in $toClone) {
    $target = "$homeDir\$repo"
    if (Test-Path $target) {
        Write-Host "[~] $repo exists, pulling..." -ForegroundColor Yellow
        git -C $target pull
    } else {
        Write-Host "[>] Cloning $repo..." -ForegroundColor Cyan
        git clone "https://BokuLabs:${token}@github.com/BokuLabs/$repo.git" $target
    }
    
    # Install deps
    $reqFile = "$target\requirements.txt"
    if (Test-Path $reqFile) {
        Write-Host "[>] Installing deps for $repo..." -ForegroundColor Cyan
        python -m pip install -r $reqFile -q
    }
}

Write-Host ""
Write-Host "Done!" -ForegroundColor Green
Write-Host ""
Write-Host "Quick commands:" -ForegroundColor Cyan
Write-Host '  cd ~\DorkParse; python main.py'
Write-Host '  cd ~\Tempmail-CloudFlare; python bot.py'
