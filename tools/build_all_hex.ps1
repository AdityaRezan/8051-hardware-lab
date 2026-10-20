<#
Builds every AT89S52 uVision project in firmware\keil, reports the code size of
each against the 2048 byte evaluation limit, and copies the finished HEX files
into firmware\hex ready to take to the lab.

Usage, from a PowerShell prompt in this folder:

    .\build_all_hex.ps1                        build all 13 programs
    .\build_all_hex.ps1 -Programs 01,12        build only those two
    .\build_all_hex.ps1 -Small                 rebuild optimised for size
    .\build_all_hex.ps1 -LX51                  also try REMOVEUNUSED
    .\build_all_hex.ps1 -KeilPath C:\Keil_v5\UV4

Double click Build-All-HEX.bat if you would rather not open PowerShell.
#>

[CmdletBinding()]
param(
    [string]$KeilPath = "",
    [string[]]$Programs = @(),
    [switch]$Small,
    [switch]$LX51,
    [switch]$Undo
)

$ErrorActionPreference = "Stop"

$root    = Split-Path -Parent $PSScriptRoot
$keilDir = Join-Path $root "firmware\keil"
$hexDir  = Join-Path $root "firmware\hex"
$logDir  = Join-Path $keilDir "Logs"
$limit   = 2048

function Write-Head($text) {
    Write-Host ""
    Write-Host "  $text" -ForegroundColor Cyan
    Write-Host ("  " + ("-" * ($text.Length))) -ForegroundColor DarkGray
}

