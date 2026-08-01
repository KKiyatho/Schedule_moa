# 📅 일정모아 1개월 MVP 개발 계획

## 1. MVP 목표 및 범위

### 🎯 1개월 MVP 목표
**"AI가 PDF/이미지에서 일정을 읽어서, 통합 캘린더에 표시하고, 할 일 완료까지 경험하는 전체 흐름을 동작시키기"**

### ✅ MVP 포함 사항
- ✅ PDF/이미지 업로드 기능
- ✅ AI 텍스트 추출 및 일정/마감/할 일 분류
- ✅ 추출 결과 수정 기능
- ✅ Google Calendar 연동 (읽기/쓰기)
- ✅ 통합 대시보드 (오늘, 이번주, 마감 임박)
- ✅ 알림 기능 (기본 알림)
- ✅ 할 일 체크 및 완료 피드백
- ✅ 데이터베이스 저장

### ❌ MVP 제외 사항 (2차 확장)
- ❌ 반복 일정 자동 학습
- ❌ Notion/외부 캘린더 연동
- ❌ 차등/반복 알림 고급 기능
- ❌ 모바일 푸시 알림 (데스크톱 알림만)
- ❌ 사용자 커스터마이징 심화

---

## 2. 기술 스택 (최소화)

### 백엔드
- **언어**: Python 3.11+
- **프레임워크**: FastAPI
- **DB**: PostgreSQL (로컬 개발 시 SQLite 가능)
- **AI**: Azure OpenAI (또는 OpenAI API)
- **파일 처리**: python-pptx, pdf2image, pytesseract (OCR), Pillow
- **캘린더**: google-auth-oauthlib, google-api-python-client

### 프론트엔드
- **언어**: Dart 3.0+
- **프레임워크**: Flutter 3.10+
- **UI 라이브러리**: Material 3 (Flutter 기본)
- **캘린더**: table_calendar 또는 syncfusion_flutter_calendar
- **상태 관리**: Riverpod 또는 Provider
- **파일 업로드**: image_picker, file_picker

### 개발 도구
- **개발 서버**: Flutter pub + hot reload
- **API 클라이언트**: http 또는 dio
- **테스트**: pytest (백엔드), flutter test (프론트엔드)
- **배포**: Docker (백엔드), Flutter build (iOS/Android/Web)

---

## 3. 데이터 모델 설계

### 3-1. 핵심 테이블

```sql
-- 사용자
CREATE TABLE users (
  id UUID PRIMARY KEY,
  email VARCHAR UNIQUE NOT NULL,
  google_access_token VARCHAR,
  google_refresh_token VARCHAR,
  created_at TIMESTAMP
);

-- 업로드된 문서
CREATE TABLE documents (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(id),
  file_name VARCHAR,
  file_path VARCHAR,
  file_type VARCHAR (pdf, image, text),
  extracted_text TEXT,
  status VARCHAR (pending, extracted, classified),
  created_at TIMESTAMP
);

-- 추출된 항목
CREATE TABLE extracted_items (
  id UUID PRIMARY KEY,
  document_id UUID REFERENCES documents(id),
  user_id UUID REFERENCES users(id),
  title VARCHAR NOT NULL,
  description TEXT,
  item_type VARCHAR (schedule, deadline, todo),
  due_date DATE,
  due_time TIME,
  location VARCHAR,
  priority INTEGER (1-5),
  status VARCHAR (pending, confirmed, synced),
  google_event_id VARCHAR (Google Calendar 연동 ID),
  created_at TIMESTAMP,
  updated_at TIMESTAMP
);

-- 완료된 할 일
CREATE TABLE completed_todos (
  id UUID PRIMARY KEY,
  item_id UUID REFERENCES extracted_items(id),
  user_id UUID REFERENCES users(id),
  completed_at TIMESTAMP
);

-- 알림 로그
CREATE TABLE notifications (
  id UUID PRIMARY KEY,
  item_id UUID REFERENCES extracted_items(id),
  user_id UUID REFERENCES users(id),
  notification_type VARCHAR (before_1day, before_3hours, deadline),
  scheduled_at TIMESTAMP,
  sent_at TIMESTAMP
);
```

### 3-2. API 응답 스키마 (TypeScript)

