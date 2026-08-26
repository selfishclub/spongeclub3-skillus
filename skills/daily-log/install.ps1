# daily-log 설치 스크립트 (Windows)
# 사용법: powershell -ExecutionPolicy Bypass -File install.ps1

$ErrorActionPreference = "Stop"
Write-Host "== daily-log 스킬 설치 ==" -ForegroundColor Cyan

# 이 스크립트가 있는 폴더 = 스킬 원본
$src = $PSScriptRoot
$dest = Join-Path $env:USERPROFILE ".claude\skills\daily-log"

# 대상 폴더 생성 후 복사
New-Item -ItemType Directory -Force -Path $dest | Out-Null
Copy-Item -Path (Join-Path $src "SKILL.md") -Destination $dest -Force
New-Item -ItemType Directory -Force -Path (Join-Path $dest "scripts") | Out-Null
Copy-Item -Path (Join-Path $src "scripts\build_log.py") -Destination (Join-Path $dest "scripts") -Force
if (Test-Path (Join-Path $src "README.md")) {
    Copy-Item -Path (Join-Path $src "README.md") -Destination $dest -Force
}
Write-Host "[OK] 스킬 복사 완료 -> $dest" -ForegroundColor Green

# Python 확인
$py = (Get-Command python -ErrorAction SilentlyContinue)
if (-not $py) {
    Write-Host "[주의] python 을 찾지 못했습니다. python.org 에서 설치하세요('Add to PATH' 체크)." -ForegroundColor Yellow
} else {
    Write-Host "[OK] Python 발견: $((python --version) 2>&1)" -ForegroundColor Green
    Write-Host "PDF 엔진(reportlab) 설치를 시도합니다..." -ForegroundColor Cyan
    try {
        python -m pip install --quiet reportlab
        Write-Host "[OK] reportlab 준비 완료 (PDF 사용 가능)" -ForegroundColor Green
    } catch {
        Write-Host "[주의] reportlab 설치 실패. MD/HTML은 정상 동작하며, PDF는 나중에 자동 재시도됩니다." -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "설치 끝! Claude Code 를 새로 켠 뒤 '오늘 로그 정리해줘' 라고 해보세요." -ForegroundColor Cyan
