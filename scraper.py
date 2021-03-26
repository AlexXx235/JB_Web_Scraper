import requests
import string
import os
import re
from bs4 import BeautifulSoup


def process_name(name):
    translate_table = str.maketrans('', '', string.punctuation + '’')
    return name.strip().translate(translate_table).replace(' ', '_')


def process_page(page_url, params, article_category):
    url_prefix = 'https://www.nature.com'
    respond = requests.get(page_url, params=params)
    if respond:
        page = BeautifulSoup(respond.content, 'html.parser')
        articles = [article for article
                    in page.find_all('article')
                    if article.find('span',
                                    class_='c-meta__type',
                                    recursive=True).text == article_category]
        urls = {}
        for article in articles:
            link = article.find('a')
            name = process_name(link.text)
            url = link.get('href')
            urls[name] = url_prefix + url
        return urls
    else:
        print('Incorrect page url!')
        exit(1)


def save_article(name, text):
    file = open(name + '.txt', 'wb')
    file.write(text.encode())
    file.close()


def process_article(url):
    response = requests.get(url)
    if response:
        article = BeautifulSoup(response.content, 'html.parser')
        body = article.find('div', class_=re.compile('__body'))
        if body is None:
            print('Article has not body!')
            exit(3)
        return body.text.strip()
    else:
        print('Incorrect article url!')
        exit(2)
    return '', ''


if __name__ == '__main__':
    master_url = 'https://www.nature.com/nature/articles'

    pages_number = int(input())
    category = input()

    for current_page in range(1, pages_number + 1):
        article_urls = process_page(master_url, {'page': f'{current_page}'}, category)
        for name, url in article_urls.items():
            print(name, url)
        directory_name = f'Page_{current_page}'
        try:
            os.mkdir(directory_name)
        except FileExistsError:
            pass
        os.chdir(directory_name)
        for article_name, article_url in article_urls.items():
            article_text = process_article(article_url)
            save_article(article_name, article_text)
        os.chdir('../')

    print('Saved all articles.')
