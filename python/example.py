import requests
from bs4 import BeautifulSoup
import pandas as pd


# 某些瀏覽器會偵測是不是爬蟲
# 需要特別設定header假扮自己是真人
headers = {
    'content-type': 'text/html; charset=UTF-8',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
}

# -------------  證券清單 -------------------
# 上市
def list_stock(input_type):
    # 將 上市與上櫃的區分成 dictionary的 value方便直接call來用
    list_stocks = {
        'exchange': 'https://isin.twse.com.tw/isin/C_public.jsp?strMode=2',
        'counter': 'https://isin.twse.com.tw/isin/C_public.jsp?strMode=4'
    }
    getdata = requests.get(
        list_stocks[input_type],
        headers=headers
    ) # 上櫃就換成 counter input_type=>counter這樣就可以找到了

    # 獲得網頁字型
    # 因為這個網頁的字型比較特殊
    # 故需要先取得字形
    # print(getdata.encoding)

    # 取得後發現字形為：'MS950'
    # 於是就用這個字形來解析網頁
    soup = BeautifulSoup(
        getdata.content,
        'html.parser',
        from_encoding='MS950'
    ).find('table', class_='h4')

    datalist = []
    for col in soup.find_all_next('tr'):
        datalist.append(
            [row.text for row in col.find_all('td')]
        )

    #對內部的資料進行處理
    for deal_str in datalist[1:]:
        if len(deal_str) == 7:
            last = deal_str[0].split('\u3000')[1]
            deal_str[0] = deal_str[0].split('\u3000')[0]
            deal_str.insert(1, last)
    #
    #設定好對應的標題名稱
    title = [
        '有價證券代號',
        '有價證券名稱',
        '國際證券辨識號碼(ISIN Code)',
        '上市日',
        '市場別',
        '產業別',
        'CFICode',
        '備註'
    ]
    #
    # # 轉成 pandas
    df = pd.DataFrame(datalist[1:], columns=title)
    print(df)
    #
    #存到 csv 大功告成！
    df.to_csv('{}_list.csv'.format(input_type), index=False)

# 上市
list_stock('exchange')

# 上櫃
list_stock('counter')