```typescript
// 추출 결과
interface ExtractedItem {
  id: string;
  title: string;
  description?: string;
  itemType: 'schedule' | 'deadline' | 'todo';
  dueDate: string; // ISO date
  dueTime?: string; // HH:MM
  location?: string;
  priority: 1 | 2 | 3 | 4 | 5;
  confidence: number; // 0-1 분류 신뢰도
}

// 문서 업로드 응답
interface DocumentUploadResponse {
  documentId: string;
  extractedItems: ExtractedItem[];
  totalItems: number;
  processingTime: number; // ms
}

// 통합 대시보드 응답
interface DashboardResponse {
  today: ExtractedItem[];
  thisWeek: ExtractedItem[];
  upcomingDeadlines: ExtractedItem[];
  completedTodos: number;
  pendingTodos: number;
}
```

---

## 4. 주차별 상세 계획

## 🔵 1주차: 기초 인프라 & 문서 처리

### 목표
"PDF/이미지에서 텍스트를 추출하고, AI가 일정 정보를 인식하는 것까지"

### 1-1. 프로젝트 초기 설정 (1일)
- [ ] 프로젝트 구조 생성 (backend, frontend 분리)
- [ ] 백엔드: FastAPI + SQLAlchemy 보일러플레이트
- [ ] 프론트엔드: React + TypeScript + Vite 초기 설정
- [ ] Docker Compose로 PostgreSQL 로컬 실행 환경 구성
- [ ] Git 저장소 초기화 및 .gitignore 설정

**산출물:**
- `backend/main.py` (FastAPI 앱 기본 구조)
- `frontend/src/` (React 기본 구조)
- `docker-compose.yml`

---

### 1-2. 문서 업로드 API (2-3일)
**백엔드:**
- [ ] FastAPI 엔드포인트: `POST /api/documents/upload`
- [ ] 파일 저장 로직 (로컬 디렉토리 또는 S3)
- [ ] PDF → 이미지 변환 (pdf2image)
- [ ] OCR (Tesseract 또는 Azure Document Intelligence)
- [ ] 텍스트 추출 후 DB 저장

**프론트엔드:**
- [ ] 파일 선택 버튼 (image_picker, file_picker)
- [ ] 업로드 진행도 표시
- [ ] 업로드 완료 후 결과 화면 준비

**산출물:**
```dart
// frontend/lib/services/document_service.dart
future<DocumentUploadResponse> uploadDocument(File file, String userId) async {
  final request = http.MultipartRequest(
    'POST',
    Uri.parse('http://localhost:8000/api/documents/upload'),
  );
  request.fields['user_id'] = userId;
  request.files.add(await http.MultipartFile.fromPath('file', file.path));
  
  final response = await request.send();
  return DocumentUploadResponse.fromJson(jsonDecode(await response.stream.bytesToString()));
}
```

---

### 1-3. AI 분류 로직 (2-3일)
**백엔드:**
- [ ] Azure OpenAI / OpenAI API 연결
- [ ] 프롬프트 설계: 날짜, 시간, 제목, 타입 추출
- [ ] AI 응답 파싱 및 구조화

**프롬프트 예시:**
```
다음 텍스트에서 일정/마감/할 일 정보를 추출하세요.

텍스트:
---
{extracted_text}
---

응답 형식 (JSON):
[
  {
    "title": "회의명/작업명",
    "itemType": "schedule" | "deadline" | "todo",
    "dueDate": "2026-08-15",
    "dueTime": "14:00",
    "location": "장소 (선택)",
    "description": "설명",
    "confidence": 0.95
  }
]
```

**프론트엔드:**
- [ ] AI 분류 결과 ListTile/Card로 표시
- [ ] 항목별 편집 기능 (제목, 날짜, 타입 변경)
- [ ] 저장/취소 버튼 (FloatingActionButton, ElevatedButton)

**산출물:**
```python
# backend/app/services/ai_classifier.py
async def classify_text(text: str) -> List[ExtractedItem]:
    # OpenAI API 호출
    # JSON 파싱
    # 검증 및 반환
    pass
```

---

### 1주차 마일스톤
- ✅ 문서 업로드 → OCR → 텍스트 추출
- ✅ AI가 텍스트에서 일정/마감/할 일 분류
- ✅ 결과 수정 및 저장 가능

**테스트:**
- 샘플 PDF 3개로 테스트
- 분류 정확도 70% 이상 목표

---

## 🔵 2주차: Google Calendar 연동 & 대시보드

### 목표
"추출된 일정을 Google Calendar에 동기화하고, 통합 대시보드에서 보기"

