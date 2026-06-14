param(
    [int]$Port = 8000
)

$ErrorActionPreference = "Stop"

$RepoRoot = Split-Path -Parent $PSScriptRoot
Set-Location $RepoRoot

$Candidates = @()

if ($env:ALPHAGUARD_PYTHON) {
    $Candidates += $env:ALPHAGUARD_PYTHON
}

$Candidates += Join-Path $RepoRoot ".venv\Scripts\python.exe"
$Candidates += Join-Path $env:USERPROFILE ".cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"
$Candidates += "python"

$Python = $null
foreach ($Candidate in $Candidates) {
    if ((Test-Path $Candidate) -or (Get-Command $Candidate -ErrorAction SilentlyContinue)) {
        $Python = $Candidate
        break
    }
}

if (-not $Python) {
    Write-Error "Python was not found. Create .venv or set ALPHAGUARD_PYTHON to a python.exe path."
}

$env:PYTHONPATH = $RepoRoot

Write-Host "Starting AlphaGuard AI at http://127.0.0.1:$Port"
Write-Host "Dashboard: http://127.0.0.1:$Port/"
Write-Host "API docs:  http://127.0.0.1:$Port/docs"

& $Python -m uvicorn app.main:app --host 127.0.0.1 --port $Port --reload
