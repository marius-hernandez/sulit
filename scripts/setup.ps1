<#
.SYNOPSIS
    One-time setup: checks tools, creates env files from examples, installs dependencies.
.EXAMPLE
    .\scripts\setup.ps1
    .\scripts\setup.ps1 -SkipInstall   # only create env files
#>
[CmdletBinding()]
param(
    [switch]$SkipInstall
)

. "$PSScriptRoot\_common.ps1"

Write-Step "Checking required tools"
Assert-Command "uv"   "Install: https://docs.astral.sh/uv/getting-started/installation/"
Assert-Command "npm"  "Install Node.js LTS: https://nodejs.org/"
Assert-Command "java" "Install a JDK matching <java.version> in sulit-java/pom.xml."

# Next.js reads .env.local; the other two read .env.
$envTargets = @(
    @{ Dir = $Services.ai.Dir;   Target = ".env" },
    @{ Dir = $Services.java.Dir; Target = ".env" },
    @{ Dir = $Services.fe.Dir;   Target = ".env.local" }
)

Write-Step "Creating env files (existing files are left untouched)"
foreach ($entry in $envTargets) {
    $example = Join-Path $entry.Dir ".env.example"
    $target = Join-Path $entry.Dir $entry.Target
    if (Test-Path $target) {
        Write-Host "  exists:  $target"
    }
    elseif (Test-Path $example) {
        Copy-Item $example $target
        Write-Host "  created: $target  <- fill in values" -ForegroundColor Yellow
    }
}

if ($SkipInstall) { return }

Write-Step "Installing sulit-ai dependencies (uv sync)"
Invoke-Native $Services.ai.Dir { uv sync }

Write-Step "Installing sulit-fe dependencies (npm install)"
Invoke-Native $Services.fe.Dir { npm install }

Write-Step "Resolving sulit-java dependencies (maven)"
Invoke-Native $Services.java.Dir { .\mvnw.cmd -q dependency:go-offline }

Write-Step "Done. Fill in the .env files, then run .\scripts\dev.ps1"