### 2-1. Google Calendar API 연동 (2일)
**백엔드:**
- [ ] OAuth 2.0 인증 흐름 구현
- [ ] `POST /api/auth/google` - 구글 로그인
- [ ] `POST /api/calendars/sync` - Google Calendar에 일정 생성
- [ ] `GET /api/calendars/events` - Google Calendar 일정 읽기
- [ ] 중복 확인 로직 (같은 일정 중복 생성 방지)

**프론트엔드:**
- [ ] 구글 로그인 버튼 (google_sign_in 패키지)
- [ ] 로그인 후 토큰 저장 (flutter_secure_storage)

**산출물:**
```python
# backend/app/services/google_calendar.py
async def sync_to_google_calendar(item: ExtractedItem, user: User):
    # Google Calendar API 호출
    # event 생성
    # event_id 저장
    pass
```

---

### 2-2. 통합 대시보드 (2-3일)
**백엔드:**
- [ ] `GET /api/dashboard?date=2026-08-01` 엔드포인트
- [ ] 응답: { today: [...], thisWeek: [...], upcomingDeadlines: [...] }

**프론트엔드:**
- [ ] 오늘 일정 카드
- [ ] 이번 주 마감 카드
- [ ] 할 일 리스트 (미완료/완료)
- [ ] 통계 (오늘 할 일 개수, 완료율 등)

**산출물:**
```dart
// frontend/lib/screens/dashboard_screen.dart
class DashboardScreen extends ConsumerStatefulWidget {
  @override
  ConsumerState<DashboardScreen> createState() => _DashboardScreenState();
}

class _DashboardScreenState extends ConsumerState<DashboardScreen> {
  @override
  void initState() {
    super.initState();
    ref.read(dashboardProvider.notifier).fetchDashboard();
  }
  
  @override
  Widget build(BuildContext context) {
    final dashboard = ref.watch(dashboardProvider);
    
    return Scaffold(
      appBar: AppBar(title: Text('일정모아')),
      body: ListView(
        children: [
          TodaySchedulesWidget(items: dashboard.today),
          ThisWeekDeadlinesWidget(items: dashboard.thisWeek),
          TodoListWidget(items: dashboard.todos),
        ],
      ),
    );
  }
}
```

---

### 2-3. 캘린더 뷰 (1-2일)
**프론트엔드:**
- [ ] 월간 캘린더 보기 (table_calendar)
- [ ] 일정/마감/할 일 색상 구분
- [ ] 클릭하면 상세 보기 (BottomSheet 또는 Dialog)

---

### 2주차 마일스톤
- ✅ Google Calendar 로그인 & 연동
- ✅ 추출 일정을 Google Calendar에 동기화
- ✅ 통합 대시보드에서 한눈에 확인
- ✅ 캘린더 뷰에서 일정 확인

**테스트:**
- Google Calendar 실제 연동 테스트
- 대시보드 데이터 정확성 확인

---

## 🔵 3주차: 알림 & 할 일 완료 피드백

### 목표
"알림이 발송되고, 할 일을 완료했을 때 성취감을 느낄 수 있는 상태"

### 3-1. 알림 시스템 (2-3일)
**백엔드:**
- [ ] 예약 작업 (Celery 또는 APScheduler)
- [ ] 알림 규칙: 
  - 일정: 1일 전, 당일 오전
  - 마감: 3일 전, 1일 전, 당일
  - 할 일: 매일 오전 (미완료시)
- [ ] DB에 알림 로그 저장

**프론트엔드:**
- [ ] 푸시 알림 (flutter_local_notifications, firebase_messaging)
- [ ] 알림 센터 (앱 내 알림 히스토리)
- [ ] 알림 설정 페이지

**산출물:**
```python
# backend/app/services/notifications.py
@scheduler.scheduled_job('cron', hour=9, minute=0)
async def send_daily_notifications():
    # 오늘 할 일 확인
    # 미완료 할 일 알림 발송
    pass
```

---

### 3-2. 할 일 완료 & 피드백 (2일)
**백엔드:**
- [ ] `PUT /api/todos/{id}/complete` 엔드포인트
- [ ] completed_todos 테이블에 기록
- [ ] 완료율 계산

**프론트엔드:**
- [ ] 체크박스 클릭 → 애니메이션
- [ ] 완료 메시지 표시 ("완료됨!", "좋아요, 1개 완료!")
- [ ] 일일 목표 완료 시 특별 메시지

**산출물:**
```dart
// frontend/lib/widgets/todo_item.dart
class TodoItem extends ConsumerWidget {
  final ExtractedItem item;
  
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return ListTile(
      title: Text(item.title),
      trailing: Checkbox(
        value: item.isCompleted,
        onChanged: (value) async {
          if (value!) {
            await ref.read(todosProvider.notifier).completeTodo(item.id);
            // 축하 애니메이션 표시
            showSuccessAnimation(context);
          }
        },
      ),
    );
  }
}
```

