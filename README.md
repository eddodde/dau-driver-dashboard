# VIP DAU 성과 동인맵 (dau-driver-dashboard)

VIP DAU를 **재방문 중심 동인 트리**로 분해해서 보여주는 진단·네비 대시보드.
왼쪽(성과지표) → 오른쪽(실행)으로 읽히는 가로 레벨 포맷.

- 역할 분리: **진단/구조 이해 = 이 대시보드**, 운영·실적 추적 = `dau-plan-dashboard`
- 모든 수치는 **전년비·구성비(지수)** 만 사용 → 절대수(실 DAU·수신동의 원수) 미노출

## 구성
- `app.py` — 단일 앱. 모든 값은 `data/*.csv`에서 로드.
- `data/`
  - `nodes.csv` — 동인 트리 노드 (축 / 동인 / 실행레버 / CRM 통제 여부 / 새 실행방안 / 상태색)
  - `kpi.csv` — 월별 MAU·DAU 전년비(%)
  - `channel.csv` — 채널별 DAU 전년비(%) (직접·푸시·광고)
  - `frequency.csv` — 빈도 그룹 구성비(%) 2025 vs 2026
  - `transition.csv` — 방문빈도 전이행렬(%) 2025→2026

## "워싱"은 CSV만 수정
코드는 건드리지 않는다. `data/*.csv` 값만 바꾸면 됨.
- **기준 통일**: DAU 정의가 버전별로 달랐음(과거 ~26,000 vs 최근 ~19,000~21,000).
  하나의 정본 기준으로 뽑은 전년비로 `kpi.csv`·`channel.csv`를 채울 것.
- **마스킹**: 절대수는 넣지 말 것. 전년비/구성비/지수만.
- **상태색**: `nodes.csv`의 `status` = `bad`(빨강)·`warn`(주황)·공란(없음).
- **새 실행방안**: `nodes.csv`의 `new_action` 비우면 `—`로 표시.

## 로컬 실행
```
pip install -r requirements.txt
streamlit run app.py
```

## 배포 (Streamlit Community Cloud)
1. 이 폴더를 GitHub 레포로 push
2. share.streamlit.io → New app → 레포·브랜치·`app.py` 지정 → Deploy

> 데이터가 준비되면 `재방문 트리거` 노드에 파일럿 실측(발송군 vs 홀드아웃)을
> 붙이는 상세 패널을 추가 예정.
