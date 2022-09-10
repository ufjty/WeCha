##############################
##
##       作者：张澳旗
##     微信：17600005204
##   有偿代做、每天自动推送
##
##############################

import cityinfo
import http.client, urllib
import json
import os
import random
import requests
import sys
from datetime import datetime, date
from requests import get, post
from time import time, localtime
from zhdate import ZhDate



# 随机颜色
def Get_Color():
    get_colors = lambda n: list(map(lambda i: "#" + "%06x" % random.randint(0, 0xFFFFFF), range(n)))
    color_list = get_colors(100)
    return random.choice(color_list)

# 验证测试号
def Get_WeChat():
    app_id = config["app_id"]
    app_secret = config["app_secret"]
    post_url = ("https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={}&secret={}"
                .format(app_id, app_secret))
    try:
        access_token = get(post_url).json()['access_token']
    except KeyError:
        print("获取access_token失败，请检查app_id和app_secret是否正确")
        os.system("pause")
        sys.exit(1)
    return access_token

# 生日倒计时
def Get_Birthday(birthday, year, today):
    birthday_year = birthday.split("-")[0]
    # 判断是否为农历生日
    if birthday_year[0] == "y":
        r_mouth = int(birthday.split("-")[1])
        r_day = int(birthday.split("-")[2])
        # 今年生日
        birthday = ZhDate(year, r_mouth, r_day).to_datetime().date()
        year_date = birthday
    else:
        # 获取国历生日的今年对应月和日
        birthday_month = int(birthday.split("-")[1])
        birthday_day = int(birthday.split("-")[2])
        # 今年生日
        year_date = date(year, birthday_month, birthday_day)
    # 计算生日年份，如果还没过，按当年减，如果过了需要+1
    if today > year_date:
        if birthday_year[0] == "y":
            # 获取农历明年生日的月和日
            r_last_birthday = ZhDate((year + 1), r_mouth, r_day).to_datetime().date()
            birth_date = date((year + 1), r_last_birthday.month, r_last_birthday.day)
        else:
            birth_date = date((year + 1), birthday_month, birthday_day)
        birth_day = str(birth_date.__sub__(today)).split(" ")[0]
    elif today == year_date:
        birth_day = 0
    else:
        birth_date = year_date
        birth_day = str(birth_date.__sub__(today)).split(" ")[0]
    return birth_day


# 城市天气
def Get_TianQiWenDu(C_ShengFen, C_ChengShi):
    try:
        city_id = cityinfo.cityInfo[C_ShengFen][C_ChengShi]["AREAID"]
    except KeyError:
        print("推送消息失败，请检查省份或城市是否正确")
        os.system("pause")
        sys.exit(1)
    t = (int(round(time() * 1000)))
    headers = {
        "Referer": "http://www.weather.com.cn/weather1d/{}.shtml".format(city_id),
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }
    url = "http://d1.weather.com.cn/dingzhi/{}.html?_={}".format(city_id, t)
    response = get(url, headers=headers)
    response.encoding = "utf-8"
    response_data = response.text.split(";")[0].split("=")[-1]
    response_json = eval(response_data)
    weatherinfo = response_json["weatherinfo"]

    C_TianQi = weatherinfo["weather"]
    C_ZuiDi = weatherinfo["tempn"]
    C_ZuiGao = weatherinfo["temp"]
    return C_TianQi, C_ZuiDi, C_ZuiGao

# 金山词霸
def Get_JinShanCiBa():
    if (True):
        url = "http://open.iciba.com/dsapi/"
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                        'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
        }
        r = get(url, headers=headers)
        
        C_CiBa = str(r.json()["content"]) + "\n" + str(r.json()["note"])
        return C_CiBa
    else:
        return ("金山词霸API调取错误，请检查API是否正确申请或是否填写正确")


