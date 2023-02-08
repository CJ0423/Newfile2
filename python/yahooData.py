import requests
from bs4 import BeautifulSoup
import pandas as pd

headers = {
    'content-type': 'text/html; charset=UTF-8',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
}

def list_stock(input_type):
    whoIsbuy ={
        # 外資買超
        'investment': 'https://tw.stock.yahoo.com/rank/foreign-investor-buy?exchange=TWO'
    }
    getdata = requests.get(
        whoIsbuy[input_type],
        headers=headers
    )
    # print(getdata.encoding) #utf-8

    soup = BeautifulSoup(
        getdata.content,
        'html.parser',
        from_encoding='utf-8'
    ).find('ul', class_='M(0) P(0) List(n)')

    datalist = []
    for col in soup.find_all_next('li'):
        data = [row.text for row in col.find_all('div', class_='Lh(20px) Fw(600) Fz(16px) Ell')]
    if len(data) > 0:
        datalist.append(data)


    title = ["股票名稱"]

    df = pd.DataFrame(datalist[0:], columns=title)
    print(df)
    df.to_csv('{}_list.csv'.format(input_type), index=False)


list_stock('investment')
