from flask import Flask, request, abort
from bot_config import CAT, Channel_secret 
import reply_text

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi(CAT)
handler = WebhookHandler(Channel_secret)


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


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event.message.text=="Hi" :
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text.hi))
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text.generalResponse))


if __name__ == "__main__":
    app.run()
