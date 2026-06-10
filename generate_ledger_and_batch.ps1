# Generate TERMUX_APP_ISSUE_LEDGER.md and TERMUX_APP_FIRST_BATCH_PLAN.md
$ErrorActionPreference = "Stop"

$issueFile = Join-Path $PSScriptRoot "issue-data\issues_utf8.jsonl"
$ledgerPath = Join-Path $PSScriptRoot "TERMUX_APP_ISSUE_LEDGER.md"
$batchPath = Join-Path $PSScriptRoot "TERMUX_APP_FIRST_BATCH_PLAN.md"

if (!(Test-Path $issueFile)) {
    throw "Missing issue file: $issueFile"
}

function To-LowerText($value) {
    if ($null -eq $value) { return "" }
    if ($value -is [array]) { return (($value -join ",").ToString()).ToLowerInvariant() }
    return ($value.ToString()).ToLowerInvariant()
}

$buckets = [ordered]@{
    A = New-Object System.Collections.Generic.List[string]
    B = New-Object System.Collections.Generic.List[string]
    C = New-Object System.Collections.Generic.List[string]
    D = New-Object System.Collections.Generic.List[string]
    E = New-Object System.Collections.Generic.List[string]
    F = New-Object System.Collections.Generic.List[string]
    G = New-Object System.Collections.Generic.List[string]
}

function Get-Bucket($issue) {
    $title = To-LowerText $issue.title
    $body = To-LowerText $issue.body
    $labels = To-LowerText $issue.labels

    # E: mirror/network/user environment first, because these are usually not app-code bugs.
    if ($title -match "mirror|network|repo|repository|hash sum|pkg update|pkg upgrade|apt|tur-packages" -or
        $body -match "hash sum mismatch|failed to fetch|mirror|tur-packages") {
        return "E"
    }

    # D: belongs in another Termux repo/package.
    if ($title -match "x11|widget|boot|termux-api|termux packages|package request|package update" -or
        $labels -match "termux-packages|termux-api|x11|widget|boot") {
        return "D"
    }

    # C: needs runtime stack / APK behavior.
    if ($title -match "session|bootstrap|install|terminal|keyboard|input|keycode|pageup|pagedown|launcher|shell|runtime" -or
        $body -match "steps to reproduce|device model|android os version") {
        return "C"
    }

    # F: Android/OEM/permission-specific.
    if ($title -match "android 1[0-9]|android|oem|permission|scoped storage|notification permission|device" -or
        $labels -match "android|permission|device|oem") {
        return "F"
    }

    # A: app-code bug with crash/exception signal.
    if ($title -match "crash|exception|fatal|anr" -or
        $body -match "stack trace|caused by|androidruntime|fatal exception|remoteexception|securityexception|nullpointerexception") {
        return "A"
    }

    # B: low-risk static/code-health/docs.
    if ($title -match "typo|null|leak|resource leak|documentation|docs|readme|deprecated|lint" -or
        $body -match "static code analysis|resource leak|typo|documentation") {
        return "B"
    }

    return "G"
}

$issues = New-Object System.Collections.Generic.List[object]

Get-Content $issueFile -Encoding utf8 | ForEach-Object {
    if ([string]::IsNullOrWhiteSpace($_)) { return }

    try {
        $issue = $_ | ConvertFrom-Json -ErrorAction Stop
    } catch {
        Write-Warning "Skipping invalid JSONL line"
        return
    }

    if ($null -eq $issue.number) { return }

    $bucket = Get-Bucket $issue
    $line = "#{0}: {1}" -f $issue.number, $issue.title
    $buckets[$bucket].Add($line)

    $issues.Add([pscustomobject]@{
        Number = $issue.number
        Title = $issue.title
        Bucket = $bucket
        UpdatedAt = $issue.updated_at
        Comments = $issue.comments
    })
}

$total = $issues.Count

$ledger = New-Object System.Collections.Generic.List[string]
$ledger.Add("# TERMUX_APP_ISSUE_LEDGER")
$ledger.Add("")
$ledger.Add("Pulled upstream open issues: $total")
$ledger.Add("")
$ledger.Add("## Bucket Counts")
$ledger.Add("")
foreach ($b in $buckets.Keys) {
    $ledger.Add("- Bucket ${b}: $($buckets[$b].Count)")
}
$ledger.Add("")

foreach ($b in $buckets.Keys) {
    $ledger.Add("## Bucket ${b}")
    $ledger.Add("")
    if ($buckets[$b].Count -eq 0) {
        $ledger.Add("- None")
    } else {
        foreach ($entry in $buckets[$b]) {
            $ledger.Add("- $entry")
        }
    }
    $ledger.Add("")
}

$utf8NoBom = New-Object System.Text.UTF8Encoding($false)
[System.IO.File]::WriteAllLines($ledgerPath, $ledger, $utf8NoBom)

$selected = New-Object System.Collections.Generic.List[string]

foreach ($b in @("A", "B")) {
    foreach ($line in $buckets[$b]) {
        if ($selected.Count -ge 10) { break }
        $selected.Add("Bucket ${b}: $line")
    }
    if ($selected.Count -ge 10) { break }
}

$batch = New-Object System.Collections.Generic.List[string]
$batch.Add("# TERMUX_APP_FIRST_BATCH_PLAN")
$batch.Add("")
$batch.Add("## Selected Issues")
$batch.Add("")
if ($selected.Count -eq 0) {
    $batch.Add("- None selected from buckets A/B")
} else {
    foreach ($entry in $selected) {
        $batch.Add("- $entry")
    }
}
$batch.Add("")
$batch.Add("## Rationale")
$batch.Add("")
$batch.Add("First batch is limited to buckets A and B only: high-confidence app-code crashes and low-risk static/code-health fixes.")
$batch.Add("")
$batch.Add("Do not batch-fix these automatically. Pick one issue, inspect source, make the smallest patch, and use GitHub Actions as the gate.")

[System.IO.File]::WriteAllLines($batchPath, $batch, $utf8NoBom)

Write-Host "Ledger and batch plan generated."
Write-Host "Total issues: $total"
foreach ($b in $buckets.Keys) {
    Write-Host "Bucket ${b}: $($buckets[$b].Count)"
}
