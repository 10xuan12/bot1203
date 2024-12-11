# -*- coding: utf-8 -*-

#載入LineBot所需要的套件
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import re
app = Flask(__name__)

# 必須放上自己的Channel Access Token
line_bot_api = LineBotApi('i56ndfznsDmPtyX20QVZR2QM9AfQJlI6rToNzoO3QH8UtjR/wBCCC003l/gkRtlOJZ/nRDxAXruKvL6cJZ3GD+Rp2XIGIPftgSYMXdeHI1eXFTQO+/G/UGJf8VeFcomwi3YXcCGMiVlwMkSFYbntZgdB04t89/1O/w1cDnyilFU=')
# 必須放上自己的Channel Secret
handler = WebhookHandler('9a14d6af945fb5f5a96c6077e699440b')

line_bot_api.push_message('Ue6f400bef64011aedf7f463f05485a7e', TextSendMessage(text='你可以開始了'))

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

#訊息傳遞區塊
##### 基本上程式編輯都在這個function #####
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = event.message.text.strip()  # 去掉多餘空格

    # 推薦餐廳功能
    if message == "推薦餐廳":
        imagemap_message = ImagemapSendMessage(
            base_url='https://i.imgur.com/AjSt5jd.jpeg',
            alt_text='組圖訊息',
            base_size=BaseSize(height=1040, width=1040),
            actions=[
                URIImagemapAction(
                    link_uri='https://www.facebook.com/2017Ninja.Sushi/',  # 日料左上
                    area=ImagemapArea(x=0, y=0, width=700, height=700)
                ),
                URIImagemapAction(
                    link_uri='http://www.facebook.com/PUROtaverna',  # 西式右上
                    area=ImagemapArea(x=700, y=0, width=700, height=700)
                ),
                URIImagemapAction(
                    link_uri='https://www.facebook.com/yangsbeefnoodle/',  # 中式左下
                    area=ImagemapArea(x=0, y=700, width=700, height=700)
                ),
                URIImagemapAction(
                    link_uri='https://www.windsortaiwan.com/tw/food/2C25b1caC2E19A4c',  # 法式右下
                    area=ImagemapArea(x=700, y=700, width=700, height=700)
                )
            ]
        )
        line_bot_api.reply_message(event.reply_token, imagemap_message)

    # 推薦景點功能
    elif message == "推薦景點":
        try:
            carousel_template_message = TemplateSendMessage(
                alt_text='熱門旅行景點',
                template=CarouselTemplate(
                    columns=[
                        CarouselColumn(
                            thumbnail_image_url='https://www.pu.edu.tw/var/file/0/1000/pictures/776/m/mczh-tw700x700_large6550_164839763256.jpg',  # 確保 URL 可用
                            title='靜宜大學',
                            text='台灣的私立大學。',
                            actions=[
                                URIAction(
                                    label='查看詳細資訊',
                                    uri='https://www.pu.edu.tw/'
                                ),
                                URIAction(
                                    label='導航至此',
                                    uri='https://maps.app.goo.gl/FbxQvA9vXXoiVXbJ6'
                                )
                            ]
                        ),
                        CarouselColumn(
                            thumbnail_image_url='https://i.imgur.com/GBPcUEP.png',  # 確保 URL 可用
                            title='台北101',
                            text='台灣最高的摩天大樓。',
                            actions=[
                                URIAction(
                                    label='查看詳細資訊',
                                    uri='https://zh.wikipedia.org/wiki/%E5%8F%B0%E5%8C%97%E5%8D%81%E4%B8%80'
                                ),
                                URIAction(
                                    label='導航至此',
                                    uri='https://www.google.com/maps?q=台北101'
                                )
                            ]
                        ),
                        CarouselColumn(
                            thumbnail_image_url='https://i.imgur.com/kRW5zTO.png',  # 確保 URL 可用
                            title='首爾塔',
                            text='首爾的標誌性建築物。',
                            actions=[
                                URIAction(
                                    label='查看詳細資訊',
                                    uri='https://zh.wikipedia.org/wiki/%E9%87%91%E9%96%A3%E5%AF%BA'
                                ),
                                URIAction(
                                    label='導航至此',
                                    uri='https://www.google.com/maps?q=首爾塔'
                                )
                            ]
                        )
                    ]
                )
            )
            line_bot_api.reply_message(event.reply_token, carousel_template_message)
        except Exception as e:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=f"推薦景點功能發生錯誤：{str(e)}"))

    # 我要訂餐功能
    elif message == "我要訂餐":
        try:
            confirm_template = TemplateSendMessage(
                alt_text='訂餐確認',
                template=ConfirmTemplate(
                    text='肉醬義大利麵 * 1 ，總價NT380',
                    actions=[
                        MessageAction(
                            label='確定',
                            text='訂單已確認，謝謝您的購買！'
                        ),
                        MessageAction(
                            label='取消',
                            text='已取消訂單，謝謝您的光臨！'
                        )
                    ]
                )
            )
            line_bot_api.reply_message(event.reply_token, confirm_template)
        except Exception as e:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=f"訂餐功能發生錯誤：{str(e)}"))

    # 我想吃飯功能
    elif message == "我想吃飯":
        try:
            quick_reply_buttons = TextSendMessage(
                text='請選擇您想加入購物車的品項：',
                quick_reply=QuickReply(
                    items=[
                        QuickReplyButton(
                            action=MessageAction(label="主菜", text="您已成功將【主菜】加入購物車")
                        ),
                        QuickReplyButton(
                            action=MessageAction(label="湯品", text="您已成功將【湯品】加入購物車")
                        ),
                        QuickReplyButton(
                            action=MessageAction(label="飲料", text="您已成功將【飲料】加入購物車")
                        )
                    ]
                )
            )
            line_bot_api.reply_message(event.reply_token, quick_reply_buttons)
        except Exception as e:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=f"功能發生錯誤：{str(e)}"))

    # 電影推薦功能
    elif message == "電影推薦":
        try:
            image_carousel_template = TemplateSendMessage(
                alt_text='電影推薦',
                template=ImageCarouselTemplate(
                    columns=[
                        ImageCarouselColumn(
                            image_url='https://hips.hearstapps.com/hmg-prod/images/obb-22-02418-66e7cf4573fbb.jpg?crop=1xw:1xh;center,top&resize=980:*',  # 確保 URL 可用
                            action=URIAction(
                                label='查看詳細資訊',
                                uri='https://zh.wikipedia.org/zh-tw/%E9%BB%91%E5%B8%A6%E5%87%BA%E5%8B%A4%E4%B8%AD'  # 例如《黑帶出勤中》
                            )
                        ),
                        ImageCarouselColumn(
                            image_url='https://hips.hearstapps.com/hmg-prod/images/mv5bnjrinjk3nzmtowrkms00owqyltljnzmtmzk0ntflmtiwzgvjxkeyxkfqcgdeqxvynty0mdc5oaatat-v1-65aa088df0fad.jpg?crop=1xw:1xh;center,top&resize=980:*',  # 確保 URL 可用
                            action=URIAction(
                                label='查看詳細資訊',
                                uri='https://zh.wikipedia.org/zh-tw/%E9%9D%9E%E5%B8%B8%E5%AE%B6%E5%8B%99%E4%BA%8B'  # 例如《非常家務事》
                            )
                        ),
                        ImageCarouselColumn(
                            image_url='https://upload.wikimedia.org/wikipedia/zh/7/7f/Inception_ver3.jpg',  # 確保 URL 可用
                            action=URIAction(
                                label='查看詳細資訊',
                                uri='https://www.imdb.com/title/tt1375666/'  # 例如《全面啟動》
                            )
                        ),
                        ImageCarouselColumn(
                            image_url='https://upload.wikimedia.org/wikipedia/zh/a/ad/Forrestgumppost.jpg',  # 確保 URL 可用
                            action=URIAction(
                                label='查看詳細資訊',
                                uri='https://www.imdb.com/title/tt0109830/'  # 例如《阿甘正傳》
                            )
                        )
                    ]
                )
            )
            line_bot_api.reply_message(event.reply_token, image_carousel_template)
        except Exception as e:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=f"電影推薦功能發生錯誤：{str(e)}"))
    # 餐廳菜單推薦系統
    elif message == "查看菜單":
        try:
            flex_message = FlexSendMessage(
                alt_text="餐廳菜單",
                contents={
                    "type": "carousel",
                    "contents": [
                        {
                            "type": "bubble",
                            "hero": {
                                "type": "image",
                                "url": "data:image/jpeg;base64,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",
                                "size": "full",
                                "aspectRatio": "20:13",
                                "aspectMode": "cover"
                            },
                            "body": {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "海鮮義大利麵",
                                        "weight": "bold",
                                        "size": "xl"
                                    },
                                    {
                                        "type": "text",
                                        "text": "搭配特製醬汁的義大利麵",
                                        "size": "sm",
                                        "wrap": True
                                    },
                                    {
                                        "type": "text",
                                        "text": "價格: NT$480",
                                        "size": "sm",
                                        "color": "#555555"
                                    }
                                ]
                            },
                            "footer": {
                                "type": "box",
                                "layout": "vertical",
                                "spacing": "sm",
                                "contents": [
                                    {
                                        "type": "button",
                                        "style": "primary",
                                        "action": {
                                            "type": "message",
                                            "label": "訂購",
                                            "text": "已加入購物車: 海鮮義大利麵"
                                        }
                                    }
                                ]
                            }
                        },
                        {
                            "type": "bubble",
                            "hero": {
                                "type": "image",
                                "url": "https://i0.wp.com/foodlifen9.com/wp-content/uploads/2023/08/%E5%BE%B7%E5%9C%8B%E8%B1%AC%E8%85%B3-scaled.jpg?ssl=1",
                                "size": "full",
                                "aspectRatio": "20:13",
                                "aspectMode": "cover"
                            },
                            "body": {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "德國豬腳",
                                        "weight": "bold",
                                        "size": "xl"
                                    },
                                    {
                                        "type": "text",
                                        "text": "超級酥脆",
                                        "size": "sm",
                                        "wrap": True
                                    },
                                    {
                                        "type": "text",
                                        "text": "價格: NT$800",
                                        "size": "sm",
                                        "color": "#555555"
                                    }
                                ]
                            },
                            "footer": {
                                "type": "box",
                                "layout": "vertical",
                                "spacing": "sm",
                                "contents": [
                                    {
                                        "type": "button",
                                        "style": "primary",
                                        "action": {
                                            "type": "message",
                                            "label": "訂購",
                                            "text": "已加入購物車: 德國豬腳"
                                        }
                                    }
                                ]
                            }
                        },
                        {
                            "type": "bubble",
                            "hero": {
                                "type": "image",
                                "url": "https://tokyo-kitchen.icook.network/uploads/recipe/cover/187573/c30dbbec0b6d6ba0.jpg",
                                "size": "full",
                                "aspectRatio": "20:13",
                                "aspectMode": "cover"
                            },
                            "body": {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "巧克力熔岩蛋糕",
                                        "weight": "bold",
                                        "size": "xl"
                                    },
                                    {
                                        "type": "text",
                                        "text": "熱熱的吃最好吃",
                                        "size": "sm",
                                        "wrap": True
                                    },
                                    {
                                        "type": "text",
                                        "text": "價格: NT$250",
                                        "size": "sm",
                                        "color": "#555555"
                                    }
                                ]
                            },
                            "footer": {
                                "type": "box",
                                "layout": "vertical",
                                "spacing": "sm",
                                "contents": [
                                    {
                                        "type": "button",
                                        "style": "primary",
                                        "action": {
                                            "type": "message",
                                            "label": "訂購",
                                            "text": "已加入購物車: 巧克力熔岩蛋糕"
                                        }
                                    }
                                ]
                            }
                        }
                    ]
                }
            )
            line_bot_api.reply_message(event.reply_token, flex_message)
        except Exception as e:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=f"菜單推薦功能發生錯誤：{str(e)}"))
   
    # 未知指令處理
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="無法識別的指令"))
       
#主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
