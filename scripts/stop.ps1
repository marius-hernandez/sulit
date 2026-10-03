<#
.SYNOPSIS
    Stops whatever is listening on the Sulit ports (8000, 8080, 3000), including child processes.
    Asks for confirmation per process; pass -Confirm:$false to skip.
.EXAMPLE
    .\scripts\stop.ps1
    .\scripts\stop.ps1 -Only java -Confirm:$false
#>
[CmdletBinding(SupportsShouldProcess, ConfirmImpact = "High")]
param(
    [ValidateSet("ai", "java", "fe")]
    [string[]]$Only = @("ai", "java", "fe")
)

. "$PSScriptRoot\_common.ps1"

foreach ($key in $Services.Keys) {
    if ($Only -notcontains $key) { continue }
    $svc = $Services[$key]

    $pids = Get-NetTCPConnection -LocalPort $svc.Port -State Listen -ErrorAction SilentlyContinue |
        Select-Object -ExpandProperty OwningProcess -Unique

    if (-not $pids) {
        Write-Host "$($svc.Name): nothing listening on :$($svc.Port)"
        continue
    }

    foreach ($procId in $pids) {
        $proc = Get-Process -Id $procId -ErrorAction SilentlyContinue
        if (-not $proc) { continue }
        if ($PSCmdlet.ShouldProcess("$($proc.ProcessName) (PID $procId) on :$($svc.Port)", "Stop process tree")) {
            # taskkill /T also stops children (e.g. uvicorn reloader workers, next-server).
            taskkill /PID $procId /T /F | Out-Null
            Write-Host "$($svc.Name): stopped $($proc.ProcessName) (PID $procId)" -ForegroundColor Green
        }
    }
}
