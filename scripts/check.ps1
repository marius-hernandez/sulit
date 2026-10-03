<#
.SYNOPSIS
    Static checks for all projects: lint + type-check (fe), ruff (ai), compile (java).
.EXAMPLE
    .\scripts\check.ps1
    .\scripts\check.ps1 -Fix   # apply auto-fixes where supported
#>
[CmdletBinding()]
param(
    [switch]$Fix
)

. "$PSScriptRoot\_common.ps1"

$failed = @()

function Invoke-Check([string]$Label, [string]$Dir, [scriptblock]$Command) {
    Write-Step $Label
    try { Invoke-Native $Dir $Command }
    catch { $script:failed += $Label; Write-Host $_.Exception.Message -ForegroundColor Red }
}

if ($Fix) {
    Invoke-Check "sulit-ai: ruff fix"    $Services.ai.Dir { uv run ruff check . --fix; if ($LASTEXITCODE -eq 0) { uv run ruff format . } }
    Invoke-Check "sulit-fe: eslint fix"  $Services.fe.Dir { npx eslint . --fix }
}
else {
    Invoke-Check "sulit-ai: ruff"        $Services.ai.Dir { uv run ruff check . }
    Invoke-Check "sulit-fe: eslint"      $Services.fe.Dir { npm run lint }
}
Invoke-Check "sulit-fe: tsc"             $Services.fe.Dir { npx tsc --noEmit }
Invoke-Check "sulit-java: compile"       $Services.java.Dir { .\mvnw.cmd -q compile }

if ($failed.Count -gt 0) {
    Write-Host "`nFailed: $($failed -join ', ')" -ForegroundColor Red
    exit 1
}
Write-Host "`nAll checks passed." -ForegroundColor Green
