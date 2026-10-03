# Shared helpers, dot-sourced by the other scripts. Compatible with Windows PowerShell 5.1 and pwsh 7.
$ErrorActionPreference = "Stop"

$RepoRoot = Split-Path -Parent $PSScriptRoot

$Services = [ordered]@{
    ai   = @{ Name = "sulit-ai";   Dir = (Join-Path $RepoRoot "sulit-ai");   Port = 8000; HealthUrl = "http://localhost:8000/health" }
    java = @{ Name = "sulit-java"; Dir = (Join-Path $RepoRoot "sulit-java"); Port = 8080; HealthUrl = "http://localhost:8080/actuator/health" }
    fe   = @{ Name = "sulit-fe";   Dir = (Join-Path $RepoRoot "sulit-fe");   Port = 3000; HealthUrl = "http://localhost:3000" }
}

function Write-Step([string]$Message) {
    Write-Host "==> $Message" -ForegroundColor Cyan
}

function Test-Command([string]$Name) {
    return [bool](Get-Command $Name -ErrorAction SilentlyContinue)
}

function Assert-Command([string]$Name, [string]$InstallHint) {
    if (-not (Test-Command $Name)) {
        throw "'$Name' was not found on PATH. $InstallHint"
    }
}

# Runs a native command in a directory and throws if it exits non-zero.
function Invoke-Native([string]$WorkingDir, [scriptblock]$Command) {
    Push-Location $WorkingDir
    try {
        & $Command
        if ($LASTEXITCODE -ne 0) {
            throw "Command failed with exit code $LASTEXITCODE in $WorkingDir"
        }
    }
    finally {
        Pop-Location
    }
}

function Get-ShellExe {
    if (Test-Command "pwsh") { return "pwsh" }
    return "powershell"
}