---

### 3-3. 알림 설정 UI (1-2일)
**프론트엔드:**
- [ ] 항목별 알림 시간 조정
- [ ] 진동 활성화/비활성화
- [ ] 알림 음소거 시간대

---

### 3주차 마일스톤
- ✅ 예약된 알림 발송
- ✅ 브라우저 알림 표시
- ✅ 할 일 체크 시 완료 피드백
- ✅ 사용자가 알림 설정 조정 가능

**테스트:**
- 실제 알림 발송 확인
- 완료 피드백 UX 테스트

---

## 🔵 4주차: 마무리 & 배포

### 목표
"MVP 완성 및 발표 준비"

### 4-1. 예외 처리 & 에러 핸들링 (2-3일)
- [ ] 파일 업로드 실패 처리
- [ ] AI 분류 오류 처리
- [ ] Google Calendar 연동 오류 처리
- [ ] 네트워크 오류 재시도 로직
- [ ] 권한 오류 메시지

---

### 4-2. 데이터 검증 및 샘플 데이터 (1-2일)
**백엔드:**
- [ ] Pydantic 모델 정의 (입출력 검증)
- [ ] 비즈니스 로직 검증 (날짜 범위, 우선순위 등)

**테스트 데이터:**
- [ ] 샘플 PDF 5개 준비
- [ ] 분류 정확도 테스트

---

### 4-3. UI/UX 다듬기 (1-2일)
**프론트엔드:**
- [ ] 반응형 디자인 확인
- [ ] 다크 모드 지원 (선택사항)
- [ ] 로딩 상태 표시
- [ ] 빈 상태 화면 (empty state)

---

### 4-4. 배포 준비 (1일)
- [ ] Docker 이미지 빌드
- [ ] 환경 변수 설정 (.env)
- [ ] 데이터베이스 마이그레이션 스크립트
- [ ] README 작성

---

### 4-5. 발표 자료 준비 (1-2일)
- [ ] 시나리오 시나리오 문서 작성
  - 시나리오 1: "회의 일정이 PDF에 있어요" → 자동 추출 → 구글 캘린더 동기화 → 대시보드 확인
  - 시나리오 2: "마감이 다가왔어요" → 알림 받기 → 할 일 완료 → 축하 메시지
- [ ] 시나리오별 스크린샷
- [ ] 데모 스크립트 작성
- [ ] 발표 슬라이드

---

### 4주차 마일스톤
- ✅ MVP 모든 기능 완성
- ✅ 예외 처리 및 에러 핸들링
- ✅ 배포 가능한 상태
- ✅ 발표 준비 완료

---

## 5. 우선순위 (MoSCoW)

### MUST (필수)
1. 문서 업로드 & OCR
2. AI 일정 분류
3. 추출 결과 수정
4. Google Calendar 동기화
5. 통합 대시보드 (오늘/이번주)
6. 할 일 완료 & 피드백

### SHOULD (높음 우선순위)
1. 알림 기능
2. 캘린더 뷰
3. 알림 설정
4. 예외 처리

### COULD (선택사항)
1. 고급 알림 규칙
2. 반복 일정
3. Notion 연동
4. 다크 모드

### WON'T (1차 제외)
1. 모바일 앱
2. 팀 협업 기능
3. AI 분류 재학습

---

## 6. 일일 체크리스트 (예시)

### 1주차 목표: 문서 처리 & AI 분류

**Day 1-2: 프로젝트 초기화**
```
[ ] FastAPI 보일러플레이트
[ ] Flutter 초기 설정 (flutter create)
[ ] Docker Compose (PostgreSQL)
[ ] 프로젝트 구조 설계
```

**Day 3-4: 문서 업로드**
```
[ ] 파일 업로드 API
[ ] PDF → 이미지 변환
[ ] OCR 통합 (Tesseract)
[ ] DB 저장 로직
[ ] UI 화면 (파일 선택, 업로드 진행도)
```

**Day 5-7: AI 분류**
```
[ ] OpenAI API 연결
[ ] 프롬프트 설계
[ ] JSON 파싱 로직
[ ] 결과 수정 UI
[ ] 저장 기능
```

---

## 7. 배포 계획

