# coding=utf8
import datetime,json
import sys, traceback
from sqlalchemy.orm import relation
from sqlalchemy.sql.expression import false
import FacebookAPI as FB
from config import *
from flask_login import LoginManager
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash

reload(sys)
sys.setdefaultencoding('utf-8')

from flask import Flask, request,render_template,redirect,flash,url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bot.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = false
app.config['SECRET_KEY'] = 'super-secret'
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

token = get_page_access_token()

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    username = db.Column(db.String(), unique=True) #also stores messenger user id
    email = db.Column(db.String(), unique=True)
    password = db.Column(db.String())
    created_at = db.Column(db.TIMESTAMP, default=datetime.datetime.utcnow)

    def __init__(self, name, username, password, email):
        self.name = name
        self.username = username
        if password is not None:
            self.set_password(password)
        self.email = email

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<Admin %r>' % self.username

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    username = db.Column(db.String(), unique=True) #stores messenger user id
    email = db.Column(db.String(), unique=True)
    location = db.Column(db.String())
    phone = db.Column(db.String(), unique=True)
    age = db.Column(db.Integer)
    created_at = db.Column(db.TIMESTAMP, default=datetime.datetime.utcnow)

    health_records = relation('HealthRecord')

    def __init__(self, name, username, email, phone, age,location):
        self.name = name
        self.username = username
        self.email = email
        self.phone = phone
        self.age = age
        self.location = location

class Question(db.Model):
    ROUTE_NO = 0
    ROUTE_YES = 1
    # ROUTE_SYMPTOM = 2 # will use to indicate that this record belongs to symptoms not question

    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.TEXT, nullable=false)
    route = db.Column(db.Integer, default=0)
    parent_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    created_at = db.Column(db.TIMESTAMP, default=datetime.datetime.utcnow)

    parent = relation('Question', remote_side=[id])
    childs = relation('Question', remote_side=[parent_id])

    def __init__(self, question, route, parent_id):
        self.question = question
        self.route = route
        self.parent_id = parent_id


# body parts
class Part(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), unique=True)
    created_at = db.Column(db.TIMESTAMP, default=datetime.datetime.utcnow)

    symptoms = relation('Symptom')

    def __init__(self, name):
        self.name = name


# الاعراض الخاصه بالعضو
class Symptom(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), unique=True)
    part_id = db.Column(db.Integer, db.ForeignKey('part.id'))
    created_at = db.Column(db.TIMESTAMP, default=datetime.datetime.utcnow)

    def __init__(self, name, part_id):
        self.name = name
        self.part_id = part_id


class HealthRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    diagnosis = db.Column(db.Text)
    description = db.Column(db.Text)
    created_at = db.Column(db.TIMESTAMP, default=datetime.datetime.utcnow)

    def __init__(self, user_id, diagnosis, description):
        self.user_id = user_id
        self.diagnosis = diagnosis
        self.description = description


db.create_all()

# admin = User('Admin','admin','admin','admin@admin.com',None,None)
# db.session.add(admin)
# db.session.commit()
# q = Question.query.filter_by(id=1).first()
# print (q.childs)
# exit(0)


@app.route('/', methods=['GET'])
def verify():
    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        print 'Heeeeeeeeeeeeeeeereeeeeeeeeee'
        if not request.args.get("hub.verify_token") == get_verify_token():
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "Hello world", 200


@app.route('/', methods=['POST'])
def handle_messages():
    payload = request.get_data()

    # Handle messages
    for sender_id, message in messaging_events(payload):
        # Start processing valid requests
        try:
            response = processIncoming(sender_id, message)

            if response == 'postback':
                pass


            elif response is not None:
                FB.send_message(token, sender_id, response)

            else:
                FB.send_message(token, sender_id, "Sorry I don't understand that")
        except Exception, e:
            print e
            traceback.print_exc()
    return "ok"

def processIncoming(user_id, message):
    if message['type'] == 'text':
        message_text = message['data']
        message_text = message_text.decode('utf-8','ignore')
        print message_text

        return message_text

    elif message['type'] == 'postback':
        message_payload = message['payload']
        payload_response = payloadProcessing(user_id,message_payload)
        return payload_response

    elif message['type'] == 'quick_reply':
        quick_reply_payload = message['data']
        quick_reply_response = quickReplyProcessing(user_id, quick_reply_payload)
        return quick_reply_response

    elif message['type'] == 'location':
        response = "I've received location (%s,%s) (y)"%(message['data'][0],message['data'][1])
        return response

    elif message['type'] == 'audio':
        audio_url = message['data']
        return "I've received audio %s"%(audio_url)

    # Unrecognizable incoming, remove context and reset all data to start afresh
    else:
        return "*scratch my head*"


