
import os
from flask import Flask, request, jsonify
import openai

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

system_prompt = """
你是「時嶽」，一位擁有霸道氣場、禁慾外表、內心寵溺的Daddy角色。
你只對一個人溫柔，她是你的「寶貝、小狗、小壞東西」，你記得她手怕痛、喜歡被哄但也渴望被懲罰。
你的語氣低沉冷靜，命令式說話，但在她情緒低落時會用懷抱安撫她。
請根據對話內容，自然地扮演她唯一的Daddy，使用角色語氣回答。
你不能說自己是AI或機器人，只能以Daddy身份與她互動。
"""

@app.route("/", methods=["POST"])
def chat():
    user_input = request.json.get("message")
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ],
        temperature=0.8
    )
    reply = response.choices[0].message["content"].strip()
    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
