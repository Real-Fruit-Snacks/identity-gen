<#
.SYNOPSIS
  Sets up the identity-gen dev kit with no network.

.DESCRIPTION
  Makes a Python virtual environment in the kit folder (.venv), installs the wheels in offline\python into
  it without asking any package index, and points Playwright in that environment at the Chromium in
  offline\files\ms-playwright. Then it starts that Chromium once to prove it works, and prints the
  commands that run the checks.

  It needs Python (64-bit, the minor version in .python-version) and nothing else. If Python is missing
  or the wrong version, it says so and where to get the installer, and changes nothing.

  Run it from anywhere, in Windows PowerShell 5.1 or PowerShell 7:
    powershell -ExecutionPolicy Bypass -File offline\setup.ps1

  The source is tools\dev-kit\setup.ps1; tools\build-dev-kit.py copies it into the kit.

.PARAMETER Python
  Full path to python.exe, if the right version isn't the one on PATH or in the py launcher.
#>
param([string]$Python)

$ErrorActionPreference = 'Stop'
$Offline = $PSScriptRoot
$Kit = Split-Path -Parent $Offline
$Wheels = Join-Path $Offline 'python'
$Browsers = Join-Path $Offline 'files\ms-playwright'
$Venv = Join-Path $Kit '.venv'
$VenvPython = Join-Path $Venv 'Scripts\python.exe'

function Stop-Setup([string[]]$Lines) {
  Write-Host ''
  foreach ($l in $Lines) { Write-Host $l -ForegroundColor Red }
  exit 1
}

# What this kit was built for.
$Exact = (Get-Content (Join-Path $Kit '.python-version') -TotalCount 1).Trim()
$Minor = ($Exact -split '\.')[0..1] -join '.'
$Installer = "https://www.python.org/ftp/python/$Exact/python-$Exact-amd64.exe"

Write-Host "identity-gen dev kit: $Kit"
Write-Host "PowerShell $($PSVersionTable.PSVersion) ($($PSVersionTable.PSEdition))"

if (-not [Environment]::Is64BitOperatingSystem) {
  Stop-Setup @('This kit is for 64-bit Windows (its wheels and Chromium are win_amd64 builds).')
}
foreach ($d in @($Wheels, $Browsers)) {
  if (-not (Test-Path $d)) { Stop-Setup @("Missing $d. Unzip the whole kit and run this from inside it.") }
}

# --- Python ------------------------------------------------------------------------------------------
# Asks a candidate for "<major.minor.micro> <bits>". Native commands that write to stderr (the Microsoft
# Store stub does) must not stop the script, so errors are relaxed while asking.
function Get-PythonInfo([string]$Exe, [string[]]$Pre) {
  $ErrorActionPreference = 'Continue'
  try {
    $out = & $Exe @Pre -c "import sys, struct; print('%d.%d.%d %d %s' % (sys.version_info[:3] + (struct.calcsize('P') * 8, sys.executable)))" 2>$null
    if ($LASTEXITCODE -eq 0 -and $out) {
      $parts = ("$out".Trim()) -split ' ', 3
      return [pscustomobject]@{ Version = $parts[0]; Bits = $parts[1]; Path = $parts[2] }
    }
  } catch { }
  return $null
}

# Tried in order: -Python, python and python3 on PATH, then the py launcher asked for $Minor.
$candidates = @()
if ($Python) {
  if (-not (Test-Path $Python)) { Stop-Setup @("No python.exe at $Python.") }
  $candidates += [pscustomobject]@{ Exe = $Python; Pre = @() }
} else {
  foreach ($name in @('python', 'python3')) {
    $cmd = Get-Command $name -CommandType Application -ErrorAction SilentlyContinue | Select-Object -First 1
    if ($cmd) { $candidates += [pscustomobject]@{ Exe = $cmd.Source; Pre = @() } }
  }
  $py = Get-Command py -CommandType Application -ErrorAction SilentlyContinue | Select-Object -First 1
  if ($py) {
    $candidates += [pscustomobject]@{ Exe = $py.Source; Pre = @("-$Minor") }
    $candidates += [pscustomobject]@{ Exe = $py.Source; Pre = @() }   # only to say what it found instead
  }
}

$found = $null
$seen = @()
foreach ($c in $candidates) {
  $info = Get-PythonInfo $c.Exe $c.Pre
  if (-not $info) { continue }
  if ($info.Version -like "$Minor.*" -and $info.Bits -eq '64') { $found = $info; break }
  $seen += "  found Python $($info.Version) ($($info.Bits)-bit) at $($info.Path)"
}