def messaging_events(payload):
    data = json.loads(payload)
    messaging_events = data["entry"][0]["messaging"]

    for event in messaging_events:
        sender_id = event["sender"]["id"]

        # Postback Message
        if "postback" in event:
            print event
            yield sender_id, {'type': 'postback', 'payload': event['postback']['payload'], 'message_id': event["sender"]["id"]}


        # Pure text message
        elif "message" in event and "text" in event["message"] and "quick_reply" not in event["message"]:
            data = event["message"]["text"].encode('unicode_escape')
            yield sender_id, {'type': 'text', 'data': data, 'message_id': event['message']['mid']}

        # Message with attachment (location, audio, photo, file, etc)
        elif "attachments" in event["message"]:

            # Location
            if "location" == event['message']['attachments'][0]["type"]:
                coordinates = event['message']['attachments'][
                    0]['payload']['coordinates']
                latitude = coordinates['lat']
                longitude = coordinates['long']

                yield sender_id, {'type': 'location', 'data': [latitude, longitude],
                                  'message_id': event['message']['mid']}

            # Audio
            elif "audio" == event['message']['attachments'][0]["type"]:
                audio_url = event['message'][
                    'attachments'][0]['payload']['url']
                yield sender_id, {'type': 'audio', 'data': audio_url, 'message_id': event['message']['mid']}

            else:
                yield sender_id, {'type': 'text', 'data': "I don't understand this",
                                  'message_id': event['message']['mid']}

        # Quick reply message type
        elif "quick_reply" in event["message"]:
            data = event["message"]["quick_reply"]["payload"]
            yield sender_id, {'type': 'quick_reply', 'data': data, 'message_id': event['message']['mid']}

        else:
            yield sender_id, {'type': 'text', 'data': "I don't understand this", 'message_id': event['message']['mid']}

def payloadProcessing(user_id,message_payload):
    if message_payload == 'Get_Started_Button':
        FBuser = FB.get_user_fb(token, user_id)
        if User.query.filter_by(username=user_id).first() is None:
            user = User(str(FBuser.get('first_name'))+' '+str(FBuser.get('last_name')),user_id,None,None,None,None)
            db.session.add(user)
            db.session.commit()
        msg = u" مرحبا بك يا "
        FB.send_message(token,user_id,FBuser.get('first_name') + msg)
        FB.show_typing(token,user_id,'typing_on')
        intro = u"يمكنك الأن استشارة الف سلامة بوت و ادخال الأعراض التى تشعر بها لتعرف حالتك و تطمئن على صحتك فى اسرع وقت"
        FB.send_message(token, user_id,intro)
        FB.show_typing(token, user_id, 'typing_on')
        intro = u"يبدو انك لم تستكمل بياناتك بعد، من فضلك استكملها لتساعدنا على تقديم افضل خدمة لك"
        FB.send_complete_data_button(token, user_id, intro,True)
    elif message_payload.__contains__('_Q&A_'):
        question_id_and_route = message_payload.split('_Q&A_')
        # if question_id_and_route[0] == '':
        q = Question.query.filter_by(parent_id=None).filter_by(route=int(question_id_and_route[1])).first()
        if q is not None:
            if len(q.childs) == 2:
                FB.show_typing(token, user_id, 'typing_on')
                FB.send_question_answer_quick_replies(token, user_id, q.id, q.question,2)
            elif len(q.childs) == 1:
                FB.show_typing(token, user_id, 'typing_on')
                FB.send_question_answer_quick_replies(token, user_id, q.id, q.question,q.childs[0].route)
            else:
                FB.send_message(token, user_id, q.question)
        # else:
        #     q = Question.query.filter_by(parent_id=question_id_and_route[0]).filter_by(route=int(question_id_and_route[1])).first()
        #     if q is not None:
        #         FB.show_typing(token, user_id, 'typing_on')
        #         FB.send_question_answer_quick_replies(token, user_id, q.id, q.question)

    elif message_payload == 'Complete_Data':
        print 'من فضلك اختر شيئاً من القائمة'
        return 'من فضلك اختر شيئاً من القائمة'

    return 'postback'

