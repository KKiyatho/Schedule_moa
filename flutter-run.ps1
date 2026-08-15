# Flutter Chrome 실행 스크립트
# 사용법: ./flutter-run.ps1

Write-Host "📱 Schedule Moa - Flutter Chrome 시작..." -ForegroundColor Cyan

# frontend 디렉토리로 이동
Push-Location frontend

# Flutter 실행
Write-Host "🚀 Flutter app 시작 중..." -ForegroundColor Green
flutter run -d chrome

# 원래 디렉토리로 돌아감
Pop-Location
