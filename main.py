from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random
from bs4 import BeautifulSoup
today = datetime.now()
start_date = os.environ['START_DATE']
city = os.environ['CITY']
birthday = os.environ['BIRTHDAY']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
template_id = os.environ["TEMPLATE_ID"]


def get_weather():
  url = "https://www.tianqi.com/suzhou/"
  headers = {
      'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36'
      ,
      'cookie': 'Hm_lvt_ab6a683aa97a52202eab5b3a9042a8d2=1661411951; Hm_lvt_30606b57e40fddacb2c26d2b789efbcb=1661413345; Hm_lpvt_3060'
                '6b57e40fddacb2c26d2b789efbcb=1661414297; cs_prov=04; cs_city=0401; ccity=101040100; Hm_lpvt_ab6a683aa97a52202eab5b3a9'
                '042a8d2=1661414326'
  }
  resp = requests.get(url=url, headers=headers).text
  html = BeautifulSoup(resp, 'html.parser')
  html2 = html.find('div', class_="weatherbox").find("dl", class_="weather_info").find('dd',class_="weather").find('span').text  # 获取当天温度
  html3 = html.find('div', class_="weatherbox").find("dl", class_="weather_info").find('dd',class_="shidu").text  # 湿度，风度紫外线
  html4 = html.find('div', class_="weatherbox").find("dl", class_="weather_info").find('dd',class_="kongqi").text  # 空气质
  return html2,html3,html4

def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

def get_birthday():
  next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
wea, humidity,quality = get_weather()
data = {"weather":{"value":wea},"humidity":{"value":humidity},"quality":{"value":quality},"love_days":{"value":get_count()},"birthday_left":{"value":get_birthday()},"words":{"value":get_words(), "color":get_random_color()}}
res = wm.send_template(user_id, template_id, data)
print(res)
