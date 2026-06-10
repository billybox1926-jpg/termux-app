# PowerShell script to generate TERMUX_APP_ISSUE_LEDGER.md and TERMUX_APP_FIRST_BATCH_PLAN.md
$issueFile = Join-Path $PSScriptRoot 'issue-data\issues_utf8.jsonl'
$ledgerPath = Join-Path $PSScriptRoot 'TERMUX_APP_ISSUE_LEDGER.md'
$batchPath = Join-Path $PSScriptRoot 'TERMUX_APP_FIRST_BATCH_PLAN.md'

# Initialize buckets
$buckets = @{ A = @(); B = @(); C = @(); D = @(); E = @(); F = @(); G = @() }

function Get-Bucket($issue) {
    $title = if ($issue.title) { $issue.title } else { '' }
    $title = $title.ToLower()
    $body = if ($issue.body) { $issue.body } else { '' }
    $body = $body.ToLower()
    $labels = ($issue.labels -join ',').ToLower()
    # Bucket A – high confidence bugs
    if ($title -match 'crash' -or $labels -match 'bug') {
        if ($body -match 'stack trace|exception|caused by|fatal error' -or $title -match 'crash') { return 'A' }
        return 'A'
    }
    # Bucket B – low risk fixes
    if ($title -match 'typo|null|leak|resource|doc|documentation') { return 'B' }
    if ($labels -match 'enhancement|documentation|question|lint') { return 'B' }
    # Bucket C – needs runtime stack
    if ($title -match 'session|install|bootstrap|runtime') { return 'C' }
    if ($labels -match 'runtime|session|install|bootstrap') { return 'C' }
    # Bucket D – belongs elsewhere
    if ($title -match 'package|api|x11|widget|boot') { return 'D' }
    if ($labels -match 'termux-packages|termux-api|widget|boot|x11') { return 'D' }
    # Bucket E – mirror/network/env
    if ($title -match 'mirror|network|repo|hash') { return 'E' }
    if ($labels -match 'mirror|network|repo') { return 'E' }
    # Bucket F – Android/device specific
    if ($title -match 'android|oem|permission|device') { return 'F' }
    if ($labels -match 'android|oem|permission|device') { return 'F' }
    return 'G'
}

Get-Content $issueFile -Encoding utf8 | ForEach-Object {
    $issue = $_ | ConvertFrom-Json -ErrorAction SilentlyContinue
    if (-not $issue) { return }
    $bucket = Get-Bucket $issue
    $buckets[$bucket] += "#${($issue.number)}: $($issue.title)"
}

# Write ledger
if (Test-Path $ledgerPath) { Remove-Item -Path $ledgerPath -Force }
$ledgerContent = "# TERMUX_APP_ISSUE_LEDGER`n"
foreach ($b in 'A','B','C','D','E','F','G') {
    $ledgerContent += "## Bucket $b`n"
    foreach ($line in $buckets[$b]) { $ledgerContent += "- $line`n" }
    $ledgerContent += "`n"
}
$ledgerTmp = "$ledgerPath.tmp"
$ledgerContent | Set-Content -Path $ledgerTmp -Encoding utf8 -Force
Move-Item -Path $ledgerTmp -Destination $ledgerPath -Force

# Prepare first batch plan (up to 10 from A and B)
if (Test-Path $batchPath) { Remove-Item -Path $batchPath -Force }
$selected = @()
foreach ($b in 'A','B') {
    foreach ($line in $buckets[$b]) {
        if ($selected.Count -ge 10) { break }
        $selected += "Bucket ${b}: $line"
    }
    if ($selected.Count -ge 10) { break }
}
"# TERMUX_APP_FIRST_BATCH_PLAN`n`n## Selected Issues (Buckets A & B)`n" | Set-Content -Path $batchPath -Encoding utf8
$selected | ForEach-Object { "- $_`n" | Add-Content -Path $batchPath -Encoding utf8 }
"`n### Rationale`nIssues chosen per lane priority: high‑confidence bugs first, then low‑risk clean‑ups, up to 10 items.`n" | Add-Content -Path $batchPath -Encoding utf8

Write-Host "Ledger and batch plan generated."