### 로컬 개발 (1-3주차)
```bash
# 백엔드 실행
cd backend
python -m uvicorn app.main:app --reload

# 프론트엔드 실행 (Android/iOS 에뮬레이터)
cd frontend
flutter pub get
flutter run

# 또는 웹
flutter run -d chrome

# DB 실행
docker-compose up -d postgresql
```

### 4주차 배포
```bash
# 백엔드 Docker로 패키징
docker build -t schedule-moa-backend ./backend

# 프론트엔드 빌드
cd frontend

# Android APK 빌드
flutter build apk --release

# iOS 빌드
flutter build ios --release

# 웹 빌드
flutter build web --release

# 배포 (선택사항: Heroku, Railway, Render 등)
docker-compose -f docker-compose.prod.yml up
```

---

## 8. 성공 기준 (MVP)

### 기능 완성도
- ✅ PDF/이미지 업로드 → 텍스트 추출 (성공률 90%)
- ✅ AI 분류 정확도 70% 이상
- ✅ Google Calendar 동기화 100%
- ✅ 대시보드 데이터 정확성 100%

### 사용성
- ✅ 새 사용자도 5분 내 첫 일정 등록 가능
- ✅ 알림이 예정 시간에 발송됨
- ✅ 할 일 완료 피드백이 자연스러움

### 기술 품질
- ✅ API 응답 시간 < 2초
- ✅ 에러 처리율 99% 이상
- ✅ 테스트 커버리지 70% 이상

---

## 9. 위험 요소 & 대응

| 위험 | 확률 | 영향 | 대응 |
|------|------|------|------|
| AI 분류 정확도 부족 | 높음 | 높음 | 샘플 데이터 다양화, 프롬프트 반복 개선 |
| Google Calendar API 한계 | 중간 | 중간 | 공식 문서 사전 검토, 최소 기능부터 구현 |
| 개발 지연 (1주 이상) | 중간 | 높음 | 우선순위 재조정 (MUST만 집중) |
| 데이터베이스 성능 | 낮음 | 중간 | 인덱싱, 쿼리 최적화 |

---

## 10. 커뮤니케이션 & 체크포인트

### 주간 점검 (매주 금요일)
- [ ] 주차 목표 달성도 확인
- [ ] 이슈 사항 정리
- [ ] 다음 주 조정사항 논의

### 예상 회의 내용
1. **1주 회의**: 문서 처리 + AI 분류 동작 확인
2. **2주 회의**: Google Calendar 연동 + 대시보드 기능
3. **3주 회의**: 알림 + 완료 피드백 UX
4. **4주 회의**: 최종 검증 + 발표 리허설

---

## 11. 핵심 산출물 목록

### 주차별 산출물

**1주차**
- `backend/app/api/documents.py` (업로드 API)
- `backend/app/services/ai_classifier.py` (분류 로직)
- `frontend/lib/screens/document_upload_screen.dart` (업로드 UI)
- `frontend/lib/screens/classification_review_screen.dart` (검토 UI)

**2주차**
- `backend/app/services/google_calendar.py` (Google Calendar 연동)
- `backend/app/api/calendars.py` (캘린더 API)
- `frontend/lib/screens/dashboard_screen.dart` (대시보드)
- `frontend/lib/screens/calendar_screen.dart` (캘린더 뷰)

**3주차**
- `backend/app/services/notifications.py` (알림 로직)
- `backend/app/api/notifications.py` (알림 API)
- `frontend/lib/widgets/todo_item.dart` (할 일 아이템)
- `frontend/lib/screens/notification_settings_screen.dart` (설정)

**4주차**
- `docker-compose.yml` (배포 구성)
- `README.md` (프로젝트 문서)
- `DEMO_SCENARIO.md` (시나리오)
- 발표 슬라이드

---

## 12. 시작하기 위한 체크리스트

**지금 바로 시작하려면:**

```
[ ] 팀 구성 확인 (백엔드, 프론트엔드, AI 담당)
[ ] Azure OpenAI / OpenAI API 키 준비
[ ] Google OAuth 클라이언트 ID/Secret 준비
[ ] PostgreSQL 설치 확인
[ ] Python 3.11+, Flutter 3.10+ 설치 확인
[ ] Android Studio (또는 Xcode) 설치 확인
[ ] Git 저장소 생성
[ ] 프로젝트 디렉토리 초기화 (flutter create)
[ ] Day 1부터 시작!
```

---

**이 MVP 계획은 Agile 방식으로 진행하며, 매일 15분 스탠드업을 통해 진행상황을 공유합니다.**

**준비되셨나요? Day 1부터 바로 시작해볼까요?** 🚀
