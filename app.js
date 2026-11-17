document.addEventListener("DOMContentLoaded", () => {
  const analyzeBtn = document.getElementById("analyzeBtn");
  const stockNameInput = document.getElementById("stockName");
  const newsTextInput = document.getElementById("newsText");
  const statusMessage = document.getElementById("statusMessage");
  const resultBox = document.getElementById("resultBox");
  const resultContent = document.getElementById("resultContent");

  function showStatus(message, type) {
    statusMessage.textContent = message;
    statusMessage.className = `status-msg ${type}`;
  }

  function hideStatus() {
    statusMessage.className = "status-msg hidden";
  }

  analyzeBtn.addEventListener("click", async () => {
    const stockName = stockNameInput.value.trim();
    const newsText = newsTextInput.value.trim();

    resultBox.classList.add("hidden");

    // 실패 처리 1: 빈 입력 검증 (필수값 누락 안내)
    if (!newsText) {
      showStatus("필수값을 입력하세요: 분석할 뉴스 기사나 공시 원문을 입력해야 합니다.", "error");
      newsTextInput.focus();
      return;
    }

    // 로딩 상태 표시
    analyzeBtn.disabled = true;
    showStatus("Gemini AI가 뉴스를 분석하고 있습니다. 잠시만 기다려주세요...", "loading");

    // 실패 처리 2: 타임아웃 설정 (15초 지연 시 안내)
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 15000);

    try {
      const response = await fetch("/api/analyze", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          stock: stockName || "미지정 종목/매크로",
          text: newsText
        }),
        signal: controller.signal
      });

      clearTimeout(timeoutId);
      const data = await response.json();

      // 실패 처리 3: API 오류(4xx/5xx) 안내
      if (!response.ok) {
        throw new Error(data.error || `서버 오류가 발생했습니다. (코드: ${response.status})`);
      }

      hideStatus();
      resultContent.textContent = data.result;
      resultBox.classList.remove("hidden");

    } catch (error) {
      if (error.name === "AbortError") {
        showStatus("응답이 지연되어 요청이 취소되었습니다. 잠시 후 다시 시도해주세요.", "error");
      } else {
        showStatus(`오류 안내: ${error.message || "일시적인 네트워크 오류가 발생했습니다."}`, "error");
      }
    } finally {
      analyzeBtn.disabled = false;
    }
  });
});