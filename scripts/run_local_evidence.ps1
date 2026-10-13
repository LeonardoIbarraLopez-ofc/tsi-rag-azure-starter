$ErrorActionPreference = "Stop"
$env:UV_CACHE_DIR = Join-Path (Get-Location) '.uv-cache'

Write-Output "=== TESTS ==="
uv run pytest -vv

Write-Output "=== GOLDEN SET ==="
uv run python scripts/evaluate_golden_set.py

Write-Output "=== ARCHIVOS DE EVIDENCIA ==="
Get-ChildItem reports -File -ErrorAction SilentlyContinue | Select-Object Name, Length
Get-ChildItem logs -File -ErrorAction SilentlyContinue | Select-Object Name, Length
