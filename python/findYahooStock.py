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
    ).find('div', class_='mod type02_m035 clearfix')

    datalist = []
    author = []

    for h4 in soup.find_all_next('h4'):
        datalist.extend(
            [row.text for row in h4.find_all('a')]
        )
    #
    # for ul in soup.find_all_next('ul', class_="msg"):
    #      author.extend(
    #          [row.text for row in ul.find_all('a')]
    #         )

    for ul in soup.find_all_next('ul', class_="msg"):
        author_row = [row.text for row in ul.find_all('a')]
        if len(author_row) == 0:
            author.append('')
        else:
            author.extend(author_row)

    title = [
        '書名']
    df = pd.DataFrame(datalist, columns=title)
    df['書名'] = pd.DataFrame(datalist)
    df['作者'] = pd.DataFrame(author)
    print(df)


    df.to_csv('{}_list.csv'.format(input_type), index=False)

findBook('book')
