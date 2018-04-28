import os
import time
import tweepy
import datetime
import json
from bottle import route, run
from bottle import TEMPLATE_PATH, jinja2_template as template

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_PATH.append(BASE_DIR + "/views")


CONSUMER_KEY = ""
CONSUMER_SECRET = ""
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
ACCESS_TOKEN = ""
ACCESS_SECRET = ""
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

api = tweepy.API(auth, wait_on_rate_limit=True)
get_friends = api.friends
get_tweet = api.user_timeline
f = open('baypic.json', 'r')
g = open('id.json', 'r')
json_data = json.load(f)
id_data = json.load(g)

@route('/top')
def top():

    print (datetime.datetime.today())
    url = json_data
    dic = id_data
    for friend in tweepy.Cursor(get_friends, id = "").items():
        value1 = 0
        c = friend.screen_name
        print(c)
        if dic.has_key(c):
            value = dic[c]
        else:
            value = 0
        for status in tweepy.Cursor(get_tweet, id=c).items():
            time.sleep(0.2)
            if value1 == 0:
                value1 = status.id
            if status.id == value:
                break
            if status.favorited == True:
                try:
                    j = 0
                    k = 0
                    for i in status.extended_entities['media']:
                        if i['media_url'] in url:
                            k = k + 1
                            break
                        else:
                            url.append(i['media_url'])
                            print(i['media_url'])
                        j = j + 1
                    if(k!=0):
                        break
                except:
                    pass
        dic[c] = value1

    fw = open('baypic.json', 'w')
    gw = open('id.json', 'w')
    li_uniq = list(set(url))
    json.dump(li_uniq, fw, indent=4)
    json.dump(dic, gw, indent=4)
    print len(li_uniq)
    print (datetime.datetime.today())

    return template('top', name="Gacky", fizzbuzz=li_uniq)

if __name__ == "__main__":
    run(host="localhost", port=8070, debug=True, reloader=True)
