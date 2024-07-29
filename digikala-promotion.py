import requests
import socket
import socks
from format_currency import format_currency
import time

# Socks5 Proxy For Run On IR Servers, you can use v2ray socks5 for it.
SOCKS5_PROXY_HOST = '127.0.0.1'
SOCKS5_PROXY_PORT = 10808
default_socket = socket.socket

socks.set_default_proxy(socks.SOCKS5, SOCKS5_PROXY_HOST, SOCKS5_PROXY_PORT)
socket.socket = socks.socksocket

TOKEN="7490505749:AAHdsL4MQi9WEXMvIQfYdXXXXXXXXXXXX" 
chatID="5240000000"
URL=f"https://api.telegram.org/bot{TOKEN}/sendMessage"
productID = 15526300
checkPeriod = 1 # in minutes

def sendMessage(message):
    try:
        requests.get(URL + f"?chat_id={chatID}&text={message}")
    except Exception as e:
        print(e)

while(True):
    try:
        r = requests.get(f"https://api.digikala.com/v2/product/{productID}/")
    except Exception as e:
        print(e)

    if 'r' in locals():
        if r.status_code == 200:
            if r.json()['status'] == 200:
                price = r.json()['data']['product']['default_variant']['price']
                promotionPrice = price['selling_price']
                orgPrice = price['rrp_price']

                if price['is_promotion']:
                    promotionPercent = str(round(100 - promotionPrice / orgPrice * 100)) + '%'
                    sendMessage(f"تخفیف خورد!!!! 😎\n\n🎉 درصد تخفیف: {promotionPercent}\n\n💰 قیمت اصلی: {format_currency(orgPrice, currency_code='IRR')}\n\n🧨 قیمت جدید: {format_currency(promotionPrice, currency_code='IRR')}")
                else:
                    sendMessage("فعلا خبری نیست!")
            else:
                sendMessage("اوه! انگاری یه مشکلی هست که باس چکش کنی!")
        else:
            sendMessage("اوه! انگاری یه مشکلی هست که باس چکش کنی!")
    
    print('Working...')
    time.sleep(checkPeriod * 60)