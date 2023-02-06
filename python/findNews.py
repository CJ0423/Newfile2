import requests
from bs4 import BeautifulSoup
import pandas as pd

headers = {
    'content-type': 'text/html; charset=UTF-8',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
}

def findBook(input_type):
    list_book = {
        'book': 'https://www.books.com.tw/web/sys_tdrntb/books/'
    }
    getdata = requests.get(
        list_book[input_type],
        headers=headers
    )
    # print(getdata.encoding) utf-8
    soup = BeautifulSoup(
        getdata.content,
        'html.parser',
        from_encoding='utf-8'
    )

    datalist = []

    for a in soup.find_all('a', {'class': 'text_brown'}):
        book_name = a.find('img')['alt']
        author = a.text.strip().replace(book_name, '').strip()
        datalist.append([book_name, author])

    title = [
        '書名',
        '作者',
    ]

    df = pd.DataFrame(datalist[0:], columns=title)
    print(df)

    df.to_csv('{}_list.csv'.format(input_type), index=False)

findBook('book')