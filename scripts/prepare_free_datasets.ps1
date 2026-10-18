# Free local-first dataset setup helper for Windows PowerShell.
# Run from the repository root:
# powershell -ExecutionPolicy Bypass -File .\scripts\prepare_free_datasets.ps1
# No cloud GPU, paid API, subscription or hosted training is used.
$ErrorActionPreference = "Stop"
$root = Join-Path (Get-Location) "datasets"
New-Item -ItemType Directory -Force -Path $root | Out-Null

Write-Host "Downloads are optional. Check your disk space and internet/data plan first."
Write-Host "Nothing is uploaded to GitHub. This script does not approve licences or labels."
Write-Host ""

$choice = Read-Host "Download C3PI sample data (~493 MB; prescription pills only)? Type YES to proceed"
if ($choice -ceq "YES") {
    $zip = Join-Path $root "C3PI_sampleData.zip"
    $url = "https://data.lhncbc.nlm.nih.gov/public/Pills/sampleData.zip"
    if (-not (Test-Path $zip)) {
        Invoke-WebRequest -Uri $url -OutFile $zip
    } else {
        Write-Host "Archive already exists; not downloading again: $zip"
    }
    Write-Host "Archive saved: $zip"
    Write-Host "Source terms: https://catalog.data.gov/dataset/computational-photography-project-for-pill-identification-c3pi"
    Write-Host "This dataset is a prescription-pill proxy, NOT illicit-narcotics ground truth."
    $extract = Read-Host "Extract archive locally? Type YES to proceed"
    $dest = Join-Path $root "C3PI_sampleData"
    if ($extract -ceq "YES" -and -not (Test-Path $dest)) {
        Expand-Archive -LiteralPath $zip -DestinationPath $dest
        Write-Host "Extracted to $dest"
    }
} else {
    Write-Host "Skipped C3PI download."
}

Write-Host ""
Write-Host "FloodNet: 2,343 aerial images and semantic segmentation labels."
Write-Host "It does NOT contain a person class; it cannot by itself train a rescue-person detector."
$floodChoice = Read-Host "Download the official FloodNet Dropbox folder as an archive? It may be large. Type DOWNLOAD to proceed"
if ($floodChoice -ceq "DOWNLOAD") {
    $floodZip = Join-Path $root "FloodNet_download.zip"
    $floodUrl = "https://www.dropbox.com/scl/fo/k33qdif15ns2qv2jdxvhx/ANGaa8iPRhvlrvcKXjnmNRc?dl=1&rlkey=ao2493wzl1cltonowjdbrnp7f"
    if (-not (Test-Path $floodZip)) {
        Invoke-WebRequest -Uri $floodUrl -OutFile $floodZip
        if ((Get-Item $floodZip).Length -lt 100000) {
            Remove-Item $floodZip -Force
            throw "Dropbox response was unexpectedly small; no archive retained. Open the official page in a browser and download from there."
        }
    } else {
        Write-Host "Archive already exists; not downloading again: $floodZip"
    }
    Write-Host "Archive downloaded to $floodZip"
    Write-Host "Inspect the archive and verify source terms before extraction."
    $extractFlood = Read-Host "Extract FloodNet locally? Type YES to proceed"
    $floodDest = Join-Path $root "FloodNet"
    if ($extractFlood -ceq "YES" -and -not (Test-Path $floodDest)) {
        Expand-Archive -LiteralPath $floodZip -DestinationPath $floodDest
        Write-Host "Extracted to $floodDest"
    }
} else {
    Write-Host "Skipped automatic FloodNet download. Official source links:"
    Write-Host "https://github.com/BinaLab/FloodNet-Supervised_v1.0"
    Write-Host "https://www.dropbox.com/scl/fo/k33qdif15ns2qv2jdxvhx/ANGaa8iPRhvlrvcKXjnmNRc?dl=0&e=2&rlkey=ao2493wzl1cltonowjdbrnp7f"
    Write-Host "Review the CDLA-Permissive 1.0 terms and required citation before use."
}
Write-Host ""
Write-Host "Next: inventory images with tools\dataset_inventory.py; review rights and labels manually."
Write-Host "Do not commit datasets or model weights to Git."
