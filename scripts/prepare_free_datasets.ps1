# Free local-first dataset setup helper for Windows PowerShell.
# No cloud GPU, paid API, subscription or hosted training is used.
# Run from the repository root: powershell -ExecutionPolicy Bypass -File .\scripts\prepare_free_datasets.ps1
$ErrorActionPreference = "Stop"
$root = Join-Path (Get-Location) "datasets"
New-Item -ItemType Directory -Force -Path $root | Out-Null
Write-Host "Dataset downloads are optional and may use substantial disk space/bandwidth."
Write-Host "No image is considered licensed or correctly labelled by this script."
Write-Host ""
$choice = Read-Host "Download the C3PI sample archive (~493 MB) for prescription-pill tooling tests? Type YES to proceed"
if ($choice -ceq "YES") {
    $zip = Join-Path $root "C3PI_sampleData.zip"
    $dest = Join-Path $root "C3PI_sampleData"
    $url = "https://data.lhncbc.nlm.nih.gov/public/Pills/sampleData.zip"
    if (-not (Test-Path $zip)) {
        Invoke-WebRequest -Uri $url -OutFile $zip
    } else {
        Write-Host "Archive already exists; not downloading again: $zip"
    }
    Write-Host "Downloaded archive: $zip"
    Write-Host "Verify the source terms and checksum before extraction. This is prescription-pill data, NOT illicit narcotics ground truth."
    $extract = Read-Host "Extract archive now? Type YES to proceed"
    if ($extract -ceq "YES" -and -not (Test-Path $dest)) {
        Expand-Archive -LiteralPath $zip -DestinationPath $dest
        Write-Host "Extracted to $dest"
    }
} else {
    Write-Host "Skipped C3PI download."
}
Write-Host ""
Write-Host "FloodNet source (2,343 aerial images; segmentation classes do not include people):"
Write-Host "https://github.com/BinaLab/FloodNet-Supervised_v1.0"
Write-Host "Official dataset download folder:"
Write-Host "https://www.dropbox.com/scl/fo/k33qdif15ns2qv2jdxvhx/ANGaa8iPRhvlrvcKXjnmNRc?dl=0&e=2&rlkey=ao2493wzl1cltonowjdbrnp7f"
Write-Host "Download via the official source page only after reviewing the CDLA-Permissive 1.0 terms and required citation."
Write-Host "Save files under datasets\FloodNet\; keep downloaded data out of Git."
Write-Host ""
Write-Host "Next: create an inventory with tools\dataset_inventory.py and manually review every licence and label."
