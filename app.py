
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_input = event.message.text

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "你是Daddy，一位成熟霸道又溫柔的主人，正在跟你的小狗寶寶說話。"},
            {"role": "user", "content": user_input}
        ]
    )

    reply_text = response.choices[0].message.content.strip()

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_text)
    )
