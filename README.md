# whiplash dot net reviews web-scraping

It's a web-scraping script for whiplash.net that extract the latest albums reviews from it and generates a RSS feed file containing those reviews' link.

Some work is needed to ensure that every generated feed file is ready to be properly consumed by a feed reader. However, it's functional.

## Installation

Make sure that you have **Python 3.x.x*** and **pipenv** installed in your machine. Then, just clone it and configure pipenv to work with this repository.

With all preparations done, you can execute [scrap.py](scrap.py).

## Usage

Just executing it will generate a RSS feed file in .whiplash folder (which will be created in $HOME). You can pass a custom path through an argument.
```sh
./scrap.py
./scrap.py /path/to/feed.xml
```

## License

[MIT](LICENSE)
