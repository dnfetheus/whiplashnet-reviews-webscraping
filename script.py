import requests
from bs4 import BeautifulSoup
import json
import re
import logging
from feedgen.feed import FeedGenerator

SITE_URL = 'https://whiplash.net/indices/cds.html'
ARTICLES_JSON = 'articles.json'


def obtain_latest_articles() -> list:
    logging.info(f'Requesting content to {SITE_URL}')
    req = requests.get(SITE_URL)

    logging.info('Parsing content')
    soup = BeautifulSoup(req.text, 'lxml')
    content = soup.find(id='conteudo1')
    title = content.find('h3')
    articles = []

    for elem in title.next_siblings:
        if elem.name == 'p':
            article_link = elem.a['href']
            file = re.search(r'\d*-.*\.html', article_link).group()
            article_id = re.match(r'\d*', file).group()
            article = {'id': article_id, 'title': elem.a.get_text(), 'link': article_link}
            articles.append(article)
        else:
            break

    logging.info('Parsing complete')

    return articles


def persist_articles(articles: list) -> None:
    articles_from_file = []
    articles_to_append = []

    try:
        logging.info('Opening stored articles')
        file = open(ARTICLES_JSON, 'r')

        with file:
            articles_from_file = json.load(file)

            for article in articles:
                exists = False

                for f_article in articles_from_file:
                    if f_article['id'] == article['id']:
                        exists = True
                        break

                if not exists:
                    articles_to_append(article)

    except OSError:
        logging.warning('Wasn\'t able to find stored articles')
        articles_to_append.extend(articles)

    articles_from_file.extend(articles_to_append)
    logging.info('Storing articles')

    with open(ARTICLES_JSON, 'w') as file:
        json.dump(articles_from_file, file, indent=2)

    logging.info('Storing complete')


def generate_feed() -> None:
    return


def main():
    articles = obtain_latest_articles()
    persist_articles(articles)
    generate_feed()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()
