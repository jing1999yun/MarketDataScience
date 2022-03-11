#載入LineBot所需要的套件
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)

# 必須放上自己的Channel Access Token
line_bot_api = LineBotApi('GG5+TOl68aadhcqGUTruwF6NNWjpdkHlnpgCyxufI40UvZLoSV4AiE/03lhj6piMQs/+4qBrzEuwbCG7RvOgd/FM0JFt6hhbxnGQ1NEzMyM05MRV/FnsAYRARehm0qTu/vGOOuHatkF3sFBNlzVdjwdB04t89/1O/w1cDnyilFU=')
# 必須放上自己的Channel Secret
handler = WebhookHandler('80da3653bc5c4f4103688a0ef934b1a0')
# 必須放上自己的User ID
line_bot_api.push_message('U85adcf8fcca10fdb462cc5d30f318c9d', TextSendMessage(text='你可以開始了'))

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


#主程式
import numpy as np
import pandas as pd
import os, time, socket, glob, requests, json

authorization = "CWB-98580B1F-26F4-44AB-8CBF-0AF2F2AE622A"
url = "https://opendata.cwb.gov.tw/api/v1/rest/datastore/O-A0002-001?Authorization=CWB-98580B1F-26F4-44AB-8CBF-0AF2F2AE622A"
res = requests.get(url, {"Authorization": authorization})
resJson = res.json()

locName = []
lat = []
lon = []
obsTime = []
elev = []
rain = []
min_10 = []
hour_3 = []
hour_6 = []
hour_12 = []
hour_24 = []
now = []
lastest_2days = []
lastest_3days = []
city = []
town = []
for i in range(0, len(resJson["records"]["location"])):
    locName.append(resJson["records"]["location"][i]['locationName']) #觀測站名稱
    lat.append(resJson["records"]["location"][i]['lat'])   #緯度
    lon.append(resJson["records"]["location"][i]['lon'] )  #經度
    obsTime.append(resJson["records"]["location"][i]['time']['obsTime'])   #觀測時間
    elev.append(resJson["records"]["location"][i]['weatherElement'][0]['elementValue'])   #高度
    rain.append( resJson["records"]["location"][i]['weatherElement'][1]['elementValue'])  #60分鐘累積雨量
    min_10.append(resJson["records"]["location"][i]['weatherElement'][2]['elementValue'])   #10分鐘累積雨量
    hour_3.append(resJson["records"]["location"][i]['weatherElement'][3]['elementValue'])   #3小時累積雨量
    hour_6.append(resJson["records"]["location"][i]['weatherElement'][4]['elementValue'])   #6小時累積雨量
    hour_12.append(resJson["records"]["location"][i]['weatherElement'][5]['elementValue'])   #12小時累積雨量
    hour_24.append(resJson["records"]["location"][i]['weatherElement'][6]['elementValue'])   #24小時累積雨量
    now.append(resJson["records"]["location"][i]['weatherElement'][7]['elementValue'])   #本日累積雨量
    lastest_2days.append(resJson["records"]["location"][i]['weatherElement'][8]['elementValue'])   #前1日0時到現在之累積雨量
    lastest_3days.append(resJson["records"]["location"][i]['weatherElement'][9]['elementValue'])   #前2日0時到現在之累積雨量
    city.append(resJson["records"]["location"][i]['parameter'][0]['parameterValue'])   #所在縣市
    town.append(resJson["records"]["location"][i]['parameter'][2]['parameterValue'])   #所在鄉鎮
    
df = pd.DataFrame({
    "觀測站名稱":locName, "緯度":lat, "經度":lon,
    "觀測時間":obsTime, "高度":elev, 
    "60分鐘累積雨量":rain, "10分鐘累積雨量":min_10, 
    "3小時累積雨量":hour_3, "6小時累積雨量":hour_6, "12小時累積雨量":hour_12, "24小時累積雨量":hour_24,
    "本日累積雨量":now, "前1日0時到現在之累積雨量":lastest_2days, "前2日0時到現在之累積雨量":lastest_3days, 
    "所在縣市":city, "所在鄉鎮":town, "自動站屬性":attribute
})


    #訊息傳遞區塊
##### 基本上程式編輯都在這個function #####
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = TextSendMessage(text=event.message.text)
    
    df1 = df[(df['所在縣市'] == message[:3]) & (df['所在鄉鎮'] == message[3:6])]
    ans = str()
    for i in range(len(df1)):
        #觀測站名稱+本日累積雨量
        ans = ans + '觀測站：' + str(df1.iloc[i][0]) + '，今日累積雨量：' + str(df1.iloc[i][11]) + '\n'
    if(message[3:6] in df1['所在鄉鎮']):
        line_bot_api.reply_message(event.reply_token,ans)
    else:
        line_bot_api.reply_message(event.reply_token,text = '我學藝不精')


import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)








