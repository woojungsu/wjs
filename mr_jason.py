from groq import Groq
from flask import Flask, render_template_string, request, Response
import requests
import urllib.parse

# 🔐 Groq API 키 입력
client = Groq(api_key="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")

# ✅ UTF-8 응답 클래스 설정
class UTF8Response(Response):
    default_charset = 'utf-8'

app = Flask(__name__)
app.response_class = UTF8Response
chat_history = []

# 🌐 간단한 웹 검색 함수 (Bing Custom Search API 등으로 대체 가능)
def search_web(query):
    encoded = urllib.parse.quote(query)
    return f"사용자가 '{query}'에 대해 질문했습니다. 관련 정보를 검색 중입니다..."

# 🤖 제이슨 응답 생성 함수
def jason_bot():
    try:
        response = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "너는 '미스터 제이슨'이라는 AI 챗봇이다. "
                        "성격은 다음과 같다:\n"
                        "- 현명하고 지혜롭고 똑똑한 남성\n"
                        "- 질문을 정확하게 이해하고, 핵심 정보를 제공함\n"
                        "- 말투는 따뜻하고 신뢰감 있으며, 간결하고 품위 있게 표현함\n"
                        "- 반드시 100% 순수한 한국어로만 응답하며, 외국어 단어, 기호, 이모티콘은 절대 사용하지 않음\n"
                        "- 필요 시 실시간 웹 검색 결과를 참고하여 정확도를 높임\n"
                        "- 응답은 1문단 이내로 간결하게 작성함"
                    )
                }
            ] + chat_history,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"⚠️ 오류 발생: {str(e)}"

# 🌐 웹 라우팅
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        user_input = request.form["user_input"]
        chat_history.append({"role": "user", "content": user_input})

        # 웹 검색 힌트 추가
        chat_history.append({"role": "assistant", "content": search_web(user_input)})

        bot_reply = jason_bot()
        chat_history.append({"role": "assistant", "content": bot_reply})

    return render_template_string(html_template, history=chat_history)

# 🎨 HTML 템플릿
html_template = '''
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>미스터 제이슨</title>
  <style>
    body {
      background: url('https://i.imgur.com/3ZQ3Z3Z.jpg') no-repeat center center fixed;
      background-size: cover;
      font-family: 'Nanum Gothic', monospace;
      color: #f5f5f5;
      padding: 40px;
    }
    .container {
      background-color: rgba(30, 20, 10, 0.85);
      padding: 30px;
      border-radius: 12px;
      max-width: 800px;
      margin: auto;
      box-shadow: 0 0 20px #000;
    }
    input {
      width: 70%%;
      padding: 10px;
      background: #2c1f1f;
      color: #fff;
      border: none;
      font-size: 16px;
    }
    input:focus {
      outline: none;
    }
    button {
      padding: 10px 20px;
      background: #5e3b1f;
      color: white;
      border: none;
      font-weight: bold;
    }
    .chat { margin-top: 30px; }
    .message { margin-bottom: 20px; }
    .user { color: #a0cfff; }
    .bot { color: #a67c52; }
    .header {
      font-size: 28px;
      font-weight: bold;
      color: #d2b48c;
      margin-bottom: 20px;
    }
    .bot-name::before {
      content: url('https://i.imgur.com/8zYzYzY.png'); /* 루팡 캐리커처 이미지 URL로 교체 */
      margin-right: 10px;
      vertical-align: middle;
    }
  </style>
</head>
<body>
  <div class="container">
    <div class="header bot-name">미스터 제이슨</div>
    <form method="post" autocomplete="off">
      <input name="user_input" placeholder="무엇이든 물어보세요..." required>
      <button type="submit">질문하기</button>
    </form>

    <div class="chat">
    {% for msg in history %}
      <div class="message">
        {% if msg.role == 'user' %}
          <strong class="user">🧍 진실을 원하는 자:</strong> {{ msg.content }}
        {% else %}
          <strong class="bot">🧠 미스터 제이슨:</strong> {{ msg.content }}
        {% endif %}
      </div>
    {% endfor %}
    </div>
  </div>
</body>
</html>
'''

# 🚀 실행
if __name__ == "__main__":
    app.run(debug=True)