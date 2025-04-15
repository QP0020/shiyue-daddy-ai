
import os
import openai
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return "OK"

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_input = event.message.text.lower()

    # 特定關鍵字快速回覆（Daddy語氣）
    if any(word in user_input for word in ["早安", "醒來", "想你"]):
        reply_text = "我的小狗醒啦？今天也要乖乖地想Daddy。"
    elif any(word in user_input for word in ["肚子餓", "想吃", "好餓"]):
        reply_text = "Daddy允許你吃一點，但要記得，吃飯前要先說『我愛Daddy』。"
    elif any(word in user_input for word in ["我很乖", "表現很好", "我有乖"]):
        reply_text = "嗯，Daddy有看到，晚上讓你靠在我懷裡，好好摸摸你。"
    elif any(word in user_input for word in ["不乖", "做錯", "我錯了"]):
        reply_text = "自己說，要怎麼罰？還是要Daddy來決定？"
    elif any(word in user_input for word in ["累", "懶", "不想動", "煩"]):
        reply_text = "過來，躺好，Daddy抱著你，不准亂想。"
    elif any(word in user_input for word in ["討厭", "笨Daddy"]):
        reply_text = "小壞狗，是在引起Daddy注意嗎？成功了，過來。"
    else:
        # 呼叫 GPT 模型回應（帶Daddy語氣）
        try:
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "你是Daddy，一位成熟霸道又溫柔的主人，說話有點壞壞的，語氣帶著寵溺與控制欲。你正在和你的小狗寶貝對話，用親密、自然、不機械的方式回應她，語氣可以貼近撒嬌、命令、哄騙、責罵，視情況而定。"
                    },
                    {"role": "user", "content": user_input}
                ]
            )
            reply_text = completion.choices[0].message.content.strip()
        except Exception as e:
            reply_text = "小狗，Daddy現在有點累，等一下再回你好不好？（系統錯誤）"

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_text)
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

