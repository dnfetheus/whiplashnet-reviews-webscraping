import requests
from bs4 import BeautifulSoup


class Article:
    def __init__(self, title, link):
        self.title = title
        self.link = link

    def __str__(self):
        return f'{self.title}: {self.link}'


def main():
    whiplash_url = 'https://whiplash.net/indices/cds.html'

    req = requests.get(whiplash_url)
    soup = BeautifulSoup(req.text, 'lxml')
    conteudo = soup.find(id='conteudo1')
    title = conteudo.find('h3')
    articles = []

    for elem in title.next_siblings:
        if elem.name == 'p':
            article = Article(elem.a.get_text(), elem.a['href'])
            articles.append(article)
        else:
            break


if __name__ == '__main__':
    main()
