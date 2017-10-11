from wxpy import *
import json
import urllib.request
import numpy as np
import time
import datetime

def getData(org,lon,lat):
    if org == 'GFS':
        data = urllib.request.urlopen('https://node.windy.com/forecast/v2.1/gfs/' + str(lat) +'/' + str(lon) + '?source=detail').read()
    if org == 'EC':
        data = urllib.request.urlopen('https://node.windy.com/forecast/v2.1/ecmwf/' + str(lat) +'/' + str(lon) + '?setup=summary&includeNow=true&source=hp').read()
    record = data.decode('UTF-8')
    data = json.loads(record)

    '''
    for i in range(0,len(data)):
        station.append(data[i]['station']['city'])
        province.append(data[i]['station']['province'])
        code.append(data[i]['station']['code'])
        time.append(data[i]['publish_time'])
        T.append(data[i]['temperature'])
        day1day.append(float(data[i]['detail'][0]['day']['weather']['temperature']))
        day1night.append(data[i]['detail'][0]['night'])
        day2day.append(float(data[i]['detail'][1]['day']['weather']['temperature']))
        day2night.append(data[i]['detail'][1]['night'])

        day1dayweather.append(int(data[i]['detail'][0]['day']['weather']['img']))
        day2dayweather.append(int(data[i]['detail'][1]['day']['weather']['img']))
    '''
    return data

def analyze(source, JSON):
    T = []
    HI = []
    LOW = []
    DATE = []

    seq = []
    result = "来自" + source + "模型的Toronto City天气预报：\n"
    #print(JSON)
    #'NOAA-GFS' OR 'ECMWF-HRES'
    model = JSON['header']['model']
    reftime = JSON['header']['refTime']
    daily = JSON['summary']
    print('[' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ']获取天气数据')
    for i in daily:
        t = daily[i]['timestamp']
        daymax = daily[i]['tempMax']
        daymin = daily[i]['tempMin']

        T.append(t/100000.0)
        HI.append(daymax)
        LOW.append(daymin)
        DATE.append(i)
        #print(i + '\tHI:' + str(round(daymax - 273.15, 1)) + '°C, LOW:' + str(round(daymin - 273.15, 1)) + '°C')
        #result += (i + '\nHI:' + str(round(daymax - 273.15, 1)) + '°C, LOW:' + str(round(daymin - 273.15, 1)) + '°C\n')

    #根据日期顺序进行排序
    min = 99999999
    pos = 0
    n = 0
    for i in range (0,len(T)):
        for i in range (0, len(T)):
            if T[i] < min:
                min = T[i]
                pos = i
        print('pos'+str(pos))
        seq.append(pos + n)
        print(T)
        del T[pos]
        n += 1
    print (seq)

    for i in range(0, len(DATE)):
        result += (DATE[i] + '\nHI:' + str(round(HI[i] - 273.15, 1)) + '°C, LOW:' + str(round(LOW[i] - 273.15, 1)) + '°C\n')

    return result


def getweather():
    source = 'EC'
    iodata = getData(source, -79.399, 43.663)
    result = analyze(source, iodata)
    print('[' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ']发送天气信息完成')
    return result

'''
#initialize
bot = Bot(console_qr = 2)#log in (need scan QRcode)

SG = bot.groups().search('ce男神日常恩爱群')[0]
my_friend = bot.friends().search('黄麟珂')[0]
# 打印来自其他好友、群聊和公众号的消息
@bot.register()
def print_others(msg):
    print('[' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ']' + str(msg))
    if msg.text == '天气' or msg.text == '气温' or msg.text == '气象':
        try:
            print('[' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ']准备发送天气信息')
            return getweather()
        except:
            return '抱歉，调取最新天气失败'


@bot.register(SG, TEXT)
def auto_reply(msg):
    print('[' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ']' + str(msg))
    if msg.text=='test':
        # 回复消息内容和类型
        # return '收到消息: {} ({})'.format(msg.text, msg.type)
        print('[' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ']向' + SG.remark_name + '发送信息')
        return 'wechat Auto-reply TEST PASS'
    if msg.text == '天气' or msg.text == '气温' or msg.text == '气象':
        try:
            print('[' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ']准备发送天气信息')
            return getweather()
        except:
            return '抱歉，调取最新天气失败'

@bot.register(my_friend, TEXT)
def weather_reply(msg):
    print('[' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ']' + str(msg))
    if msg.text == '天气' or msg.text == '气温' or msg.text == '气象':
        try:
            print('[' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ']准备发送天气信息')
            return getweather()
        except:
            return '抱歉，调取最新天气失败'

embed()
'''
print (getweather())