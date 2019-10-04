from flask import Flask, request, abort
from bot_config import CAT, Channel_secret 
import reply_text
import json 
from getDetectionBot import getDetectionBot 
import threading
import time
import multiprocessing as mp
import subprocess 


from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, FollowEvent
)

detection_result = {}
app = Flask(__name__)
line_bot_api = LineBotApi(CAT)
handler = WebhookHandler(Channel_secret)
register = set()
jsonFileName = 'detectionResult.json'
 
def pushMessage():
    def parseResult():
        with open(jsonFileName) as json_file:
            result = json.load(json_file)
            global detection_result
            detection_result = result 
        return result
    while True: 
        dets = parseResult()
        detsCnt = len(dets)
        registerCnt = len(register)
        if registerCnt == 0 or detsCnt == 0:
            continue
        for usr in register:
            line_bot_api.push_message(usr,TextSendMessage(text="偵測到{}個站立".format(detsCnt)))
#        time.sleep(1)

def pushMessageLocal():
    bot = getDetectionBot() 
    while True: 
        dets = bot.getDetectionLocal()
        detsCnt = len(dets)
        registerCnt = len(register)
        if registerCnt == 0 or detsCnt == 0:
            continue
        for usr in register:
            line_bot_api.push_message(usr,TextSendMessage(text="偵測到{}個站立".format(detsCnt)))
#

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

@app.route("/hello",methods=['GET'])
def hello():
    return "Hello, line chatbot"

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    #print(event.source.user_id)
    #line_bot_api.reply_message(event.reply_token, TextSendMessage(text="ABC"))
    text2reply = []
    msg = event.message.text 
    if "開啟" in msg:
        text2reply.append(TextSendMessage(text="功能已啟用"))
        register.add(event.source.user_id)
    elif "停止" in msg:
        text2reply.append(TextSendMessage(text="功能已關閉"))
        register.remove(event.source.user_id)
    
    elif msg == "Hi" or msg == "hi":
        text2reply.append(TextSendMessage(text=reply_text.Hi))
    elif msg == "介紹":
        text2reply.append(TextSendMessage(reply_text.helpMessage))
    elif "笑話" in msg or "joke" in msg:
        text2reply.append(TextSendMessage(reply_text.joke))
    else:
        text2reply.append(TextSendMessage(text=reply_text.generalResponse))
        text2reply.append(TextSendMessage(reply_text.intro))
    

    line_bot_api.reply_message(event.reply_token, messages=text2reply)
    #line_bot_api.push_message("Ucd82fda579561396b75c340fe72e1342",TextSendMessage(text="安安"))
    #line_bot_api.push_message("U253c8bf25a08de15f97f7c47472ea840",TextSendMessage(text="安安"))

@handler.add(FollowEvent)
def handle_follow(event):
    text2reply = []
    app.logger.info("Got Follow Event:" + event.source.user_id)
    text2reply.append(TextSendMessage(reply_text.greeting))
    text2reply.append(TextSendMessage(reply_text.intro))
    line_bot_api.reply_message(event.reply_token,messages=text2reply)

if __name__ == "__main__":
    jsonFileName = 'detectionResult.json'
#    detBot = getDetectionBot.getDetectionBot()
#    det_thread = mp.Process(target=detBot.getDetections,args=(jsonFileName,))
#    det_thread.start()
#    push_process = mp.Process(target=pushMessage)
#    push_process.start()
    push_thread = threading.Thread(target=pushMessageLocal)
    push_thread.start()
    #app_thread = threading.Thread(target=app.run)
    #app_thread.start()
    app.run()
