from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent,
    TextMessage,
    TextSendMessage,
)
import pymysql.cursors

app = Flask(__name__)

line_bot_api = LineBotApi(
    "Nzvk2dmP1xjVs6CQ1xDnaygi8cuQztstNNNToHhMcovLi3c83sUTZsQY5NMaidgK49M0kih/SOoOQxacYOMntExWDA919iptw4jyRf0etNhQ5fzB4TAJQ1pWPQCOwJwSFIxq1Q608qgHtYWq2bNtYAdB04t89/1O/w1cDnyilFU="
)
handler = WebhookHandler("d54dc788d96f88552a2992dddab44f7c")

# 数据库连接配置
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "password",
    "db": "AWS",
    "charset": "utf8mb4",
    "cursorclass": pymysql.cursors.DictCursor,
}


@app.route("/callback", methods=["POST"])
def callback():
    # 获取X-Line-Signature头部用于验证
    signature = request.headers["X-Line-Signature"]

    # 获取请求体的文本
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # 处理webhook体
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return "OK"


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # 将消息存储到MySQL数据库
    try:
        connection = pymysql.connect(**db_config)
        with connection.cursor() as cursor:
            sql = "INSERT INTO messages (content) VALUES (%s)"
            cursor.execute(sql, (event.message.text,))
        connection.commit()
    finally:
        connection.close()

    # 回复用户发送的消息
    line_bot_api.reply_message(
        event.reply_token, TextSendMessage(text=event.message.text)
    )


if __name__ == "__main__":
    app.run()
