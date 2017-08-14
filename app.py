# coding=utf8
import os
import sys
import json

import requests
from flask import Flask, request

from FacebookAPI import *
from config import *
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

app = Flask(__name__)

token = get_page_access_token()


@app.route('/', methods=['GET'])
def verify():
    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == get_verify_token():
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "Hello world", 200


@app.route('/', methods=['POST'])
def webhook():
    # endpoint for processing incoming messaging events

    data = request.get_json()
    log(data)  # you may not want to log every incoming message in production, but it's good for testing

    if data.get('object') and data["object"] == "page":

        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:
                sender_id = messaging_event["sender"]["id"]
                recipient_id = messaging_event["recipient"]["id"]

                if messaging_event.get("message"):  # someone sent us a message
                    message_text = messaging_event["message"]["text"]

                    if messaging_event.get("message").get('quick_reply').get('payload'):
                        if messaging_event.get("message").get('quick_reply').get('payload').__contains__('body_part_'):
                            send_message(token, sender_id, 'ddddd')
                            send_question_answer_quick_replies(token, sender_id, 'اختر الاجابة')
                        elif messaging_event.get("message").get('quick_reply').get('payload').__contains__('Q&A_'):
                            num = messaging_event.get("message").get('quick_reply').get('payload').replace('Q&A_', '')
                            send_message(token, sender_id, num)

                            # send_picture(token, sender_id, 'http://flask.pocoo.org/docs/0.12/_static/flask.png', 'image',
                            # 'image')
                            # send_body_quick_replies(token, sender_id, 'choose body part number from picture')
                if messaging_event.get("delivery"):  # delivery confirmation
                    pass

                if messaging_event.get("optin"):  # optin confirmation
                    pass

                if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                    # if messaging_event.get("postback").get('payload').__contains__('body_part_'):
                    #     send_message(token,messaging_event.get("postback").get('payload').replace('body_part_',''))
                    if messaging_event.get("postback").get('payload') == "Get_Started_Button":
                        user = get_user_fb(token, sender_id)
                        msg = u" مرحبا بك يا "
                        send_message(token, sender_id, user.get('first_name') + msg)
                        send_picture(token, sender_id, 'http://flask.pocoo.org/docs/0.12/_static/flask.png', 'image',
                                     'image')
                        send_body_quick_replies(token, sender_id, 'اختر الرقم المقابل للعضو')

    return "ok", 200


def log(message):  # simple wrapper for logging to stdout on heroku
    print str(message)
    sys.stdout.flush()


if __name__ == '__main__':
    app.run(debug=True)
