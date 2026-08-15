# Schedule Moa 풀 스택 실행 스크립트
# 사용법: ./start-app.ps1

Write-Host "🚀 Schedule Moa - 풀 스택 시작..." -ForegroundColor Cyan
Write-Host "백엔드와 프론트엔드를 동시에 실행합니다`n" -ForegroundColor Yellow

# Backend 시작 (새 PowerShell 창에서)
Write-Host "📦 백엔드 서버 시작 중..." -ForegroundColor Green
$backendScript = @"
cd backend
c:/dev/Schedule_moa/.venv/Scripts/python.exe -m uvicorn main:app --reload --host 0.0.0.0
"@
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd c:\dev\Schedule_moa; $backendScript"

# 백엔드 시작 대기
Write-Host "⏳ 백엔드 시작 대기 중... (3초)" -ForegroundColor Yellow
Start-Sleep -Seconds 3

# Frontend 시작
Write-Host "📱 프론트엔드 시작 중..." -ForegroundColor Green
Push-Location frontend
flutter run -d chrome
Pop-Location
