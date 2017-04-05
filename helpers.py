'''
Helper functions for interacting with the wikipedia API
'''

import requests
import json
from bs4 import BeautifulSoup


def get_random_page(baseurl='https://en.wikipedia.org/api/rest_v1'):
    '''
    Retrieve the title of a random article via HTTP

    arguments:
        baseurl:str

    returns:
        title:str
    '''
    url = baseurl + '/page/random/title'
    headers = {'Accept': 'application/json'}

    response = requests.get(url, headers=headers)
    res_json = response.json()

    return str(res_json['items'][0]['title'])

def get_page_revision(title, baseurl='https://en.wikipedia.org/api/rest_v1'):
    '''
    Retrieve the latest revision of a given article

    arguments:
        title:str
        baseurl:str

    returns:
        revision:str
    '''
    url = baseurl + '/page/html/%s/' % title
    headers = {'Accept': 'application/json'}

    response = requests.get(url, headers=headers)
    res_json = response.json()

    return str(res_json['items'][0]['revision'])

def get_page_html(title, baseurl='https://en.wikipedia.org/api/rest_v1'):
    '''
    Retrieve the HTML contents of an article with the given title

    arguments:
        title:str
        baseurl:str

    returns:
        content:str
    '''
    url = baseurl + '/page/html/%s' % title
    headers = {
        'Accept': 'text/html; charset=utf-8; profile="https://www.mediawiki.org/wiki/Specs/HTML/1.3.0"'
    }

    response = requests.get(url, headers=headers)
    return str(response.text)

def get_link(content):
    '''
    Parse the HTML content of an article, looking for the first valid link.
    Valid links are in the main text body of the article, are not citations,
    and are not surrounded by parentheses.

    Keeps a running total of unclosed parentheses.

    Returns None if none are found.

    arguments:
        content:str

    returns:
        title:str | None
    '''

    soup = BeautifulSoup(content, 'lxml')
    parens = 0

    for p in soup.body:
        if p.name != 'p':
            continue
        for item in p.children:
            if isinstance(item, str):
                parens += (item.count('(') - item.count(')'))
                parens = parens if parens >= 0 else 0

            elif item.name == 'a' and parens == 0 and item['rel'][0] == 'mw:WikiLink':
                return item['href'].lstrip('./').split('#')[0]
    return None
