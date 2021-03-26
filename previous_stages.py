import requests
import json
import string
from bs4 import BeautifulSoup


def first_stage():
    request = input('Input the URL: ')
    response = requests.get(request)
    if response:
        json_text = response.text
        text = json.loads(json_text)
        if 'content' in text:
            print(text['content'])
            exit(0)
    print('Invalid quote resource!')


def second_stage():
    request = input('Input the URL: ')
    response = requests.get(request, headers={'Accept-Language': 'en-US,en;q=0.5'})
    if response:
        # json_text = response.text
        # print(json_text)
        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.find('title').text
        if title.endswith('IMDb'):
            index = title.find('(')
            if index != -1:
                title = title[:index - 1]
        else:
            print('Invalid movie page!')
            return
        description_external = soup.find('div',
                                         class_='plot_summary',
                                         recursive=True)
        if description_external is None:
            print('Invalid movie page!')
            return
        else:
            description = description_external.find_next()
            if description is None:
                print('Invalid movie page!')
                return
        result = {'title': title,
                  'description': description.text.strip()}
        print(result)
    else:
        print('Invalid movie page!')


def third_stage():
    filename = 'source.html'
    request = input('Input the URL: ')
    respond = requests.get(request)
    if respond:
        file = open(filename, 'wb')
        file.write(respond.content)
        file.close()
        print('Content saved.')
    else:
        print(f'The URL returned {respond.status_code}!')


def fourth_stage():
    master_url = 'https://www.nature.com/nature/articles'
    url_prefix = 'https://www.nature.com'
    desired_type = 'News'
    main_page = requests.get(master_url)
    if not main_page:
        print('Bad url!')
        exit(1)
    soup = BeautifulSoup(main_page.content, 'html.parser')
    articles = soup.find_all('article')
    article_links = {}
    for article in articles:
        article_type = article.find('span', class_='c-meta__type', recursive=True)
        # print(article_type.text)
        if article_type.text == desired_type:
            article_link = article.find('a', recursive=True)
            article_name = article_link.text
            article_url = article_link.get('href')
            article_links[article_name] = url_prefix + article_url
    translate_table = str.maketrans('', '', string.punctuation + "’")
    for name, url in article_links.items():
        print(url)
        response = requests.get(url)
        if response:
            article_page = BeautifulSoup(response.content, 'html.parser')
            body = article_page.body.find('div', class_='article__body cleared')
            article_name = name.strip().translate(translate_table).replace(' ', '_')
            file = open(article_name.strip() + '.txt', 'wb')
            file.write(body.text.strip().encode())
            file.close()
            print(article_name, article_links[name])
