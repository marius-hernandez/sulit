<#
.SYNOPSIS
    Checks that each Sulit server is up.
.EXAMPLE
    .\scripts\health.ps1
#>
[CmdletBinding()]
param()

. "$PSScriptRoot\_common.ps1"

$allUp = $true
foreach ($key in $Services.Keys) {
    $svc = $Services[$key]
    try {
        $response = Invoke-WebRequest -Uri $svc.HealthUrl -UseBasicParsing -TimeoutSec 5
        Write-Host ("{0,-11} UP    {1} ({2})" -f $svc.Name, $svc.HealthUrl, $response.StatusCode) -ForegroundColor Green
    }
    catch {
        $allUp = $false
        Write-Host ("{0,-11} DOWN  {1} ({2})" -f $svc.Name, $svc.HealthUrl, $_.Exception.Message) -ForegroundColor Red
    }
}

if (-not $allUp) { exit 1 }
