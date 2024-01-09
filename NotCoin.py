from telethon import TelegramClient,functions
from urllib.parse import unquote
import subprocess
import requests
import base64
import random
import time

webappdata_global = ""
client = TelegramClient("cheat",123,"123").start()

session = requests.Session()
session.headers = {
    "accept": "application/json",
    "Accept-Language":"en,en-US;q=0.9",
    "auth":"1",
    "Connection":"keep-alive",
    "Host": "clicker-api.joincommunity.xyz",
    "Origin": "https://clicker.joincommunity.xyz",
    "Referer": "https://clicker.joincommunity.xyz/",
    "User-Agent": "Mozilla/5.0 (Linux; Android 9; SM-N975F Build/PI; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/120.0.6099.116 Mobile Safari/537.36",
    "X-Requested-With": "org.telegram.messenger.web",
}

def send_coin(count,hash):
    global webappdata_global
    print("making coins:",count,"with hash",hash)
    data = {
    "count":count ,
    "webAppData": webappdata_global,
    "hash": hash
    }
    r = session.post("https://clicker-api.joincommunity.xyz/clicker/core/click",json=data)
    try:
        return r.json()
    except:
        pass

async def GetWebAppData():
    global webappdata_global
    notcoin = await client.get_entity("notcoin_bot")
    msg = await client(functions.messages.RequestWebViewRequest(notcoin,notcoin,platform="android",url="https://clicker.joincommunity.xyz/clicker"))
    webappdata_global = msg.url.split('https://clicker.joincommunity.xyz/clicker#tgWebAppData=')[1].replace("%3D","=").split('&tgWebAppVersion=')[0].replace("%26","&")
    user_data = webappdata_global.split("&user=")[1].split("&auth")[0]
    webappdata_global = webappdata_global.replace(user_data,unquote(user_data))

def getAuthToken():
    global webappdata_global,session
    client.loop.run_until_complete(GetWebAppData())
    data = {
        "webAppData": webappdata_global
        }
    
    session.headers.update({"content-length":str(len(data))})
    r = session.post("https://clicker-api.joincommunity.xyz/auth/webapp-session",json=data)
    session.headers.update({"Authorization":"Bearer " + r.json()['data']['accessToken']})

def evaluate_js(string):
    if string == "document.querySelectorAll('body').length":
        return 1
    elif "window.location" in string:
        return 121
    elif "window.Telegram.WebApp" in string:
        return 5

    open("evalit.js","w").write(f"console.log({string})")
    result = subprocess.getoutput("node evalit.js").replace(" ","")
    try:
        return int(result)
    except:
        print("error on evaluate",result)

def base_64(data):
    return base64.b64decode(data.encode()).decode("utf-8")

def evaluate_hash(hashes):
    if len(hashes) != 1:
        sum = 0
        for i in hashes:
            sum += evaluate_js(base_64(i))

        return sum
    else:
        return evaluate_js(base_64(hashes[0]))

getAuthToken()
coin_boost = 4
start_hash = 1

send_result = send_coin(coin_boost,1)
start_hash = evaluate_hash(send_result['data'][0]['hash'])

while True:
    try:
        count = (random.randint(20,100) // coin_boost) * coin_boost
        send_result = send_coin(count,start_hash)
        hashes = send_result['data'][0]['hash']
        start_hash = evaluate_hash(hashes)
        
        print("started_hash",start_hash)
        print("lastAvailableCoins",send_result['data'][0]['lastAvailableCoins'])
        if send_result['data'][0]['lastAvailableCoins'] < 60:
            print("collect limited. sleeping 120")
            time.sleep(120)    
        time.sleep(2)
    except KeyError:
        getAuthToken()
        print("Session Expired Getting new session")