# 天气预报
def Get_TianQiYuBao():
    if (API_TQYB != "替换掉我"):
        conn = http.client.HTTPSConnection('api.tianapi.com')
        params = urllib.parse.urlencode({'key':API_TQYB,'city':C_ChengShi})
        headers = {'Content-type':'application/x-www-form-urlencoded'}
        conn.request('POST','/tianqi/index',params,headers)
        res = conn.getresponse()
        data = res.read()
        data = json.loads(data)
        
        C_JiangYu = data["newslist"][0]["pop"]
        C_ChuXing = data["newslist"][0]["tips"]
        return C_JiangYu, C_ChuXing
    else:
        return ("天气预报API调取错误，请检查API是否正确申请或是否填写正确")

# 星座运势
def Get_XingZuoYunSHi():
    if (API_XZYS != "替换掉我"):
        conn = http.client.HTTPSConnection('api.tianapi.com')
        params = urllib.parse.urlencode({'key':API_XZYS,'astro':S_XingZuo})
        headers = {'Content-type':'application/x-www-form-urlencoded'}
        conn.request('POST','/star/index',params,headers)
        res = conn.getresponse()
        data = res.read()
        data = json.loads(data)
        
        C_ZongHe = data["newslist"][0]["content"]
        C_AiQing = data["newslist"][1]["content"]
        C_GongZuo = data["newslist"][2]["content"]
        C_CaiYun = data["newslist"][3]["content"]
        C_JianKang = data["newslist"][4]["content"]
        C_XingZuo = data["newslist"][8]["content"]
        return C_ZongHe, C_AiQing, C_GongZuo, C_CaiYun, C_JianKang, C_XingZuo
    else:
        return ("星座运势API调取错误，请检查API是否正确申请或是否填写正确")


# 早安心语
def Get_ZaoAnXinYu():
    if (API_ZAXY != "替换掉我"):
        conn = http.client.HTTPSConnection('api.tianapi.com')
        params = urllib.parse.urlencode({'key':API_ZAXY})
        headers = {'Content-type':'application/x-www-form-urlencoded'}
        conn.request('POST','/zaoan/index',params,headers)
        res = conn.getresponse()
        data = res.read()
        data = json.loads(data)
        
        C_ZaoAn = data["newslist"][0]["content"]
        return C_ZaoAn
    else:
        return ("早安心语API调取错误，请检查API是否正确申请或是否填写正确")

# 晚安心语
def Get_WanAnXinYu():
    if (API_WAXY != "替换掉我"):
        conn = http.client.HTTPSConnection('api.tianapi.com')
        params = urllib.parse.urlencode({'key':API_WAXY})
        headers = {'Content-type':'application/x-www-form-urlencoded'}
        conn.request('POST','/wanan/index',params,headers)
        res = conn.getresponse()
        data = res.read()
        data = json.loads(data)
        
        C_WanAn = data["newslist"][0]["content"]
        return C_WanAn
    else:
        return ("晚安心语API调取错误，请检查API是否正确申请或是否填写正确")


# 舔狗日记
def Get_TianGouRiJi():
    if (API_TGRJ != "替换掉我"):
        conn = http.client.HTTPSConnection('api.tianapi.com')
        params = urllib.parse.urlencode({'key':API_TGRJ})
        headers = {'Content-type':'application/x-www-form-urlencoded'}
        conn.request('POST','/tiangou/index',params,headers)
        res = conn.getresponse()
        data = res.read()
        data = json.loads(data)
        
        C_TianGou = data["newslist"][0]["content"]
        return C_TianGou
    else:
        return ("舔狗日记API调取错误，请检查API是否正确申请或是否填写正确")

# 土味情话
def Get_TuWeiQingHua():
    if (API_TWQH != "替换掉我"):
        conn = http.client.HTTPSConnection('api.tianapi.com')
        params = urllib.parse.urlencode({'key':API_TWQH})
        headers = {'Content-type':'application/x-www-form-urlencoded'}
        conn.request('POST','/saylove/index',params,headers)
        res = conn.getresponse()
        data = res.read()
        data = json.loads(data)
        
        C_TuWei = data["newslist"][0]["content"]
        return C_TuWei
    else:
        return ("土味情话API调取错误，请检查API是否正确申请或是否填写正确")


# 表白文案
def Get_BiaoBaiWenAn():
	C_BiaoBai = requests.get("https://api.shadiao.pro/chp")
	if C_BiaoBai.status_code != 200:
		return Get_BiaoBaiWenAn()
	return C_BiaoBai.json()['data']['text']

