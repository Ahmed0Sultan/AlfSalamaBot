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

def send_complete_data_button(token, user_id, intro,MyData= True):
    data = {"recipient": {"id": user_id},
            "message": {
                "attachment": {
                    "type": "template",
                    "payload": {
                        "template_type": "button",
                        "text": intro,
                        "buttons":[{
                            "type":"web_url",
                            "url":"https://alfsalama.herokuapp.com/complete-data/"+str(user_id) + "?mine="+ str(MyData),
                            "title": u"استكمال البيانات"
                          }]
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

def send_body_parts(token, user_id,parts):
    print parts[0]['buttons']
    r = requests.post("https://graph.facebook.com/v2.6/me/messages",
                      params={"access_token": token},
                      data=json.dumps({
                          "recipient": {"id": user_id},
                          "message": {
                              "attachment": {
                                  "type": "template",
                                  "payload": {
                                      "template_type": "generic",
                                      "elements": parts
                                  }
                              }
                          }
                      }),
                      headers={'Content-type': 'application/json'})
    if r.status_code != requests.codes.ok:
        print r.text
def send_test_generic(token, user_id):
    r = requests.post("https://graph.facebook.com/v2.6/me/messages",
                      params={"access_token": token},
                      data=json.dumps({
                          "recipient": {"id": user_id},
                          "message":{
                            "attachment":{
                              "type":"template",
                              "payload":{
                                "template_type":"generic",
                                "elements":[
                                   {
                                    "title":"Welcome to Peter\'s Hats",
                                    "image_url":"https://petersfancybrownhats.com/company_image.png",
                                    "subtitle":"We\'ve got the right hat for everyone.",

                                    "buttons":[
                                      {
                                        "type":"web_url",
                                        "url":"https://petersfancybrownhats.com",
                                        "title":"View Website"
                                      },{
                                        "type":"postback",
                                        "title":"Start Chatting",
                                        "payload":"DEVELOPER_DEFINED_PAYLOAD"
                                      }
                                    ]
                                  }
                                ]
                              }
                            }
                          }
                      }),
                      headers={'Content-type': 'application/json'})
    if r.status_code != requests.codes.ok:
        print r.text

def send_body_parts_test(token, user_id,parts):
    # print parts[0]['buttons']
    r = requests.post("https://graph.facebook.com/v2.6/me/messages",
                      params={"access_token": token},
                      data=json.dumps({
                            "recipient": {"id": user_id},
                            "message": {
                                "text": 'test',
                                "quick_replies": parts
                            }
                      }),
                      headers={'Content-type': 'application/json'})
    if r.status_code != requests.codes.ok:
        print r.text

def send_more_body_parts_quick_replies(token, user_id, intro,list_number):
    quickRepliesOptions = [
        {"content_type": "text",
         "title": "المزيد",
         "payload": 'Show_Parts_' + str(list_number)
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


def send_question_answer_quick_replies(token, user_id, question_id, intro,route):
    key = '_Q&A_'
    if route == 2 :
        quickRepliesOptions = [
            {"content_type": "text",
             "title": u"نعم",
             "payload": str(question_id) + key + '1'
             },
            {"content_type": "text",
             "title": u"لا",
             "payload": str(question_id) + key + '0'
             }
        ]
    elif route == 1:
        quickRepliesOptions = [
            {"content_type": "text",
             "title": u"نعم",
             "payload": str(question_id) + key + '1'
             }
        ]
    elif route == 0:
        quickRepliesOptions = [
            {"content_type": "text",
             "title": u"لا",
             "payload": str(question_id) + key + '0'
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

def send_complete_data_quick_replies(token, user_id, intro):

    quickRepliesOptions = [
        {"content_type": "text",
         "title": "استكمال البيانات",
         "payload":'Complete_Data'
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

def send_where_to_go_quick_replies(token, user_id, intro):

    quickRepliesOptions = [
        {"content_type": "text",
         "title": "تشخيص",
         "payload":'Choose_Who_To_Diagnose'
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

def send_whose_diagnoses(token, user_id, intro):

    quickRepliesOptions = [
        {"content_type": "text",
         "title": "هذا التشخيص لى",
         "payload":'Show_Parts_0'
         },
        {"content_type": "text",
         "title": "هذا التشخيص لشخص اخر",
         "payload": 'Complete_Person_Data_Request'
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

def send_symptoms(token, user_id,options,first_list,part_id):
    if first_list == 0 and len(options) > 1:
        r = requests.post("https://graph.facebook.com/v2.6/me/messages",
              params={"access_token": token},
              data=json.dumps({
                    "recipient": {"id": user_id},
                    "message":{
                        "attachment":{
                            "type":"template",
                            "payload":{
                                "template_type":"list",
                                "top_element_style": "compact",
                                "elements": options
                            }
                        }
                    }
              }),
              headers={'Content-type': 'application/json'})
    elif len(options) == 1:
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

    else:
        r = requests.post("https://graph.facebook.com/v2.6/me/messages",
                          params={"access_token": token},
                          data=json.dumps({
                              "recipient": {"id": user_id},
                              "message": {
                                  "attachment": {
                                      "type": "template",
                                      "payload": {
                                          "template_type": "list",
                                          "top_element_style": "compact",
                                          "elements": options,
                                          "buttons": [
                                              {
                                                  "title": "المزيد",
                                                  "type": "postback",
                                                  "payload": str(part_id) + "_More_Symptoms_1"
                                              }
                                          ]
                                      }
                                  }
                              }
                          }),
                          headers={'Content-type': 'application/json'})
    if r.status_code != requests.codes.ok:
        print r.text


def send_more_symptoms(token, user_id,options,list_num,part_id):
    if list_num == 0 and len(options) > 1:
        r = requests.post("https://graph.facebook.com/v2.6/me/messages",
              params={"access_token": token},
              data=json.dumps({
                    "recipient": {"id": user_id},
                    "message":{
                        "attachment":{
                            "type":"template",
                            "payload":{
                                "template_type":"list",
                                "top_element_style": "compact",
                                "elements": options
                            }
                        }
                    }
              }),
              headers={'Content-type': 'application/json'})
    elif len(options) == 1:
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
    else:
        r = requests.post("https://graph.facebook.com/v2.6/me/messages",
                          params={"access_token": token},
                          data=json.dumps({
                              "recipient": {"id": user_id},
                              "message": {
                                  "attachment": {
                                      "type": "template",
                                      "payload": {
                                          "template_type": "list",
                                          "top_element_style": "compact",
                                          "elements": options,
                                          "buttons": [
                                              {
                                                  "title": "المزيد",
                                                  "type": "postback",
                                                  "payload": str(part_id) + "_More_Symptoms_" + str(list_num)
                                              }
                                          ]
                                      }
                                  }
                              }
                          }),
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
