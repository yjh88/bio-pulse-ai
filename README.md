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