# 自定义字符串
def Get_String(C_String01, C_String02, C_String03):
    return C_String01, C_String02, C_String03



# 生成接口
def send_message(to_user, access_token):
    url = "https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={}".format(access_token)
    week_list = ["星期日", "星期一", "星期二", "星期三", "星期四", "星期五", "星期六"]
    year = localtime().tm_year
    month = localtime().tm_mon
    day = localtime().tm_mday
    today = datetime.date(datetime(year=year, month=month, day=day))
    week = week_list[today.isoweekday() % 7]
    # 获取在一起的日子的日期格式
    love_year = int(config["S_Love"].split("-")[0])
    love_month = int(config["S_Love"].split("-")[1])
    C_Love = int(config["S_Love"].split("-")[2])
    S_Love = date(love_year, love_month, C_Love)
    # 获取在一起的日期差
    love_days = str(today.__sub__(S_Love)).split(" ")[0]
    # 获取所有生日数据
    birthdays = {}
    for k, v in config.items():
        if k[0:5] == "birth":
            birthdays[k] = v
    data = {
        "touser": to_user,
        "template_id": config["template_id"],
        "url": "https://weixin110.qq.com/security/con/newreadtemplate?t=banurlplaintext/index.html&midpagecode=45166ef79c3450b81536cb1836811971636b1e23784cf4d6649cce002f899295fe50d3e479f5bfc0a1538e77ac7f094318b003c65eab66381defee1fe8acbf7ed23d3b930ab808e9f9c40be783598a7cf87d6e634ebb54bf608f56e97a742e9631d35591d0f54df6f59615204ff8d5f9c5c6d586bdcc5fa7581312a7cd62ab59529e05f3a150261a80ec959e2b38bc10e588ba65ec760598a777d66af1616b74798016a898096c76352ae307a93f828b539e58a97325feafdf69bbdf489ca06e89663612e6c2b49e666c8ca89e7b780503797dd29b48e46a942d67fc6a4cc045303011df5b16689107d0bf503cbbeeebaff6ea59a663773cf581076b9820a7412fef4b786a2286098deb69b373d1c3f8f83da32027689e1a6f9508c53c466660960e73c6b395bb4e4e76012c6f4186332b0bcd4f56e099494d56902885d98a50",
        "topcolor": "#FF0000",
        "data":
        {
            # 当前时间
            "date": {"value": "{} {}".format(today, week), "color": Get_Color()},
            
            # 纪念日
            "C_Love": {"value": love_days, "color": Get_Color()},
            
            # 省份
            "C_ShengFen": {"value": C_ShengFen, "color": Get_Color()},
            
            # 城市
            "C_ChengShi": {"value": C_ChengShi, "color": Get_Color()},
            
            
            # 天气变化
            "C_TianQi": {"value": C_TianQi, "color": Get_Color()},
            
            # 最低气温
            "C_ZuiDi": {"value": C_ZuiDi, "color": Get_Color()},
            
            # 最高气温
            "C_ZuiGao": {"value": C_ZuiGao, "color": Get_Color()},
            
            # 金山词霸
            "C_CiBa": {"value": C_CiBa, "color": Get_Color()},
            
            
            # 降雨概率
            "C_JiangYu": {"value": C_JiangYu, "color": Get_Color()},
            
            # 出行建议
            "C_ChuXing": {"value": C_ChuXing, "color": Get_Color()},
            
            # 综合指数
            "C_ZongHe": {"value": C_ZongHe, "color": Get_Color()},
            
            # 爱情指数
            "C_AiQing": {"value": C_AiQing, "color": Get_Color()},
            
            # 工作指数
            "C_GongZuo": {"value": C_GongZuo, "color": Get_Color()},
            
            # 财运指数
            "C_CaiYun": {"value": C_CaiYun, "color": Get_Color()},
            
            # 健康指数
            "C_JianKang": {"value": C_JianKang, "color": Get_Color()},
            
            # 星座运势
            "C_XingZuo": {"value": C_XingZuo, "color": Get_Color()},
            
            
            # 早安心语
            "C_ZaoAn": {"value": C_ZaoAn, "color": Get_Color()},
            
            # 晚安心语
            "C_WanAn": {"value": C_WanAn, "color": Get_Color()},
            
            
            # 舔狗日记
            "C_TianGou": {"value": C_TianGou, "color": Get_Color()},
            
            # 土味情话
            "C_TuWei": {"value": C_TuWei, "color": Get_Color()},
            
            
            # 表白文案
            "C_BiaoBai": {"value":C_BiaoBai, "color":Get_Color()},
            
            # 自定义字符串01
            "C_String01": {"value":C_String01, "color":Get_Color()},
            
            # 自定义字符串02
            "C_String02": {"value":C_String02, "color":Get_Color()},
            
            # 自定义字符串03
            "C_String03": {"value":C_String03, "color":Get_Color()}
        }
    }
    for key, value in birthdays.items():
        # 获取距离下次生日的时间
        birth_day = Get_Birthday(value, year, today)
        # 将生日数据插入data
        data["data"][key] = {"value": birth_day, "color": Get_Color()}
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }
    response = post(url, headers=headers, json=data).json()
    if response["errcode"] == 40037:
        print("推送消息失败，请检查模板id是否正确")
    elif response["errcode"] == 40036:
        print("推送消息失败，请检查模板id是否为空")
    elif response["errcode"] == 40003:
        print("推送消息失败，请检查微信号是否正确")
    elif response["errcode"] == 0:
        print("推送消息成功")
    else:
        print(response)



