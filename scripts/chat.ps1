<#
.SYNOPSIS
    End-to-end smoke test: sends a message through the backend (and therefore the AI service and DB).
.EXAMPLE
    .\scripts\chat.ps1 "Plan a 1000 peso weekly grocery list"
    .\scripts\chat.ps1 "Make it vegetarian" -ConversationId <uuid>
    .\scripts\chat.ps1 -Direct "hello"    # bypass Spring Boot, call FastAPI directly
#>
[CmdletBinding()]
param(
    [Parameter(Mandatory, Position = 0)]
    [string]$Message,
    [string]$ConversationId,
    [switch]$Direct
)

. "$PSScriptRoot\_common.ps1"

if ($Direct) {
    $uri = "http://localhost:$($Services.ai.Port)/v1/chat"
    $body = @{ messages = @(@{ role = "user"; content = $Message }) }
    $headers = @{}
    $envFile = Join-Path $Services.ai.Dir ".env"
    if (Test-Path $envFile) {
        $keyLine = Select-String -Path $envFile -Pattern '^\s*INTERNAL_API_KEY\s*=\s*(.+)$' | Select-Object -First 1
        if ($keyLine) { $headers["X-Internal-Api-Key"] = $keyLine.Matches[0].Groups[1].Value.Trim() }
    }
}
else {
    $uri = "http://localhost:$($Services.java.Port)/api/chat"
    $body = @{ message = $Message }
    if ($ConversationId) { $body.conversationId = $ConversationId }
    $headers = @{}
}

Write-Step "POST $uri"
$response = Invoke-RestMethod -Method Post -Uri $uri -Headers $headers -ContentType "application/json" `
    -Body ($body | ConvertTo-Json -Depth 5) -TimeoutSec 120
$response | ConvertTo-Json -Depth 5
