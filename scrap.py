import requests
import re
import logging as logger
from itertools import takewhile
from pathlib import Path

from bs4 import BeautifulSoup

from feedgen.feed import FeedGenerator


SITE_URL = 'https://whiplash.net/indices/cds.html'

SCRAPING_FOLDER = f'{Path.home()}/.whiplash'
FEED_FILE = f'{SCRAPING_FOLDER}/feed.xml'


def get_article(elem) -> dict:
    article_link = elem.a['href']
    file = re.search(r'\d*-.*\.html', article_link).group()
    article_id = re.match(r'\d*', file).group()
    article = {'id': article_id, 'title': elem.a.get_text(), 'link': article_link}

    return article


def obtain_latest_articles() -> list:
    logger.info(f'Requesting content to {SITE_URL}')

    req = requests.get(SITE_URL)

    logger.info('Parsing content')

    soup = BeautifulSoup(req.text, 'lxml')
    content = soup.find(id='conteudo1')
    title = content.find('h3')

    articles = list(map(get_article, takewhile(lambda elem: elem.name == 'p', title.next_siblings)))

    logger.info('Parsed successfully')

    return articles


def generate_feed(articles: list) -> None:
    logger.info('Generating feed')

    fg = FeedGenerator()
    fg.author({'name': 'Whiplash', 'email': 'jpwhiplash@gmail.com'})
    fg.description('Feed não oficial de resenhas do Whiplash')
    fg.title('Resenhas - Whiplash')
    fg.logo('https://whiplash.net/favicon-32x32.png')
    fg.link(href=SITE_URL, rel='self')

    for article in articles:
        fe = fg.add_entry()
        fe.title(article['title'])
        fe.link(href=article['link'])

    Path(SCRAPING_FOLDER).mkdir(exist_ok=True)
    fg.rss_file(FEED_FILE, pretty=True)

    logger.info('Generation completed')


def main():
    articles = obtain_latest_articles()
    generate_feed(articles)


if __name__ == '__main__':
    logger.basicConfig(level=logger.INFO)
    main()
