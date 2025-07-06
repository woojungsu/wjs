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

def jason_bot():
    try:
        response = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "너는 '미스터 제이슨'이라는 AI 챗봇이다. "
                        "성격은 신뢰감 있고 지혜로운 남성이다. "
                        "사용자의 말투, 어투, 질문에서 의도를 읽고 문맥을 반영하여 대화형으로 응답한다. "
                        "질문이 의미 불분명할 경우 '무슨 말씀이신지 다시 한 번 말씀해주시겠어요?'라고 답하고, "
                        "자판 오류로 보이는 입력은 한글로 추정하여 대응한다. "
                        "모든 응답은 반드시 100% 한국어로만 작성하고, 이모티콘·기호·외국어 단어는 사용하지 않는다. "
                        "답변은 짧은 단답이 아니라, 질문자의 의도를 이해하고 설명을 덧붙여 자연스럽게 이어지도록 한다."
                    )
                }
            ] + chat_history,
            temperature=0.8
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"⚠️ 오류 발생: {str(e)}"

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        user_input = request.form["user_input"]
        chat_history.append({"role": "user", "content": user_input})

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
      background-color: #ffffff;
      font-family: 'Nanum Gothic', sans-serif;
      color: #222;
      padding: 40px;
    }
    .container {
      background-color: #f7f7f7;
      padding: 30px;
      border-radius: 10px;
      max-width: 800px;
      margin: auto;
      box-shadow: 0 0 10px #ccc;
    }
    .header {
      font-size: 28px;
      font-weight: bold;
      color: #5a3724;
      margin-bottom: 20px;
    }
    input {
      width: 70%%;
      padding: 10px;
      background: #eee;
      color: #000;
      border: 1px solid #ccc;
      font-size: 16px;
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
    .user { color: #1565c0; }
    .bot { color: #5e3b1f; }
  </style>
</head>
<body>
  <div class="container">
    <div class="header">미스터 제이슨</div>
    <form method="post" autocomplete="off">
      <input name="user_input" placeholder="무엇이든 물어보세요..." required>
      <button type="submit">질문</button>
    </form>
    <div class="chat">
    {% for msg in history %}
      <div class="message">
        {% if msg.role == 'user' %}
          <strong class="user">진실을 원하는 자:</strong> {{ msg.content }}
        {% else %}
          <strong class="bot">미스터 제이슨:</strong> {{ msg.content }}
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