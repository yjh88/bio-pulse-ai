# Bio-Pulse AI (바이오·매크로 뉴스 투자 심리 분석기)

## 1. 서비스 소개
복잡한 제약·바이오 임상 결과, 영문 FDA 공시, 거시경제 뉴스를 입력하면 Gemini AI가 객관적으로 분석하여 **투자 심리(호재/악재/중립)**와 **핵심 요인 3줄 요약**, **리스크 요인**을 도출해 주는 웹 서비스입니다.

* **배포 URL:** ([https://bio-pulse-ai.vercel.app](https://bio-pulse-ai.vercel.app))

## 2. 기술 스택
* **Frontend:** HTML5, CSS3 (반응형 웹 디자인), Vanilla JavaScript (`fetch` API)
* **Backend:** Vercel Serverless Functions (Python 3)
* **AI API:** Google Gemini API (`google-genai`, `gemini-2.5-flash`)
* **Deployment:** GitHub, Vercel

## 3. 프로젝트 구조
```text
bio-pulse-ai/
├── index.html           # 메인 화면 (서비스 소개 / AI 분석기 / 투자 유의사항 3개 섹션)
├── css/
│   └── style.css        # 스타일 및 모바일 반응형 레이아웃
├── js/
│   └── app.js           # 입력값 검증, fetch 요청 및 실패/타임아웃 처리
├── api/
│   └── analyze.py       # Python Serverless Function (Gemini API 호출)
├── requirements.txt     # Python 패키지 의존성 (google-genai)
└── README.md            # 프로젝트 설명서






---

## 6. 서비스 기획서

### 1) 서비스 개요
* **서비스명:** Bio-Pulse AI (바이오·매크로 뉴스 투자 심리 분석기)
* **타겟 사용자:** 제약·바이오 섹터 및 거시 경제 뉴스를 빠르게 파악하고자 하는 개인 투자자
* **서비스 목적:** 복잡한 임상 결과, 영문 FDA 공시, 경제 기사를 AI가 객관적으로 분석하여 투자 심리(호재/악재/중립)와 핵심 요인을 3줄로 요약 제공

### 2) 페이지/섹션 구성 (3개 섹션, 상단 네비게이션 메뉴 이동)
* **서비스 소개 (`#home`):** 서비스 타이틀, 목적 소개 및 분석기 바로가기 버튼
* **AI 뉴스 분석기 (`#analyzer`):** 종목명/키워드 및 뉴스 원문 입력 폼, AI 분석 실행 버튼, 결과 출력 영역
* **투자 유의사항 (`#guide`):** 추천 입력 데이터 안내(FAQ) 및 투자 책임 면책 조항(Disclaimer)

### 3) AI 기능 설계
* **입력:** 관심 종목/키워드(선택) + 뉴스 기사 또는 공시 원문 텍스트(필수)
* **출력:** 투자 심리 판별(호재/악재/중립 및 한 줄 이유) + 핵심 내용 3줄 요약 + 주요 리스크 및 체크포인트
* **실패 처리 기준:**
  * 빈 입력(필수값 누락): `"필수값을 입력하세요: 분석할 뉴스 기사나 공시 원문을 입력해야 합니다."` 안내 문구 표시
  * API/서버 오류(4xx/5xx): `"오류 안내: 서버 오류가 발생했습니다."` 에러 메시지 표시
