from http.server import BaseHTTPRequestHandler
import json
import os
from google import genai


class handler(BaseHTTPRequestHandler):

  def do_POST(self):
    try:
      # 1. 프론트엔드에서 보낸 데이터 읽기
      content_length = int(self.headers.get("Content-Length", 0))
      body = self.rfile.read(content_length).decode("utf-8")
      data = json.loads(body)

      stock = data.get("stock", "미지정 종목/매크로")
      news_text = data.get("text", "").strip()

      if not news_text:
        self.send_json(400, {"error": "분석할 텍스트가 비어있습니다."})
        return

      # 2. 환경 변수에서 API 키 가져오기 (보안 규정 준수)
      api_key = os.environ.get("GEMINI_API_KEY")
      if not api_key:
        self.send_json(500, {"error": "서버에 GEMINI_API_KEY가 설정되지 않았습니다."})
        return

      # 3. Gemini AI 호출
      client = genai.Client(api_key=api_key)
      prompt = f"""
            다음은 '{stock}' 관련 제약·바이오 또는 거시경제 뉴스/공시입니다.
            투자자가 객관적으로 판단할 수 있도록 아래 형식에 맞춰 분석해 주세요.

            [분석 형식]
            1. 투자 심리 판별: [호재 / 악재 / 중립] 중 하나 선택 및 한 줄 이유
            2. 핵심 내용 3줄 요약:
               - 
               - 
               - 
            3. 주요 리스크 및 체크포인트: (한 줄 요약)

            [원문 텍스트]
            {news_text}
            """

      response = client.models.generate_content(
          model="gemini-2.5-flash", contents=prompt
      )

      # 4. 정상 결과 반환
      self.send_json(200, {"result": response.text})

    except Exception as e:
      self.send_json(500, {"error": f"AI 분석 중 오류가 발생했습니다: {str(e)}"})

  def send_json(self, status_code, payload):
    self.send_response(status_code)
    self.send_header("Content-Type", "application/json; charset=utf-8")
    self.end_headers()
    self.wfile.write(json.dumps(payload, ensure_ascii=False).encode("utf-8"))