<#
.SYNOPSIS
    Starts the Sulit servers, each in its own terminal window.
.EXAMPLE
    .\scripts\dev.ps1                 # ai + java + fe
    .\scripts\dev.ps1 -Only java,fe   # subset
#>
[CmdletBinding()]
param(
    [ValidateSet("ai", "java", "fe")]
    [string[]]$Only = @("ai", "java", "fe")
)

. "$PSScriptRoot\_common.ps1"

$commands = @{
    ai   = "uv run uvicorn app.main:app --reload --port 8000"
    java = ".\mvnw.cmd spring-boot:run"
    fe   = "npm run dev"
}

$requiredEnvFile = @{
    ai   = ".env"
    java = ".env"
    fe   = $null
}

$shell = Get-ShellExe

# Ordered so dependencies come up first: ai -> java -> fe.
foreach ($key in $Services.Keys) {
    if ($Only -notcontains $key) { continue }

    $svc = $Services[$key]
    $envFile = $requiredEnvFile[$key]
    if ($envFile -and -not (Test-Path (Join-Path $svc.Dir $envFile))) {
        Write-Warning "$($svc.Name): $envFile not found. Run .\scripts\setup.ps1 or copy .env.example."
    }

    $title = "$($svc.Name) :$($svc.Port)"
    $startup = "`$Host.UI.RawUI.WindowTitle = '$title'; $($commands[$key])"

    Write-Step "Starting $title"
    Start-Process -FilePath $shell -WorkingDirectory $svc.Dir -ArgumentList @("-NoExit", "-NoProfile", "-Command", $startup)
}

Write-Host ""
Write-Host "Frontend: http://localhost:3000"
Write-Host "Backend:  http://localhost:8080"
Write-Host "AI docs:  http://localhost:8000/docs"
Write-Host "Check status with .\scripts\health.ps1; stop everything with .\scripts\stop.ps1"