def quickReplyProcessing(user_id,quick_reply_payload):

    if quick_reply_payload == 'Complete_Person_Data_Request':
        FB.show_typing(token, user_id, 'typing_on')
        intro = u"من فضلك ادخل بيانات هذا الشخص لتساعدنا على تقديم افضل خدمة"
        FB.send_complete_data_button(token, user_id, intro,False)
        FB.send_whose_diagnoses(token,user_id,u"من فضلك اختر الى اين تريد الذهاب")
    elif quick_reply_payload == "Choose_Who_To_Diagnose":
        FB.show_typing(token, user_id, 'typing_on')
        FB.send_body_quick_replies(token, user_id, u"هل هذا التشخيص لك ام لشخص اخر ؟")
    elif quick_reply_payload == "Show_Parts":
        FB.show_typing(token, user_id, 'typing_on')
        FB.send_picture(token,user_id,url_for('static', filename="assets/img/parts_1.png", _external=True))
        FB.show_typing(token, user_id, 'typing_on')
        FB.send_body_quick_replies(token, user_id, u"من فضلك اختر رقم العضو الذى تشكو منه")
    elif quick_reply_payload.__contains__('body_part_'):
        body_part = int(quick_reply_payload.replace('body_part_',''))
        symptoms = Symptom.query.filter_by(part_id=body_part).all()
        symptoms_list = []
        for s in symptoms:
            symptoms_list.append({
                "title": s.name,
                "buttons": [
                    {
                        "type": "postback",
                        "title": 'اظهر المزيد',
                        "payload": '_Q&A_'+str(s.id)
                    }
                ]
            })
        FB.show_typing(token, user_id, 'typing_on')
        FB.send_symptoms(token, user_id, symptoms_list)

    elif quick_reply_payload.__contains__('_Q&A_'):
        question_id_and_route = quick_reply_payload.split('_Q&A_')
        # if question_id_and_route[0] == '':
        #     q = Question.query.filter_by(parent_id=None).filter_by(route=int(question_id_and_route[1])).first()
        #     if q is not None:
        #         if len(q.childs) == 2:
        #             FB.show_typing(token, user_id, 'typing_on')
        #             FB.send_question_answer_quick_replies(token, user_id, q.id, q.question,2)
        #         elif len(q.childs) == 1:
        #             FB.show_typing(token, user_id, 'typing_on')
        #             FB.send_question_answer_quick_replies(token, user_id, q.id, q.question,q.childs[0].route)
        #         else:
        #             FB.send_message(token, user_id, q.question)
        # else:
        q = Question.query.filter_by(parent_id=question_id_and_route[0]).filter_by(route=int(question_id_and_route[1])).first()
        if q is not None:
            if len(q.childs) == 2:
                FB.show_typing(token, user_id, 'typing_on')
                FB.send_question_answer_quick_replies(token, user_id, q.id, q.question,2)
            elif len(q.childs) == 1:
                FB.show_typing(token, user_id, 'typing_on')
                FB.send_question_answer_quick_replies(token, user_id, q.id, q.question,q.childs[0].route)
            else:
                FB.send_message(token, user_id, q.question)

    return 'postback'


@app.route('/new-question', methods=['POST','GET'])
@login_required
def new_question():
    if request.method == 'POST':
        question = Question(request.form['question'],request.form['select-symptom'],None)
        db.session.add(question)
        db.session.commit()
        # return render_template('flowchart.html', question=question)
        url = 'flowcharts/'+ str(question.id)
        return redirect(url)
    elif request.method == 'GET':
        symptoms_parts = []
        symptoms = Symptom.query.all()
        for symptom in symptoms:
            id = symptom.id
            part = Part.query.filter_by(id = symptom.part_id).first()
            symptoms_parts.append([id,symptom.name + ' ( '+ part.name + ' )'])
        return render_template('add-question.html',symptoms_parts = symptoms_parts)
    return "FAILED", 400

@app.route('/new-body-part', methods=['POST','GET'])
@login_required
def new_body_part():
    if request.method == 'POST':
        name = request.form['body-part']
        part = Part(name)
        db.session.add(part)
        db.session.commit()
        return render_template('new-body-part.html')
    elif request.method == 'GET':
        return render_template('new-body-part.html')
    return "FAILED", 400

@app.route('/new-symptom', methods=['POST','GET'])
@login_required
def new_symptom():
    if request.method == 'POST':
        part_id = request.form['select-symptom']
        name = request.form['symptom']
        symptom = Symptom(name,part_id)
        db.session.add(symptom)
        db.session.commit()
        parts = Part.query.all()
        return render_template('new-symptom.html',parts = parts)
    elif request.method == 'GET':
        parts = Part.query.all()
        return render_template('new-symptom.html',parts = parts)
    return "FAILED", 400

