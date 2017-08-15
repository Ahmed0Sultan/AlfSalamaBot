# coding=utf8
import datetime
import sys

from sqlalchemy.orm import relation
from sqlalchemy.sql.expression import false

from FacebookAPI import *
from config import *

reload(sys)
sys.setdefaultencoding('utf-8')

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bot.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = false
db = SQLAlchemy(app)

token = get_page_access_token()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    username = db.Column(db.String(), unique=True)
    password = db.Column(db.String())
    email = db.Column(db.String(), unique=True)

    def __init__(self, name, username, password, email):
        self.name = name
        self.username = username
        self.password = password
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.TEXT, nullable=false)
    route = db.Column(db.Boolean,  default=0)
    parent_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    parent = relation('Question', remote_side=[id])
    childs = relation('Question', remote_side=[parent_id])
    created_at = db.Column(db.TIMESTAMP, default=datetime.datetime.utcnow)

    def __init__(self, question, route, parent_id):
        self.question = question
        self.route = route
        self.parent_id = parent_id


db.create_all()


# q = Question.query.filter_by(id=6).first()
# print (len(q.childs))
# exit(0)


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
                            q = Question.query.filter_by(id=message_text).first()
                            send_message(token, sender_id, q.question)
                            send_question_answer_quick_replies(token, sender_id, message_text, 'اختر الاجابة')

                        elif messaging_event.get("message").get('quick_reply').get('payload').__contains__('_Q&A_'):
                            question_id_and_route = messaging_event.get("message").get('quick_reply').get(
                                'payload').replace('_Q&A_', ',')
                            id_route = question_id_and_route.split(',')

                            q = Question.query.filter_by(parent_id=id_route[0], route=id_route[1]).first()
                            if q is not None:
                                send_message(token, sender_id, q.question)
                                if len(q.childs):
                                    send_question_answer_quick_replies(token, sender_id, q.id, 'اختر الاجابة')

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


@app.route('/new-question', methods=['POST'])
def new_question():
    if (request.form.get('question') is not None) and (request.form.get('parent_id') is not None) and (request.form.get(
            'route') is not None):  # route check left or right branch 0 or 1
        q = Question(str(request.form.get('question')), int(request.form.get('route')),
                     int(request.form.get('parent_id')))
        # q.created_at = datetime.datetime.utcnow
        db.session.add(q)
        db.session.commit()
        return "OK", 200

    return "FAILED", 400


def log(message):  # simple wrapper for logging to stdout on heroku
    print str(message)
    sys.stdout.flush()


if __name__ == '__main__':
    app.run(debug=True)
