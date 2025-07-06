from groq import Groq
from flask import Flask, render_template_string, request, Response
import os
import urllib.parse

client = Groq(api_key="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")

class UTF8Response(Response):
    default_charset = 'utf-8'

app = Flask(__name__)
app.response_class = UTF8Response
chat_history = []

# 간단한 검색 문구 삽입 (시뮬레이션용)
def search_web(query):
    encoded = urllib.parse.quote(query)
    return f"“{query}”에 대한 정보를 정리하고 있어요..."

def jason_bot():
    try:
        response = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "너는 '미스터 제이슨'이라는 AI 챗봇이다. "
                        "성격은 지혜롭고 신뢰감 있으며, 현명한 조언을 해주는 따뜻한 남성이다.\n"
                        "반드시 순수한 한국어만 사용하고, 외국어 단어, 특수문자, 이모티콘은 절대 포함하지 않는다.\n"
                        "사용자의 질문에 대해 정확하고 명료하게 답변하며, 품위 있는 어조로 짧은 문단으로 전달한다."
                    )
                }
            ] + chat_history,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"⚠️ 오류: {str(e)}"

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        user_input = request.form["user_input"]
        chat_history.append({"role": "user", "content": user_input})
        chat_history.append({"role": "assistant", "content": search_web(user_input)})
        bot_reply = jason_bot()
        chat_history.append({"role": "assistant", "content": bot_reply})

    return render_template_string(html_template, history=chat_history)

html_template = '''
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>미스터 제이슨</title>
  <style>
    body {
      background: url('https://i.imgur.com/x8KqOgH.jpg') no-repeat center center fixed;
      background-size: cover;
      font-family: 'Nanum Gothic', sans-serif;
      color: #f3f3f3;
      padding: 40px;
    }
    .container {
      background-color: rgba(30, 20, 10, 0.88);
      padding: 30px;
      border-radius: 10px;
      max-width: 800px;
      margin: auto;
      box-shadow: 0 0 20px #000;
    }
    .header {
      font-size: 28px;
      font-weight: bold;
      color: #c49a6c;
      margin-bottom: 20px;
    }
    input {
      width: 70%%;
      padding: 10px;
      background: #2d1f1f;
      color: #fff;
      border: none;
      font-size: 16px;
    }
    input:focus { outline: none; }
    button {
      padding: 10px 20px;
      background: #6d4c41;
      color: white;
      border: none;
      font-weight: bold;
    }
    .chat { margin-top: 30px; }
    .message { margin-bottom: 20px; }
    .user { color: #a0cfff; }
    .bot { color: #c49a6c; }
    .bot::before {
      content: url('https://i.imgur.com/g4x2zxB.png'); /* 루팡 느낌 이미지 넣기 */
      margin-right: 8px;
      vertical-align: middle;
    }
  </style>
</head>
<body>
  <div class="container">
    <div class="header">🕵️ 미스터 제이슨</div>
    <form method="post" autocomplete="off">
      <input name="user_input" placeholder="궁금한 걸 물어보세요..." required>
      <button type="submit">묻기</button>
    </form>
    <div class="chat">
    {% for msg in history %}
      <div class="message">
        {% if msg.role == 'user' %}
          <strong class="user">🔎 진실을 원하는 자:</strong> {{ msg.content }}
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

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)