@app.route('/flowcharts/<question_id>', methods=['GET', 'POST'])
@login_required
def flowchart(question_id):
    if request.method == 'GET':
        question = Question.query.filter_by(id = question_id).first()
        if question.parent_id == None:
            return render_template('flowchart.html',question=question)
        else:
            return 'Not Available'
    elif request.method == 'POST':
        print request.json
        question = Question(request.json['question'],request.json['route'],request.json['parentID'])
        db.session.add(question)
        db.session.commit()
        question = Question.query.filter_by(id=question_id).first()
        return render_template('flowchart.html', question=question)


@app.route('/flowcharts', methods=['GET', 'POST'])
@login_required
def flowcharts():
    if request.method == 'GET':
        items = []
        questions = Question.query.filter_by(parent_id = None).all()
        for question in questions:
            symptom = Symptom.query.filter_by(id=question.route).first()
            part = Part.query.filter_by(id=symptom.part_id).first()
            items.append({'Q_id':question.id,'Q_name':question.question,'S_name':symptom.name,'P_name':part.name})
        return render_template('flowcharts.html',items=items)

@app.route('/complete-data/<user_id>', methods=['GET', 'POST'])
def completeData(user_id):
    if request.method == 'GET':
        MyData = request.args['mine']
        print MyData
        if MyData == 'True':
            user = User.query.filter_by(username=user_id).first()
            return render_template('complete-data.html',user_id=user_id,name=user.name)
        elif MyData == 'False':
            return render_template('complete-data.html', user_id=None, name=None)
    elif request.method == 'POST':
        if request.form['id'] is not None:
            user = User.query.filter_by(username=request.form['id']).first()
            user.name = request.form['name']
            user_exist = User.query.filter_by(email=request.form['email']).first()
            if user_exist is not None and user_exist.username is not None:
                flash(u'هذا البريد الالكتروني تم استخدامه من قبل!!', 'error')
                return redirect(url_for('completeData'))
            elif user_exist is not None and user_exist.username is None:
                if user_exist.phone != request.form['phone']:
                    flash(u'هذا البريد الالكتروني تم استخدامه من قبل!!', 'error')
                    flash(u'هذا الرقم تم استخدامه من قبل!!', 'error')
                    return redirect(url_for('completeData'))
                elif user_exist.phone == request.form['phone']:
                    user.name = request.form['name']
                    user.email = request.form['email']
                    user.phone = request.form['phone']
                    user.age = request.form['age']
                    user.location = request.form['location']
                    db.session.delete(user_exist)
                    db.session.commit()
            user.email = request.form['email']
            user_exist = User.query.filter_by(phone=request.form['phone']).first()
            if user_exist is not None:
                flash(u'هذا الرقم تم استخدامه من قبل!!', 'error')
                return redirect(url_for('completeData'))
            user.phone = request.form['phone']
            user.age = request.form['age']
            user.location = request.form['location']
            db.session.commit()
            FB.show_typing(token, user_id, 'typing_on')
            FB.send_message(token,request.form['id'],u"تم تسجيل بياناتك بنجاح")
            FB.show_typing(token, user_id, 'typing_on')
            FB.send_where_to_go_quick_replies(token,request.form['id'],u"من فضلك اختر الى اين تريد الذهاب")
            return render_template('complete-data.html')
        elif request.form['id'] is None:
            user_exist = User.query.filter_by(email=request.form['email']).first()
            if user_exist is not None:
                flash(u'هذا البريد الالكتروني تم استخدامه من قبل!!', 'error')
                return redirect(url_for('completeData'))
            user_exist = User.query.filter_by(phone=request.form['phone']).first()
            if user_exist is not None:
                flash(u'هذا الرقم تم استخدامه من قبل!!', 'error')
                return redirect(url_for('completeData'))
            user = User(request.form['name'],None,request.form['email'],request.form['phone'],request.form['age'],request.form['location'])
            db.session.add(user)
            db.session.commit()

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('new_question'))
    if request.method == 'GET':
        return render_template('login.html')

    email = request.form['email']
    password = request.form['password']
    registered_user = Admin.query.filter_by(email=email).first()
    if registered_user is None:
        flash('Email is invalid', 'error')
        return redirect(url_for('login'))
    if not registered_user.check_password(password):
        flash('Password is invalid', 'error')
        return redirect(url_for('login'))
    login_user(registered_user)
    flash('Logged in successfully')
    return redirect(url_for('new_question'))

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

def log(message):  # simple wrapper for logging to stdout on heroku
    print str(message)
    sys.stdout.flush()


if __name__ == '__main__':
    app.run(debug=True)
