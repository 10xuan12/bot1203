# -*- coding: utf-8 -*-

# 載入LineBot所需要的套件
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *
from datetime import datetime
import pytz
import re
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
tz = pytz.timezone('Asia/Taipei')
current_time = datetime.now(tz).strftime("%Y/%m/%d %H:%M")
line_bot_api.push_message('U6773b925616e46b96db121f79eb2e76d', TextSendMessage(text=f'您好，目前時間是 {current_time} ，請問需要什麼服務呢?'))

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
    elif user_message == "心情好":   # 傳送高興心情的貼圖
        reply_message = StickerSendMessage(package_id='446', sticker_id='1989')  # 開心貼圖
    elif user_message == "心情不好": # 傳送傷心心情的貼圖
        reply_message = StickerSendMessage(package_id='446', sticker_id='2008')  # 哭泣貼圖

    elif user_message == "找美食":  # 傳送餐廳位置
        reply_message = LocationSendMessage(
            title="大頭麵麵",
            address="433台中市沙鹿區北英路119號",
            latitude=24.227595243057735,
            longitude=120.57426516467484
        )
    elif user_message == "找景點":  # 傳送景點位置
        reply_message = LocationSendMessage(
            title="旗津沙灘",
            address="805高雄市旗津區廟前路1號",
            latitude=22.61144200827212,
            longitude=120.26726434891295
        )

    elif user_message == "熱門音樂":  # 傳送熱門音樂音訊
        reply_message = AudioSendMessage(
            original_content_url="https://drive.google.com/uc?export=download&id=1J2MmpK7bb4S-HsHx4yC0YeAuoZQhnOag",  
            duration=203000  # 音訊時長 (毫秒)
        )
    elif user_message == "放鬆音樂":  # 傳送放鬆音樂音訊
        reply_message = AudioSendMessage(
            original_content_url="https://drive.google.com/uc?export=download&id=1LgcJ2bjD8DFakbWY4w6wo8cKyXISuewG",  
            duration=235000  # 音訊時長 (毫秒)
        )
     
    # 新增影片類型處理
    elif user_message == "動作片":
        reply_message = VideoSendMessage(
            original_content_url="https://drive.google.com/uc?export=download&id=1wfWeybmhT9HdX9Ygn1vknu54ia4rPBm5",  # 替換為真實影片連結
            preview_image_url="https://img.pikbest.com/wp/202345/octopus-cartoon-an-image-of-a-swimming-with-large-eyes_9581639.jpg!w700wp"  # 替換為真實預覽圖連結
        )
    elif user_message == "動畫":
        reply_message = VideoSendMessage(
            original_content_url="https://drive.google.com/uc?export=download&id=1JBIfjBjTmVYBwJ3X8JFFZVBpNLwvGs6o",  # 替換為真實影片連結
            preview_image_url="https://pic.616pic.com/ys_bnew_img/00/16/62/0rWVcmU1fK.jpg"  # 替換為真實預覽圖連結
        )
    elif user_message == "紀錄片":
        reply_message = VideoSendMessage(
            original_content_url="https://drive.google.com/uc?export=download&id=1krx3O0rgj7DKTg5pKKRmIFn4xo1Jro5V",  # 替換為真實影片連結
            preview_image_url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTL3K1L1IArBJSNdV7O27-oh-aB6vAylFy3zg&s"  # 替換為真實預覽圖連結
        )

    elif user_message == "今天是我的生日":
        image_message = ImageSendMessage(
            original_content_url="https://img.lovepik.com/free-template/20210106/bg/d4e0b6dd02a87.png_detail.jpg!detail808",
            preview_image_url="https://img.lovepik.com/free-template/20210106/bg/d4e0b6dd02a87.png_detail.jpg!detail808"
        )
        text_message = TextSendMessage(text="生日快樂！希望你有個美好的一天 🎉🎂")
        reply_message = [image_message, text_message]
        
    else:
        reply_message = TextSendMessage(text="抱歉，沒有東西。")

    line_bot_api.reply_message(event.reply_token, reply_message)
# 主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
