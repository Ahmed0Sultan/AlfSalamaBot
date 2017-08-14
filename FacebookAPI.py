# encoding=utf8
import requests, json
from flask import url_for


def get_user_fb(token, user_id):
    r = requests.get("https://graph.facebook.com/v2.6/" + user_id,
                     params={"fields": "first_name,last_name,profile_pic,locale,timezone,gender"
                         , "access_token": token
                             })
    if r.status_code != requests.codes.ok:
        print r.text
        return
    user = json.loads(r.content)
    return user


def show_typing(token, user_id, action='typing_on'):
    r = requests.post("https://graph.facebook.com/v2.6/me/messages",
                      params={"access_token": token},
                      data=json.dumps({
                          "recipient": {"id": user_id},
                          "sender_action": action
                      }),
                      headers={'Content-type': 'application/json'})
    if r.status_code != requests.codes.ok:
        print r.text


def send_message(token, user_id, text):
    r = requests.post("https://graph.facebook.com/v2.6/me/messages",
                      params={"access_token": token},
                      data=json.dumps({
                          "recipient": {"id": user_id},
                          "message": {"text": text.decode('utf-8')}
                      }),
                      headers={'Content-type': 'application/json'})
    if r.status_code != requests.codes.ok:
        print r.text


def send_picture(token, user_id, imageUrl, title="", subtitle=""):
    if title != "":
        data = {"recipient": {"id": user_id},
                "message": {
                    "attachment": {
                        "type": "template",
                        "payload": {
                            "template_type": "generic",
                            "elements": [{
                                "title": title,
                                "subtitle": subtitle,
                                "image_url": imageUrl
                            }]
                        }
                    }
                }
                }
    else:
        data = {"recipient": {"id": user_id},
                "message": {
                    "attachment": {
                        "type": "image",
                        "payload": {
                            "url": imageUrl
                        }
                    }
                }
                }
    r = requests.post("https://graph.facebook.com/v2.6/me/messages",
                      params={"access_token": token},
                      data=json.dumps(data),
                      headers={'Content-type': 'application/json'})
    if r.status_code != requests.codes.ok:
        print r.text


def send_url(token, user_id, text, title, url):
    r = requests.post("https://graph.facebook.com/v2.6/me/messages",
                      params={"access_token": token},
                      data=json.dumps({
                          "recipient": {"id": user_id},
                          "message": {
                              "attachment": {
                                  "type": "template",
                                  "payload": {
                                      "template_type": "button",
                                      "text": text,
                                      "buttons": [
                                          {
                                              "type": "web_url",
                                              "url": url,
                                              "title": title
                                          }
                                      ]
                                  }
                              }
                          }
                      }),
                      headers={'Content-type': 'application/json'})
    if r.status_code != requests.codes.ok:
        print r.text


def send_intro_screenshots(token, user_id):
    chat_speak = {
        "title": 'You can both chat and speak to me',
        "image_url": url_for('static', filename="assets/img/intro/1-voice-and-text.jpg", _external=True),
        "subtitle": 'I understand voice and natural language (I try to be smarter everyday :D)'
    }
    location_text = {
        "title": "Find a restaurant/shop for you",
        "image_url": url_for('static', filename="assets/img/intro/2-yelp-gps-location.jpg", _external=True),
        "subtitle": "Tell me what you want, then your location name, address or GPS"
    }
    location_gps = {
        "title": "In case you've never sent location in Messenger",
        "image_url": url_for('static', filename="assets/img/intro/3-how-to-send-location.jpg", _external=True),
        "subtitle": "GPS will be the best option, but just a distinctive name would do",
    }
    location_save = {
        "title": "Save your favorite locations",
        "image_url": url_for('static', filename="assets/img/intro/4-save-location.jpg", _external=True),
        "subtitle": "Make it convenient for you"
    }
    memo1 = {
        "title": "Say \"Memorize\" or \"Memorize this for me\"",
        "image_url": url_for('static', filename="assets/img/intro/5-memo.jpg", _external=True),
        "subtitle": "Then your memo in the same/separate message"
    }
    news = {
        "title": "Keep you updated",
        "image_url": url_for('static', filename="assets/img/intro/6-news.jpg", _external=True),
        "subtitle": "With the most trending news"
    }

    options = [chat_speak, location_text, location_gps, location_save, memo1, news]

    r = requests.post("https://graph.facebook.com/v2.6/me/messages",
                      params={"access_token": token},
                      data=json.dumps({
                          "recipient": {"id": user_id},
                          "message": {
                              "attachment": {
                                  "type": "template",
                                  "payload": {
                                      "template_type": "generic",
                                      "elements": options
                                  }
                              }
                          }
                      }),
                      headers={'Content-type': 'application/json'})
    if r.status_code != requests.codes.ok:
        print r.text


