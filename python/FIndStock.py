import requests
from bs4 import BeautifulSoup
import pandas as pd

headers = {
    'content-type': 'text/html; charset=UTF-8',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
}

def list_stock(input_type):
    list_stocks = {
        'exchange': 'https://isin.twse.com.tw/isin/C_public.jsp?strMode=2',
        'counter': 'https://isin.twse.com.tw/isin/C_public.sup?strMode=4'
    }

getdata = requests.get(
    list_stocks[input_type],
    headers=headers
)

print(getdata.encoding) # 取得文字資訊

soup = BeautifulSoup(
    getdata.content,
    'html.parser',
    from_encoding='MS950'
).find('table',class_='h4')


