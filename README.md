# NotCoin-Cheat
[NotCoin_bot cheat script](https://t.me/notcoin_bot) first time in github and ... .

### Automated Script

* This script has been completely reverse-engineered from notcoin bot.

* You should just login to your account with script.

* The algorithm of the script is such that cheats are not detected

* This script has been thoroughly tested and is working fine.

## New Update:
NotCoin Security now uses `TLS v1.3` to secure NotCoin APIs and detect bots. To bypass NotCoin Cloudflare anti-bot measures, you have two options:
1. Use the `cloudscraper` library in my GitHub repository.
2. Edit your current `cloudscraper` library .

⚠️ Note: I have tested this method with a Hetzner IP, and it may not work unless your **IP address should be clean**.

### **Method 1:**
clone my repository then 
```bash
pip3 install cloudscraper
```
```bash
pip3 uninstall cloudscraper
```
We do this to install the required libraries.

## **Method 2**:
install cloudscraper library 
```bash
pip3 install cloudscraper
```
Find your Cloudscraper path in Linux at `/home/username/.local/lib/python3.xx/site-packages/cloudscraper`. 
After that, go ahead and open `__init__.py` and edit line 86 as shown in the picture.

![image](https://raw.githubusercontent.com/ConfusedCharacter/NotCoin-Cheat/main/help-cloud.png)

**Done.**

# installation:

Edit line `11,12` and `129` in "NotCoin.py". In line `129`, it should be your coins multiplied by one click. In line `11,12`, you should put your Telegram `api_id` and `api_hash`.

you can get api id and hash from here <https://my.telegram.org> development part.

install nodejs first
```bash
sudo apt install nodejs
```
install telethon library

```bash
pip3 install telethon
```

install cloudscraper library

```bash
pip3 install cloudscraper
```

```bash
git clone https://github.com/ConfusedCharacter/NotCoin-Cheat; cd NotCoin-Cheat
```

read `New Update` part and run it!

```bash
python3 NotCoin.py
```

## Test image:

![image](https://raw.githubusercontent.com/ConfusedCharacter/NotCoin-Cheat/main/test-image.png)

I would appreciate it if you give a star and mention the repository❤️.

**Author: ConfusedCharacter**
