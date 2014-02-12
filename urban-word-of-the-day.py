#!/usr/bin/env python

import json
import urllib2

from flask import Flask

from bs4 import BeautifulSoup

APP = Flask(__name__)
URL = 'http://www.urbandictionary.com'

def get_wod(day=0):
    if day > 6:
        raise LookupError('Words of the day older than one week from today are not available.')

    content = urllib2.urlopen(URL).read()
    soup = BeautifulSoup(content)
    words = []
    meanings = []

    for div in soup.findAll('div', attrs={'class': 'word'}):
        words.append(div.text.strip())

    for div in soup.findAll('div', attrs={'class': 'meaning'}):
        meanings.append(div.text.strip())

    return zip(words, meanings)[day]


def jsonize_wod(wod):
    return json.dumps({ 'word': wod[0], 'meaning': wod[1] })


@APP.route('/')
@APP.route('/today')
def today():
    return jsonize_wod(get_wod(0))


@APP.route('/yesterday')
def yesterday():
    return jsonize_wod(get_wod(1))


if __name__ == '__main__':
    APP.run(debug=True)