function Find-UV4([string]$hint) {
    $candidates = New-Object System.Collections.ArrayList

    if ($hint -ne "") {
        [void]$candidates.Add((Join-Path $hint "UV4.exe"))
        [void]$candidates.Add($hint)
    }
    if ($env:UV4_PATH) { [void]$candidates.Add($env:UV4_PATH) }

    [void]$candidates.Add("C:\Keil_v5\UV4\UV4.exe")
    [void]$candidates.Add("C:\Keil\UV4\UV4.exe")

    foreach ($p in @("C:\Program Files", "C:\Program Files (x86)")) {
        if (Test-Path $p) {
            foreach ($d in (Get-ChildItem -Path $p -Directory -Filter "Keil*" -ErrorAction SilentlyContinue)) {
                [void]$candidates.Add((Join-Path $d.FullName "UV4\UV4.exe"))
            }
        }
    }
    foreach ($d in (Get-ChildItem -Path "C:\" -Directory -Filter "Keil*" -ErrorAction SilentlyContinue)) {
        [void]$candidates.Add((Join-Path $d.FullName "UV4\UV4.exe"))
    }

    foreach ($c in $candidates) {
        if ($c -and (Test-Path $c)) { return (Resolve-Path $c).Path }
    }
    return $null
}

function Get-LogText([string]$path) {
    if (-not (Test-Path $path)) { return "" }
    $t = [System.IO.File]::ReadAllText($path, [System.Text.Encoding]::Default)
    if ($t -match "Program Size" -or $t -match "Error") { return $t }
    return [System.IO.File]::ReadAllText($path, [System.Text.Encoding]::Unicode)
}

function Test-HexFile([string]$path) {
    if (-not (Test-Path $path)) { return "no file" }
    $lines = Get-Content -Path $path -ErrorAction SilentlyContinue
    if (-not $lines -or $lines.Count -lt 2) { return "empty" }
    $first = ($lines[0]).Trim()
    $last  = ($lines[-1]).Trim()
    if ($first -notlike ":0300000002*") { return "no reset jump" }
    if ($last  -ne ":00000001FF")       { return "no end record" }
    return "ok"
}

Write-Host ""
Write-Host "  8051 HARDWARE LAB - BUILD ALL HEX FILES"
Write-Host "  ======================================="

if ($Undo) {
    Write-Head "Restoring original project files"
    $n = 0
    foreach ($f in (Get-ChildItem -Path $keilDir -Filter "*.bak" -ErrorAction SilentlyContinue)) {
        Move-Item -Path $f.FullName -Destination ($f.FullName -replace "\.bak$", "") -Force
        $n++
    }
    Write-Host "  Restored $n file(s)."
    exit 0
}

if (-not (Test-Path $keilDir)) {
    Write-Host "  Cannot find $keilDir" -ForegroundColor Red
    Write-Host "  Run this script from the tools folder inside the repository."
    exit 1
}

$uv4 = Find-UV4 $KeilPath
if (-not $uv4) {
    Write-Host "  Could not find UV4.exe (Keil uVision)." -ForegroundColor Red
    Write-Host "  Run again with the path to the folder that holds UV4.exe:"
    Write-Host "    .\build_all_hex.ps1 -KeilPath C:\Keil_v5\UV4"
    exit 1
}
Write-Host "  Compiler : $uv4"
Write-Host "  Projects : $keilDir"
Write-Host "  HEX out  : $hexDir"
if ($Small) { Write-Host "  Mode     : size optimised (level 9, favour size)" }
if ($LX51)  { Write-Host "  Mode     : LX51 linker with REMOVEUNUSED" }

New-Item -ItemType Directory -Force -Path $hexDir | Out-Null
New-Item -ItemType Directory -Force -Path $logDir | Out-Null

$projects = Get-ChildItem -Path $keilDir -Filter "*_AT89S52.uvprojx" | Sort-Object Name
if ($Programs.Count -gt 0) {
    $projects = $projects | Where-Object {
        $name = $_.Name
        ($Programs | Where-Object { $name -like "$_*" }).Count -gt 0
    }
}

if (-not $projects) {
    Write-Host "  No matching projects found." -ForegroundColor Red
    exit 1
}

Write-Head "Building $($projects.Count) project(s)"

$results = @()
$index   = 0

foreach ($proj in $projects) {
    $index++
    $base = $proj.Name -replace "_AT89S52\.uvprojx$", ""
    $tag  = $base
    $work = $proj.FullName

    if ($Small -or $LX51) {
        $suffix = ""
        if ($Small) { $suffix += "s" }
        if ($LX51)  { $suffix += "x" }
        $work = Join-Path $keilDir ($base + "_AT89S52_" + $suffix + ".uvprojx")
        $text = [System.IO.File]::ReadAllText($proj.FullName)
        if ($Small) {
            $text = $text -replace "<OLevel>8</OLevel>", "<OLevel>9</OLevel>"
            $text = $text -replace "<OptimizeSize>0</OptimizeSize>", "<OptimizeSize>1</OptimizeSize>"
        }
        if ($LX51) {
            $text = $text -replace "<BL51>", "<LX51>`r`n            <MiscControls>REMOVEUNUSED</MiscControls>"
            $text = $text -replace "</BL51>", "</LX51>"
        }
        [System.IO.File]::WriteAllText($work, $text, [System.Text.Encoding]::UTF8)
    }

    $log = Join-Path $logDir ($tag + ".log")
    if (Test-Path $log) { Remove-Item $log -Force }

    Write-Host ("  [{0,2}/{1,2}] {2}" -f $index, $projects.Count, $tag) -NoNewline

    $pinfo = New-Object System.Diagnostics.ProcessStartInfo
    $pinfo.FileName               = $uv4
    $pinfo.Arguments              = '-j0 -r "' + $work + '" -o "' + $log + '"'
    $pinfo.RedirectStandardOutput = $false
    $pinfo.UseShellExecute        = $false
    $pinfo.CreateNoWindow         = $true
    $pinfo.WorkingDirectory       = $keilDir
    $proc = [System.Diagnostics.Process]::Start($pinfo)
    $proc.WaitForExit()
    $exit = $proc.ExitCode

    $text    = Get-LogText $log
    $code    = 0
    $data    = 0
    $errors  = -1
    $warnings = 0
    $fatal   = ""

    $m = [regex]::Match($text, "Program Size:\s*data=([\d.]+)\s+xdata=(\d+)\s+code=(\d+)")
    if ($m.Success) {
        $data = [double]$m.Groups[1].Value
        $code = [int]$m.Groups[3].Value
    }
    $m = [regex]::Match($text, "(\d+)\s+Error\(s\)\s*,\s*(\d+)\s+Warning\(s\)")
    if ($m.Success) {
        $errors   = [int]$m.Groups[1].Value
        $warnings = [int]$m.Groups[2].Value
    }
    $m = [regex]::Match($text, "(FATAL ERROR L\d+:[^\r\n]*)")
    if ($m.Success) { $fatal = $m.Groups[1].Value.Trim() }
    $m = [regex]::Match($text, "(ERROR L\d+:[^\r\n]*Extended Linker[^\r\n]*)")
    if ($m.Success) { $fatal = $m.Groups[1].Value.Trim() }

    $outName = $tag
    $xm = [regex]::Match([System.IO.File]::ReadAllText($work), "<OutputName>([^<]*)</OutputName>")
    if ($xm.Success) { $outName = $xm.Groups[1].Value }

    $srcHex = Join-Path $keilDir ("Objects\" + $outName + ".hex")
    $dstHex = Join-Path $hexDir  ($outName + ".hex")
    $hexOk  = "not built"
    if (Test-Path $srcHex) {
        Copy-Item $srcHex $dstHex -Force
        $hexOk = Test-HexFile $dstHex
    }

    if ($fatal -ne "")          { $state = "FATAL" }
    elseif ($errors -lt 0)      { $state = "NO LOG" }
    elseif ($errors -gt 0)      { $state = "ERRORS" }
    elseif ($code -eq 0)        { $state = "NO OUTPUT" }
    elseif ($code -gt $limit)   { $state = "OVER LIMIT" }
    elseif ($hexOk -ne "ok")    { $state = "BAD HEX" }
    else                        { $state = "OK" }

    $colour = switch ($state) {
        "OK"         { "Green" }
        "OVER LIMIT" { "Yellow" }
        default      { "Red" }
    }
    Write-Host ("  {0,6} bytes   {1}" -f $code, $state) -ForegroundColor $colour
    if ($fatal -ne "") { Write-Host ("           " + $fatal) -ForegroundColor Red }

    if ($LX51 -and $text -match "BL51") {
        Write-Host "           the log still shows BL51, so the extended linker did not take." -ForegroundColor Yellow
        Write-Host "           Set it by hand once: Options for Target > Device > tick" -ForegroundColor Yellow
        Write-Host "           'Use Extended Linker (LX51) instead of BL51', then" -ForegroundColor Yellow
        Write-Host "           LX51 Misc > Misc Controls: REMOVEUNUSED" -ForegroundColor Yellow
    }

    $results += [pscustomobject]@{
        Program  = $tag
        Code     = $code
        Data     = $data
        Errors   = $errors
        Warnings = $warnings
        Hex      = $hexOk
        State    = $state
    }
}

Write-Head "Summary"

$width = ($results | ForEach-Object { $_.Program.Length } | Measure-Object -Maximum).Maximum
Write-Host ("  {0,-$width}  {1,7}  {2,6}  {3,6}  {4,8}  {5,-10}  {6}" -f "PROGRAM", "CODE", "DATA", "ERR", "WARN", "HEX", "STATE")
Write-Host ("  " + ("-" * ($width + 58)))
foreach ($r in $results) {
    $colour = switch ($r.State) {
        "OK"         { "Green" }
        "OVER LIMIT" { "Yellow" }
        default      { "Red" }
    }
    Write-Host ("  {0,-$width}  {1,7}  {2,6}  {3,6}  {4,8}  {5,-10}  {6}" -f `
        $r.Program, $r.Code, $r.Data, $r.Errors, $r.Warnings, $r.Hex, $r.State) -ForegroundColor $colour
}

$ok    = ($results | Where-Object { $_.State -eq "OK" }).Count
$over  = ($results | Where-Object { $_.State -eq "OVER LIMIT" }).Count
$bad   = ($results | Where-Object { $_.State -ne "OK" -and $_.State -ne "OVER LIMIT" }).Count
$free  = $limit - (($results | ForEach-Object { $_.Code } | Measure-Object -Maximum).Maximum)

Write-Host ""
Write-Host "  $ok ready, $over over the $limit byte limit, $bad failed."
Write-Host "  Largest program has $free bytes of headroom."
Write-Host "  HEX files copied to $hexDir"
Write-Host ""
Write-Host "  Copy that whole folder to a pen drive. In the lab you only need"
Write-Host "  the HEX files and docs\FLASHING.md."
Write-Host ""

if ($bad -gt 0) { exit 2 }
if ($over -gt 0) { exit 1 }
exit 0
