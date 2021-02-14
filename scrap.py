import sys
import requests
import re
import logging as logger
from itertools import takewhile
from pathlib import Path

from bs4 import BeautifulSoup

from feedgen.feed import FeedGenerator


CONTENT_URL = 'https://whiplash.net/indices/cds.html'

DEFAULT_SCRAPING_FOLDER_PATH = f'{Path.home()}/.whiplash'
DEFAULT_FEED_FILE_PATH = f'{DEFAULT_SCRAPING_FOLDER_PATH}/feed.xml'


def get_arguments() -> dict:
    logger.info('Validating arguments')

    args = {
        'output_file_path': sys.argv[1] if len(sys.argv) >= 2 else DEFAULT_FEED_FILE_PATH
    }

    return args


def get_article(elem) -> dict:
    article_link = elem.a['href']
    file = re.search(r'\d*-.*\.html', article_link).group()
    article_id = re.match(r'\d*', file).group()

    article = {
        'id': article_id,
        'title': elem.a.get_text(),
        'link': article_link
    }

    return article


def obtain_latest_articles() -> iter:
    logger.info(f'Requesting content to {CONTENT_URL}')

    req = requests.get(CONTENT_URL)

    logger.info('Parsing content')

    soup = BeautifulSoup(req.text, 'lxml')
    content = soup.find(id='conteudo1')
    title = content.find('h3')

    required_elements = takewhile(lambda elem: elem.name == 'p', title.next_siblings)
    articles = map(get_article, required_elements)

    return articles


def generate_feed(articles: iter, args: dict) -> None:
    logger.info('Generating feed file')

    fg = FeedGenerator()
    fg.author({'name': 'Whiplash', 'email': 'jpwhiplash@gmail.com'})
    fg.description('Feed não oficial de resenhas do Whiplash')
    fg.title('Resenhas - Whiplash')
    fg.logo('https://whiplash.net/favicon-32x32.png')
    fg.link(href=CONTENT_URL, rel='self')

    for article in articles:
        fe = fg.add_entry()
        fe.title(article['title'])
        fe.link(href=article['link'])

    if len(sys.argv) < 2:
        Path(DEFAULT_SCRAPING_FOLDER_PATH).mkdir(exist_ok=True)
    
    fg.rss_file(args['output_file_path'], pretty=True)

    logger.info('Feed file has been generated successfully')


def main():
    args = get_arguments()
    articles = obtain_latest_articles()
    generate_feed(articles, args)


if __name__ == '__main__':
    logger.basicConfig(level=logger.INFO)
    main()
