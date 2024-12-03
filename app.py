# -*- coding: utf-8 -*-

# 載入LineBot所需要的套件
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *

app = Flask(__name__)

# 必須放上自己的Channel Access Token
line_bot_api = LineBotApi('hX3xmKllxDvn9vCe2bKkDKR/P8nXVcuu3/YVwIIbnOQWUHmdDGPPIdaZojMC/9m49/5syhp0/ZZ6any3uWmp+FHblqjhccsg8TdAPB1JCsksON0cRcwcn3tkV/Ednn/V5R5ZWwD5yfV6NI+8mKAwWQdB04t89/1O/w1cDnyilFU=')

# 必須放上自己的Channel Secret
handler = WebhookHandler('4278a1f8dd7606599872d3b45358aab1')

# 發送 Push Message
line_bot_api.push_message(
    'Ue6f400bef64011aedf7f463f05485a7e',
    TextSendMessage(text='您好,目前時間是 2024/10/10 14:00 ，請問需要什麼服務呢?')
)

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

# 訊息傳遞區塊
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text

    if user_message == "天氣":
        reply_message = "請稍等，我幫您查詢天氣資訊！"
    else:
        reply_message = "很抱歉，我目前無法理解這個內容。"

    # 回覆訊息
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_message)
    )

# 主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
