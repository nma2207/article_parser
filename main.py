#coding: utf-8

import sys
from parser import ArticleParser

if __name__ == "__main__":
    link = sys.argv[1]
    filename = sys.argv[2]
    article_parser = ArticleParser()
    article_parser.get_article(link, filename)