# 消息推送
if __name__ == "__main__":
    try:
        with open("config.txt", encoding="utf-8") as f:
            config = eval(f.read())
    except FileNotFoundError:
        print("推送消息失败，请检查config.txt文件是否与程序位于同一路径")
        os.system("pause")
        sys.exit(1)
    except SyntaxError:
        print("推送消息失败，请检查配置文件格式是否正确")
        os.system("pause")
        sys.exit(1)

    # 获取accessToken
    accessToken = Get_WeChat()
    # 接收的用户
    users = config["user_id"]
    
    
    # 城市天气API
    C_ShengFen, C_ChengShi = config["C_ShengFen"], config["C_ChengShi"]
    # 自定义字符串
    C_String01, C_String02, C_String03 = config["C_String01"], config["C_String02"], config["C_String03"]
    
    # 天气预报API
    API_TQYB = config["API_TQYB"]
    # 星座运势API
    S_XingZuo = config["S_XingZuo"]
    API_XZYS = config["API_XZYS"]
    
    # 早安心语API
    API_ZAXY = config["API_ZAXY"]
    # 晚安心语API
    API_WAXY = config["API_WAXY"]
    
    # 舔狗日记API
    API_TGRJ = config["API_TGRJ"]
    # 土味情话API
    API_TWQH = config["API_TWQH"]
    
    
    # 城市天气
    C_TianQi, C_ZuiDi, C_ZuiGao = Get_TianQiWenDu(C_ShengFen, C_ChengShi)
    # 金山词霸
    C_CiBa = Get_JinShanCiBa()
    
    # 天气预报
    C_JiangYu, C_ChuXing = Get_TianQiYuBao()
    # 星座运势
    C_ZongHe, C_AiQing, C_GongZuo, C_CaiYun, C_JianKang, C_XingZuo = Get_XingZuoYunSHi()
    
    # 早安心语
    C_ZaoAn = Get_ZaoAnXinYu()
    # 晚安心语
    C_WanAn = Get_WanAnXinYu()
    
    # 舔狗日记
    C_TianGou = Get_TianGouRiJi()
    # 土味情话
    C_TuWei = Get_TuWeiQingHua()
    
    # 表白文案
    C_BiaoBai = Get_BiaoBaiWenAn()
    # 自定义字符串
    C_String01, C_String02, C_String03 = Get_String(C_String01, C_String02, C_String03)
    
    
    # 公众号推送消息
    for user_id in users:
        send_message(user_id, accessToken)
    import time
    time_duration = 3.5
    time.sleep(time_duration)