def send_body_quick_replies(token, user_id, intro):
    body_key = 'body_part_'
    quickRepliesOptions = [
        {"content_type": "text",
         "title": "1",
         "payload": body_key + '1'
         },
        {"content_type": "text",
         "title": "2",
         "payload": body_key + '2'
         },
        {"content_type": "text",
         "title": "3",
         "payload": body_key + '3'
         },
        {"content_type": "text",
         "title": "4",
         "payload": body_key + '4'
         },
        {"content_type": "text",
         "title": "5",
         "payload": body_key + '5'
         },
        {"content_type": "text",
         "title": "6",
         "payload": body_key + '6'
         },
        {"content_type": "text",
         "title": "7",
         "payload": body_key + '7'
         },
        {"content_type": "text",
         "title": "8",
         "payload": body_key + '8'
         },
        {"content_type": "text",
         "title": "9",
         "payload": body_key + '9'
         },
        {"content_type": "text",
         "title": "10",
         "payload": body_key + '10'
         }
    ]
    data = json.dumps({
        "recipient": {"id": user_id},
        "message": {
            "text": intro,
            "quick_replies": quickRepliesOptions
        }
    })
    data = data.encode('utf-8')
    r = requests.post("https://graph.facebook.com/v2.6/me/messages",
                      params={"access_token": token},
                      data=data,
                      headers={'Content-type': 'application/json'})

    if r.status_code != requests.codes.ok:
        print r.text


def send_question_answer_quick_replies(token, user_id, intro):
    key = 'Q&A_'

    quickRepliesOptions = [
        {"content_type": "text",
         "title": "yes",
         "payload": key + '1'
         },
        {"content_type": "text",
         "title": "no",
         "payload": key + '0'
         }
    ]
    data = json.dumps({
        "recipient": {"id": user_id},
        "message": {
            "text": intro,
            "quick_replies": quickRepliesOptions
        }
    })
    data = data.encode('utf-8')
    r = requests.post("https://graph.facebook.com/v2.6/me/messages",
                      params={"access_token": token},
                      data=data,
                      headers={'Content-type': 'application/json'})

    if r.status_code != requests.codes.ok:
        print r.text


def set_menu(token):
    r = requests.post("https://graph.facebook.com/v2.6/me/messenger_profile",
                      params={"access_token": token},
                      data=json.dumps({
                          "setting_type": "call_to_actions",
                          "thread_state": "existing_thread",
                          "call_to_actions": [
                              {
                                  "type": "postback",
                                  "title": "الئمة",
                                  "payload": "Akla_Menu"
                              },
                              {
                                  "type": "postback",
                                  "title": "الطلبات",
                                  "payload": "Akla_Orders"
                              },
                              {
                                  "type": "postback",
                                  "title": "حسابي",
                                  "payload": "Akla_Account"
                              }
                          ]
                      }),
                      headers={'Content-type': 'application/json'})
    print r.content
    if r.status_code != requests.codes.ok:
        print r.text


def set_get_started_button(token):
    r = requests.post("https://graph.facebook.com/v2.6/me/thread_settings",
                      params={"access_token": token},
                      data=json.dumps({
                          "setting_type": "call_to_actions",
                          "thread_state": "new_thread",
                          "call_to_actions": [
                              {
                                  "payload": "Get_Started_Button"
                              }
                          ]
                      }),
                      headers={'Content-type': 'application/json'})
    print r.content
    if r.status_code != requests.codes.ok:
        print r.text

        # set_menu()
        # set_get_started_button()
