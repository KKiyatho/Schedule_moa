# 일정모아 백엔드 (Backend)

AI가 PDF/이미지에서 일정을 읽어 통합 관리하는 앱의 **FastAPI 기반 백엔드**

## 🏗️ 프로젝트 구조

```
backend/
├── main.py                 # FastAPI 앱 진입점
├── requirements.txt        # 의존성
├── .env.example           # 환경 변수 템플릿
├── app/
│   ├── __init__.py
│   ├── core/              # 설정, 보안
│   │   ├── config.py      # 환경 설정
│   │   └── security.py    # 인증, 토큰 생성
│   ├── models/            # SQLAlchemy 모델
│   │   └── __init__.py    # User, Document, ExtractedItem
│   ├── schemas/           # Pydantic 스키마
│   │   └── __init__.py    # API 요청/응답 검증
│   ├── db/                # 데이터베이스
│   │   ├── base.py        # SQLAlchemy 설정
│   │   └── session.py     # 세션 관리
│   ├── crud/              # 데이터 조작
│   │   ├── user.py        # 사용자 CRUD
│   │   ├── document.py    # 문서 CRUD
│   │   └── item.py        # 일정항목 CRUD
│   ├── api/               # API 엔드포인트
│   │   └── v1/
│   │       ├── api.py     # 라우터 통합
│   │       └── endpoints/
│   │           ├── auth.py        # 인증
│   │           ├── documents.py   # 문서 업로드/조회
│   │           ├── items.py       # 일정/마감/할 일
│   │           └── calendar.py    # Google Calendar
│   └── utils/             # 유틸리티 함수
│       ├── ai.py          # AI/LLM 처리
│       └── file_processor.py  # 파일 처리
├── tests/                 # 테스트
│   └── test_auth.py       # 인증 테스트
├── migrations/            # Alembic 마이그레이션
└── uploads/               # 업로드된 파일
```

## 🚀 시작하기

### 1. 환경 설정

```bash
# 백엔드 폴더 이동
cd backend

# 가상환경 생성
python -m venv venv

# 가상환경 활성화
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 환경 변수 설정
copy .env.example .env
# 또는
cp .env.example .env
```

### 2. 의존성 설치

```bash
pip install -r requirements.txt
```

### 3. 개발 서버 실행

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 4. 테스트

**Swagger UI에서 테스트:**
```
http://localhost:8000/docs
```

**cURL로 테스트:**
```bash
# 건강 검사
curl http://localhost:8000/health

# 사용자 등록
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","full_name":"User Name"}'
```

## 📋 API 엔드포인트

### Authentication
- `POST /api/v1/auth/register` - 사용자 등록
- `POST /api/v1/auth/login` - 로그인
- `GET /api/v1/auth/me` - 현재 사용자 정보

### Documents
- `POST /api/v1/documents/upload` - 파일 업로드
- `GET /api/v1/documents/` - 문서 목록
- `GET /api/v1/documents/{document_id}` - 문서 상세
- `DELETE /api/v1/documents/{document_id}` - 문서 삭제

### Items (Schedule/Deadline/Todo)
- `GET /api/v1/items/` - 항목 목록
- `GET /api/v1/items/{item_id}` - 항목 상세
- `POST /api/v1/items/` - 항목 생성
- `PUT /api/v1/items/{item_id}` - 항목 수정
- `POST /api/v1/items/{item_id}/complete` - 항목 완료 표시
- `DELETE /api/v1/items/{item_id}` - 항목 삭제

### Calendar
- `POST /api/v1/calendar/sync` - Google Calendar 동기화
- `GET /api/v1/calendar/events` - Calendar 이벤트 조회

## 🗄️ 데이터베이스

### 기본 설정
- **Type**: PostgreSQL (프로덕션) / SQLite (개발)
- **ORM**: SQLAlchemy
- **마이그레이션**: Alembic

### 테이블 구조

**users**
- id (UUID, PK)
- email (String, Unique)
- full_name (String)
- google_access_token (String)
- google_refresh_token (String)
- is_active (Boolean)
- created_at, updated_at (DateTime)

**documents**
- id (UUID, PK)
- user_id (UUID, FK)
- file_name, file_path (String)
- file_type (pdf, image, text)
- extracted_text (Text)
- status (pending, extracted, classified)
- created_at, updated_at (DateTime)

**extracted_items**
- id (UUID, PK)
- document_id, user_id (UUID, FK)
- title, description (String/Text)
- item_type (schedule, deadline, todo)
- due_date, due_time (Date/Time)
- location (String)
- priority (1-5)
- status (pending, confirmed, synced)
- google_event_id (String)
- is_completed (Boolean)
- completed_at (DateTime)
- created_at, updated_at (DateTime)

## 🧪 테스트 실행

```bash
# 모든 테스트 실행
pytest

# 특정 파일 테스트
pytest tests/test_auth.py -v

# 커버리지 확인
pytest --cov=app tests/
```

## 🔒 보안

### 인증
- JWT 토큰 기반 인증
- HTTPBearer 스키마
- 토큰 만료 시간: 30분 (설정 가능)

### 패스워드
- bcrypt 해싱

### CORS
- 환경 변수에서 설정 가능한 CORS 화이트리스트

## 🛠️ 다음 단계

### 1단계: 파일 처리 (Week 2)
- [ ] PDF 텍스트 추출 (pdf2image, pytesseract)
- [ ] 이미지 OCR
- [ ] 텍스트 정제 및 전처리

### 2단계: AI 통합 (Week 2)
- [ ] OpenAI API 연동
- [ ] 일정/마감/할 일 자동 분류
- [ ] 신뢰도 점수 계산

### 3단계: Google Calendar (Week 3)
- [ ] OAuth 2.0 인증
- [ ] 이벤트 생성/조회/수정
- [ ] 양방향 동기화

### 4단계: 고급 기능 (Week 4)
- [ ] 배치 처리 (APScheduler)
- [ ] 알림 시스템
- [ ] 완료 피드백

## 📚 참고 자료

- [FastAPI 공식 문서](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://docs.sqlalchemy.org/)
- [Pydantic](https://docs.pydantic.dev/)
- [OpenAI API](https://platform.openai.com/docs/)
- [Google Calendar API](https://developers.google.com/calendar)

## 🤝 기여

이슈나 PR은 언제든 환영합니다!

## 📄 라이선스

MIT License
