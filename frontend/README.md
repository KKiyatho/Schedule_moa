# 일정모아 프론트엔드 (Frontend)

AI가 문서에서 일정을 읽어 통합 관리하는 앱의 **Flutter 기반 프론트엔드**

## 🏗️ 프로젝트 구조

```
frontend/
├── lib/
│   ├── main.dart                  # 진입점
│   ├── models/                    # 데이터 모델
│   ├── services/
│   │   └── api_service.dart       # API 클라이언트
│   ├── providers/                 # Riverpod 상태 관리
│   ├── screens/                   # 스크린/페이지
│   │   ├── home_screen.dart
│   │   ├── login_screen.dart
│   │   ├── calendar_screen.dart
│   │   ├── items_screen.dart
│   │   └── profile_screen.dart
│   └── widgets/                   # 재사용 가능한 위젯
│       ├── item_card.dart
│       ├── upload_button.dart
│       └── calendar_widget.dart
├── test/                          # 테스트
├── pubspec.yaml                   # Flutter 의존성
└── README.md
```

## 🚀 시작하기

### 1. Flutter 설치 확인

```bash
flutter --version
flutter doctor
```

### 2. 의존성 설치

```bash
flutter pub get
```

### 3. 개발 서버 실행 (웹)

```bash
flutter run -d chrome
```

또는 특정 디바이스 선택:

```bash
flutter devices          # 연결된 디바이스 확인
flutter run -d <device_id>
```

### 4. 모바일 빌드

```bash
# Android
flutter build apk --release

# iOS (macOS만)
flutter build ios --release
```

## 📱 지원 플랫폼

- ✅ Web (Chrome, Firefox, Safari)
- ✅ Android
- ✅ iOS
- ✅ Windows
- ✅ macOS
- ✅ Linux

## 🔧 기술 스택

### State Management
- **Riverpod**: 상태 관리 및 의존성 주입

### HTTP & Networking
- **Dio**: API 클라이언트

### UI Components
- **Material 3**: Google Material Design
- **table_calendar**: 캘린더 위젯

### File & Storage
- **image_picker**: 이미지 선택
- **file_picker**: 파일 선택
- **shared_preferences**: 로컬 저장소
- **hive**: 로컬 데이터베이스
- **flutter_secure_storage**: 보안 저장소

### Authentication
- **google_sign_in**: Google 로그인

### Notifications
- **flutter_local_notifications**: 로컬 알림

## 📋 주요 화면

### 1. 로그인 화면
- 이메일 로그인
- Google OAuth 로그인
- 회원 가입

### 2. 홈/대시보드
- 오늘의 일정
- 이번주 일정
- 마감 임박 항목
- 완료율

### 3. 일정 관리
- 캘린더 뷰
- 리스트 뷰
- 필터링 (일정/마감/할 일)
- 상세보기 및 편집

### 4. 파일 업로드
- PDF/이미지 업로드
- AI 처리 결과 확인
- 자동 분류 결과 검증

### 5. 프로필
- 사용자 정보
- Google Calendar 동기화 설정
- 알림 설정
- 로그아웃

## 🔌 API 통합

### 기본 설정

```dart
import 'package:schedule_moa/services/api_service.dart';

final api = ApiService();

// 헬스 체크
bool isHealthy = await api.healthCheck();

// 로그인
String? token = await api.login(
  email: 'user@example.com',
  password: 'password',
);

// 토큰 설정
api.setAuthToken(token!);

// 일정 조회
List<dynamic>? items = await api.getItems(itemType: 'schedule');
```

## 🧪 테스트 실행

```bash
# 모든 테스트 실행
flutter test

# 특정 파일 테스트
flutter test test/widgets/home_test.dart

# 상세 출력
flutter test --verbose
```

## 🛠️ 개발 팁

### 핫 리로드
개발 중 코드 변경 시 `r` 키를 눌러 핫 리로드

### 디버그 모드
DevTools 접속:
```bash
flutter run -d chrome
# 브라우저에서 DevTools 열기
```

### 코드 포맷팅
```bash
dart format lib/
```

### 린트 체크
```bash
flutter analyze
```

## 📚 프로젝트 마일스톤

### Week 1: 기초 UI
- [ ] 로그인/회원가입 화면
- [ ] 홈 스크린
- [ ] 네비게이션 구조

### Week 2: 기본 기능
- [ ] 파일 업로드 UI
- [ ] 캘린더 통합
- [ ] 일정 목록 표시

### Week 3: API 연동
- [ ] 백엔드 API 연결
- [ ] 실시간 데이터 동기화
- [ ] 에러 핸들링

### Week 4: 고도화
- [ ] 알림 시스템
- [ ] Google Calendar 연동
- [ ] 성능 최적화

## 🐛 트러블슈팅

### "포트 이미 사용 중" 에러
```bash
flutter run -d chrome --port 5001
```

### 의존성 오류
```bash
flutter pub get --no-example
flutter clean && flutter pub get
```

### 빌드 에러
```bash
flutter clean
flutter pub get
flutter pub run build_runner build
```

## 📖 참고 자료

- [Flutter 공식 문서](https://flutter.dev/docs)
- [Riverpod 가이드](https://riverpod.dev/)
- [Dio 문서](https://pub.dev/packages/dio)
- [Material 3 가이드](https://m3.material.io/)

## 🤝 기여

이슈나 PR은 언제든 환영합니다!

## 📄 라이선스

MIT License
