from wxpy import *
from sympy import *
import json
import urllib.request
import numpy as np
import time
import datetime
import requests
import sched
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler

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
    n = 0
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
        seq.append(n)
        n += 1
        #print(i + '\tHI:' + str(round(daymax - 273.15, 1)) + '°C, LOW:' + str(round(daymin - 273.15, 1)) + '°C')
        #result += (i + '\nHI:' + str(round(daymax - 273.15, 1)) + '°C, LOW:' + str(round(daymin - 273.15, 1)) + '°C\n')

    #根据日期顺序进行排序
    min = 99999999
    lastpos = 0
    pos = 0
    n = 0
    for i in range(0,len(T)):
        for i in range(n, len(T)):
            if T[i] < min:
                min = T[i]
                pos = i

        temp = seq[n]
        seq[n] = seq[pos]
        seq[pos] = temp

        temp = T[n]
        T[n] = T[pos]
        T[pos] = temp

        min = 99999999
        n += 1

    for i in range(0, len(DATE)):
        result += (DATE[seq[i]] + '\nHI:' + str(round(HI[seq[i]] - 273.15, 1)) + '°C, LOW:' + str(round(LOW[seq[i]] - 273.15, 1)) + '°C\n')

    return result

def getweather():
    source = 'EC'
    iodata = getData(source, -79.399, 43.663)
    result = analyze(source, iodata)
    print('[' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ']发送天气信息完成')
    return result

def turingreply(msg,usr):
    data = {'key': '1f87c3c9cf3b4867b412267f8c7c1d30',
            'info': msg,
            'loc': '',
            'userid': usr}
    r = requests.post(url='http://www.tuling123.com/openapi/api', data = data)
    result = json.loads(r.text)
    return result['text']

def msgdiff(msg):
    msg = msg.replace('／', '/');
    msg = msg.replace('？', '?');
    msg = msg.replace('。', '.');
    msg = msg.replace('，', ',');
    msg = msg.replace('；', ';');
    x = Symbol("x")
    s = msg
    return(str(diff(s, x)) + '\n- 叮咚云计算v1')

def msgrref(msg):
    msg = msg.replace('／', '/');
    msg = msg.replace('？', '?');
    msg = msg.replace('。', '.');
    msg = msg.replace('，', ',');
    msg = msg.replace('；',';');
    msg = msg.replace(' ', '');

    middle = []
    tmp = []
    flag = 0

    while msg.find(';') != -1 or flag == 1:
        tmp = []
        tempstr = msg[0:msg.find(';')]
        if msg.find(';') == -1:
            tempstr = msg[0:len(msg)]
        while tempstr.find(',') != -1:
            tmp.append(int(tempstr[0:tempstr.find(',')]))
            tempstr = tempstr[tempstr.find(',') + 1:len(tempstr)]
        tmp.append(int(tempstr[0:len(tempstr)]))
        middle.append(tmp)
        msg = msg[msg.find(';') + 1:len(msg)]
        if flag == 1:
            flag += 1
        if msg.find(';') == -1 and flag == 0:
            flag += 1

    M = Matrix(middle)
    rref = M.rref()
    result = ""
    for i in range(0, M.rows):
        for j in range(0, M.cols):
            if j != M.cols - 1:
                result += str(list(rref[0])[i * M.cols + j]) + ','
            else:
                result += str(list(rref[0])[i * M.cols + j])
        result += '\n'
    result += 'with leading term on col: '
    for i in range(0, len(list(rref[1]))):
        if i != len(list(rref[1])) - 1:
            result += str(rref[1][i]+1) + ','
        else:
            result += str(rref[1][i]+1) + '.'
    result += '\n- 叮咚云计算v1'
    return result

def clearlog():
    #clear logs every hour
    f = open('/home/weather/hsefz_server/wxbot/record/txtrecord.txt', 'w')
    f.write('[' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ']record重新写入')
    f.close()  # you can omit in most cases as the destructor will call it
    print('[' + time.strftime("%Y-%m-%d %H:%M:%S",
                                time.localtime()) + ']record重制完成')


scheduler = BackgroundScheduler()
scheduler.add_job(clearlog, 'interval', seconds = 3600 * 6)#间隔6小时执行一次
scheduler.start()    #这里的调度任务是独立的一个线程

#initialize
print('[' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ']机器人准备登陆')
bot = Bot(console_qr = 2)#log in (need scan QRcode)

print('[' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ']机器人登陆成功')
myself = bot.self
#SG = bot.groups().search(' ')[0]
#my_friend = bot.friends().search(' ')[0]
# 打印来自其他好友、群聊和公众号的消息

@bot.register(except_self = False)
def print_others(msg):
    print('[' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ']' + str(msg))
    f = open('/home/weather/hsefz_server/wxbot/record/txtrecord.txt', 'w+')
    f.write('[' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ']' + str(msg))
    f.close()  # you can omit in most cases as the destructor will call it

    if msg.text == '天气' or msg.text == '气温' or msg.text == '气象':
        try:
            print('[' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ']准备发送天气信息')
            return getweather()
        except:
            return '[ERR100:内部错误]抱歉，调取最新天气失败'
    elif msg.text[0:4] == '叮咚求导':
        try:
            result = msgdiff(msg.text[4:len(msg.text)])
            print('[' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ']求导完成：' + result)
            return result
        except:
            return '[ERR102:用户错误]抱歉，输入公式格式有误，语法例如:叮咚求导2*x^2'
    elif msg.text[0:6] == '叮咚RREF' or msg.text[0:6] == '叮咚rref':
        try:
            result = msgrref(msg.text[6:len(msg.text)])
            print('[' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ']RREF计算完成：' + result)
            return result
        except:
            return '[ERR102:用户错误]抱歉，输入格式有误,语法例如:叮咚rref1,2;3,4'
    elif msg.text[0:2] == '叮咚':
        try:
            usr = str(msg.sender.remark_name)
            print('检测到用户：' + usr)
        except:
            usr = str(msg.member.name)
            print('[WARNING]属于群聊的信息' + '，检测到用户：' + usr)
        message = msg.text[2:len(msg.text)]

        try:
            print('[' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ']自动回复开启')
            reply = turingreply(message,usr)
            print('[' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ']自动回复：' + reply)
            return reply + '[auto-reply]'
        except:
            myself.send('[' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ']'+'[ERR199:未知错误]程序调用出现错误，请检查！')
            return '[ERR199:未知错误]抱歉，出现了未知错误'

'''
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
            return '[ERR100:内部错误]抱歉，调取最新天气失败'
'''
'''
@bot.register(my_friend, TEXT)
def weather_reply(msg):
    print('[' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ']' + str(msg))
    if msg.text == '天气' or msg.text == '气温' or msg.text == '气象':
        try:
            print('[' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ']准备发送天气信息')
            return getweather()
        except:
            return '[ERR100:内部错误]抱歉，调取最新天气失败'
'''
embed()
#print(msgrref('4,-12,4;3,-14,8;4,-11,3'))