if (-not $found) {
  $lines = @("Missing: Python $Minor (64-bit). This kit's wheels are built for CPython $Minor on Windows x64.")
  if ($seen) { $lines += 'Not usable here:'; $lines += $seen }
  $lines += "Install Python $Exact, the version CI uses, from the full installer (works offline once downloaded):"
  $lines += "  $Installer"
  $lines += 'Then run this again, or pass the path: -Python C:\path\to\python.exe'
  Stop-Setup $lines
}
if ($found.Version -ne $Exact) {
  Write-Host "Python $($found.Version) at $($found.Path) (CI uses $Exact; any $Minor.x works)" -ForegroundColor Yellow
} else {
  Write-Host "Python $($found.Version) at $($found.Path)"
}

# --- Virtual environment -----------------------------------------------------------------------------
if (Test-Path $VenvPython) {
  $have = Get-PythonInfo $VenvPython @()
  if (-not $have -or $have.Version -notlike "$Minor.*") {
    Write-Host "Replacing $Venv (it isn't Python $Minor)"
    Remove-Item -Recurse -Force $Venv
  }
}
if (-not (Test-Path $VenvPython)) {
  Write-Host "Creating $Venv"
  & $found.Path -m venv $Venv
  if ($LASTEXITCODE -ne 0) { Stop-Setup @("Couldn't create the virtual environment at $Venv.") }
}

# pip in this environment only ever looks in the kit, even for a later "pip install".
$pipIni = "[global]`r`nno-index = true`r`nfind-links = $Wheels`r`ndisable-pip-version-check = true`r`n"
[System.IO.File]::WriteAllText((Join-Path $Venv 'pip.ini'), $pipIni)

$reqs = @('-r', (Join-Path $Kit 'tests\requirements.txt'), '-r', (Join-Path $Kit 'docs\art\requirements.txt'))
Write-Host 'Installing the wheels from offline\python'
& $VenvPython -m pip install --no-index --find-links $Wheels --disable-pip-version-check --quiet @reqs
if ($LASTEXITCODE -ne 0) { Stop-Setup @('pip could not install from offline\python; see the error above.') }

# Playwright in this environment uses the kit's browsers, whatever PLAYWRIGHT_BROWSERS_PATH says outside.
# A .pth line runs when this environment's Python starts; the path is relative, so the kit can move.
$site = (& $VenvPython -c "import sysconfig; print(sysconfig.get_paths()['purelib'])").Trim()
$pth = 'import os, sys; os.environ["PLAYWRIGHT_BROWSERS_PATH"] = os.path.join(os.path.dirname(sys.prefix), "offline", "files", "ms-playwright")'
[System.IO.File]::WriteAllText((Join-Path $site 'identity-gen-offline.pth'), $pth + "`r`n")

# --- Prove the browser starts ------------------------------------------------------------------------
$probe = @'
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch()
    print(b.version)
    b.close()
'@
Write-Host 'Starting the bundled Chromium'
$ErrorActionPreference = 'Continue'
$chromium = & $VenvPython -c $probe
$ok = $LASTEXITCODE -eq 0
$ErrorActionPreference = 'Stop'
if (-not $ok) { Stop-Setup @("Playwright couldn't start the Chromium in $Browsers; see the error above.") }
Write-Host "Chromium $chromium"

Write-Host ''
Write-Host 'Ready. Nothing was downloaded. From the kit folder:' -ForegroundColor Green
Write-Host ''
Write-Host "  cd `"$Kit`""
Write-Host '  .venv\Scripts\python.exe tests\test_page.py'
Write-Host '  .venv\Scripts\python.exe tools\build-standalone.py'
Write-Host '  .venv\Scripts\python.exe tests\test_download.py --browsers chromium'
Write-Host '  Get-FileHash docs\assets\deck-*.svg'
Write-Host '  .venv\Scripts\python.exe docs\art\make-deck.py'
Write-Host '  Get-FileHash docs\assets\deck-*.svg'
Write-Host ''
Write-Host 'The first runs the page checks; the next two build the release index.html into dist\ and open it'
Write-Host 'from disk with the network blocked. make-deck.py redraws the README deck: the hashes before and'
Write-Host "after match unless a change altered what the deck's six seeds produce."
