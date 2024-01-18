from telethon import TelegramClient,functions
from requests.adapters import HTTPAdapter
from requests.sessions import Session
from urllib.parse import unquote
import subprocess
import base64
import random
import json
import time
import ssl

webappdata_global = ""
api_id = 123 # your api id
api_hash = "123" # your api hash
client = TelegramClient("cheat",api_id,api_hash).start()



class TLSv1_3_BYPASS(HTTPAdapter):
    ciphers = "TLS_AES_128_GCM_SHA256:TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256:ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:ECDHE-RSA-AES128-SHA:ECDHE-RSA-AES256-SHA:AES128-GCM-SHA256:AES256-GCM-SHA384:AES128-SHA:AES256-SHA:DES-CBC3-SHA"
    
    def __init__(self, *args, **kwargs):
        self.ssl_context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        self.ssl_context.orig_wrap_socket = self.ssl_context.wrap_socket
        self.ssl_context.wrap_socket = self.wrap_socket
        self.ssl_context.set_ciphers(TLSv1_3_BYPASS.ciphers)
        self.ssl_context.set_ecdh_curve("prime256v1")
        self.ssl_context.minimum_version = ssl.TLSVersion.TLSv1_3
        self.ssl_context.maximum_version = ssl.TLSVersion.TLSv1_3
        super(TLSv1_3_BYPASS, self).__init__(**kwargs)

    def wrap_socket(self, *args, **kwargs):
        self.ssl_context.check_hostname = True
        return self.ssl_context.orig_wrap_socket(*args, **kwargs)

    def init_poolmanager(self, *args, **kwargs):
        kwargs["ssl_context"] = self.ssl_context
        kwargs["source_address"] = None
        return super(TLSv1_3_BYPASS, self).init_poolmanager(*args, **kwargs)

    def proxy_manager_for(self, *args, **kwargs):
        kwargs["ssl_context"] = self.ssl_context
        kwargs["source_address"] = None
        return super(TLSv1_3_BYPASS, self).proxy_manager_for(*args, **kwargs)

session = Session()
session.mount("https://", TLSv1_3_BYPASS())
session.headers = headers = {
    'Host': 'clicker-api.joincommunity.xyz',
    'Accept': 'application/json',
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
    'Auth': '5',
    'Content-Type': 'application/json',
    'Origin': 'https://clicker.joincommunity.xyz',
    'Sec-Fetch-Site': 'same-site',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://clicker.joincommunity.xyz/',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9'
}
cli = session = Session()
cli.mount("https://", TLSv1_3_BYPASS())
cli.headers = {
        "Host": "clicker-api.joincommunity.xyz",
        "Accept": "*/*",
        "Access-Control-Request-Method": "POST",
        "Access-Control-Request-Headers": "auth,authorization,content-type",
        "Origin": "https://clicker.joincommunity.xyz",
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://clicker.joincommunity.xyz/",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en-US,en;q=0.9"
}

def send_options():
    r = cli.options('https://clicker-api.joincommunity.xyz/clicker/core/click')
    print(r.status_code)

def send_coin(count,hash):
    global webappdata_global
    send_options()
    print("collect coins:",count,"with hash",hash)
    data = {
    "count":count ,
    "webAppData": webappdata_global,
    }
    if hash != -1:
        data['hash'] = hash

    data = json.dumps(data)
    session.headers.update({"Content-Length":str(len(data))})
    r = session.post("https://clicker-api.joincommunity.xyz/clicker/core/click",data=data)
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
    
    session.headers.update({"Content-Length":str(len(json.dumps(data)))})
    r = session.post("https://clicker-api.joincommunity.xyz/auth/webapp-session",json=data)
    try:
        session.headers.update({"Authorization":"Bearer " + r.json()['data']['accessToken']})
    except:
        pass

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
coin_boost = 10 # your coins multiples
start_hash = -1

try:
    count = coin_boost * 4 # dont edit this
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
    
while True:
    try:
        count = random.randint(20,100) # this mean collect from random 20 to 100 example: 80 coins or 35 coins
        print(count)
        count = (count // coin_boost) * coin_boost
        send_result = send_coin(count,start_hash)
        hashes = send_result['data'][0]['hash']
        start_hash = evaluate_hash(hashes)
        
        print("started_hash",start_hash)
        print("lastAvailableCoins",send_result['data'][0]['lastAvailableCoins'])
        if send_result['data'][0]['lastAvailableCoins'] < 60:
            print("collect limited. sleeping 120")
            time.sleep(120)    
        time.sleep(7)
    except KeyError:
        getAuthToken()
        print("Session Expired Getting new session")
        time.sleep(2)
