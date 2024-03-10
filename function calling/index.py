from flask import Flask, request, json
from openai import OpenAI
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # 启用CORS

# 你的OpenAI API密钥
api_key = "sk-w8d5xkXYAplWbFGWtaIWjOaticX6qnNIeToGxlLtJcfGXU2f"
base_url = "https://api.fe8.cn/v1"
systemRole = "用中文回答问题"


@app.route('/chat', methods=['POST'])
def chat():
    # 从请求中获取用户输入的消息
    data = request.json
    # 最近十条的历史消息
    messages = data.get('history', [])
    # 创建一个空字符串用于存储转换后的聊天内容
    chat_content = ""

    # 遍历列表，构建聊天内容字符串
    for item in messages:
        user = item['user']
        text = item['text']
        # 使用字符串格式化构建每条消息
        chat_line = f'{user}：{text}\n'
        chat_content += chat_line


    client = OpenAI(
        api_key="sk-w8d5xkXYAplWbFGWtaIWjOaticX6qnNIeToGxlLtJcfGXU2f",
        base_url="https://api.fe8.cn/v1"
    )

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": systemRole,
            },
            {
                "role": "user",
                "content": chat_content,
            }
        ],
        model="gpt-3.5-turbo",
    )

    # 返回AI的回复
    return chat_completion.choices[0].message.content, 200


if __name__ == '__main__':
    app.run(debug=True)
