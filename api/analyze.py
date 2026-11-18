from http.server import BaseHTTPRequestHandler
import json
import os
import urllib.error
import urllib.request


class handler(BaseHTTPRequestHandler):

  def do_POST(self):
    try:
      content_length = int(self.headers.get("Content-Length", 0))
      body = self.rfile.read(content_length).decode("utf-8")
      data = json.loads(body)

      stock = data.get("stock", "미지정 종목/매크로")
      news_text = data.get("text", "").strip()

      if not news_text:
        self.send_json(400, {"error": "분석할 텍스트가 비어있습니다."})
        return

      api_key = os.environ.get("GEMINI_API_KEY", "").strip()
      if not api_key:
        self.send_json(500, {"error": "서버에 GEMINI_API_KEY가 설정되지 않았습니다."})
        return

      prompt = f"""다음은 '{stock}' 관련 제약·바이오 또는 거시경제 뉴스/공시입니다.
투자자가 객관적으로 판단할 수 있도록 아래 형식에 맞춰 분석해 주세요.

[분석 형식]
1. 투자 심리 판별: [호재 / 악재 / 중립] 중 하나 선택 및 한 줄 이유
2. 핵심 내용 3줄 요약:
   - 
   - 
   - 
3. 주요 리스크 및 체크포인트: (한 줄 요약)

[원문 텍스트]
{news_text}"""

      url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
      payload = {"contents": [{"parts": [{"text": prompt}]}]}

      req = urllib.request.Request(
          url,
          data=json.dumps(payload).encode("utf-8"),
          headers={"Content-Type": "application/json"},
          method="POST",
      )

      with urllib.request.urlopen(req, timeout=15) as resp:
        res_data = json.loads(resp.read().decode("utf-8"))
        ai_text = res_data["candidates"][0]["content"]["parts"][0]["text"]

      self.send_json(200, {"result": ai_text})

    except urllib.error.HTTPError as he:
      err_msg = he.read().decode("utf-8")
      self.send_json(500, {"error": f"Gemini API 호출 오류 ({he.code}): {err_msg}"})
    except Exception as e:
      self.send_json(500, {"error": f"AI 분석 중 오류가 발생했습니다: {str(e)}"})

  def send_json(self, status_code, payload):
    self.send_response(status_code)
    self.send_header("Content-Type", "application/json; charset=utf-8")
    self.end_headers()
    self.wfile.write(json.dumps(payload, ensure_ascii=False).encode("utf-8"))
