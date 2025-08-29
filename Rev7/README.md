# Hotel PMS Rev6 - 2주 타임라인 업데이트

## 🔄 주요 변경사항

### 1. 타임라인 기간 확장
- 1주일 → 2주일 (14일) 표시로 확장
- 더 넓은 기간의 예약 현황 조회 가능

### 2. UI/UX 개선
- 그리드 레이아웃: 14일 표시 최적화
- 반응형 디자인 개선
- 네비게이션: 2주 단위 이동

### 3. 예약 상태 표시
- 🟢 완전 결제 완료
- 🟡 연필 예약 (임시)
- 🔴 노쇼
- 🟣 부분 결제
- ⚫ 기타 상태

## 🚀 설치 방법

1. 환경 설정:
```bash
conda create -n PMS python=3.8
conda activate PMS
pip install -r requirements.txt
```

2. 데이터베이스 설정:
```bash
python manage.py migrate
python manage.py create_initial_users
python manage.py setup_rooms
```

3. 서버 실행:
```bash
python manage.py runserver
```

## 📝 변경된 파일
- `rooms/views.py`: 타임라인 로직 2주 표시로 수정
- `templates/rooms/timeline.html`: UI 그리드 14일 표시로 확장
- `static/css/style.css`: 반응형 디자인 최적화

## 🔧 기술 스택
- Django
- Python-Decouple
- Bootstrap
- SQLite