import requests
from bs4 import BeautifulSoup
import json
import re
import logging
from feedgen.feed import FeedGenerator


SITE_URL = 'https://whiplash.net/indices/cds.html'
ARTICLES_FILE = 'articles.json'
FEED_FILE = 'feed.xml'


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

    logging.info('Parsed successfully')

    return articles


def persist_articles(articles: list) -> None:
    articles_from_file = []
    articles_to_append = []

    try:
        logging.info('Opening stored articles')
        file = open(ARTICLES_FILE, 'r')

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

    with open(ARTICLES_FILE, 'w') as file:
        json.dump(articles_from_file, file, indent=2)

    logging.info('Articles had been stored successfully')


def generate_feed() -> None:
    logging.info('Generating feed')
    fg = FeedGenerator()

    fg.author({'name': 'Whiplash', 'email': 'jpwhiplash@gmail.com'})
    fg.description('Feed de resenhas do Whiplash')
    fg.title('Resenhas - Whiplash')
    fg.logo('https://whiplash.net/favicon-32x32.png')
    fg.link(href=SITE_URL, rel='self')

    with open(ARTICLES_FILE, 'r') as file:
        # FIXME: load in order
        articles = json.load(file)

        for article in articles:
            fe = fg.add_entry()
            fe.title(article['title'])
            fe.link(href=article['link'])

    fg.rss_file(FEED_FILE, pretty=True)

    logging.info('Generation completed')


def main():
    articles = obtain_latest_articles()
    persist_articles(articles)
    generate_feed()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()
