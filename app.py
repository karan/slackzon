# -*- coding: utf-8 -*-

import os

from bs4 import BeautifulSoup
from flask import Flask, request, Response, redirect
import bottlenose

try:
    import config
    AWS_ACCESS_KEY_ID = config.aws['AWS_ACCESS_KEY_ID']
    AWS_SECRET_ACCESS_KEY = config.aws['AWS_SECRET_ACCESS_KEY']
    AWS_ASSOCIATE_TAG = config.aws['AWS_ASSOCIATE_TAG']
except:
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    AWS_ASSOCIATE_TAG = os.environ.get('AWS_ASSOCIATE_TAG')


if not all([AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_ASSOCIATE_TAG]):
    import sys
    print 'No config.py file found. Exiting...'
    sys.exit(0)


MAX_PRODUCTS = 5


app = Flask(__name__)
amazon_client = bottlenose.Amazon(AWS_ACCESS_KEY_ID,
                           AWS_SECRET_ACCESS_KEY,
                           AWS_ASSOCIATE_TAG,
                           Parser=BeautifulSoup)


def get_response_string(item_xml):
    try:
        item = amazon_client.ItemLookup(ItemId=item_xml.asin.string,
                                        ResponseGroup='Offers',
                                        MerchantId='All')
        price = item.find('formattedprice').string
        url = item_xml.detailpageurl.string
        title = item_xml.itemattributes.title.string
        manufacturer = item_xml.itemattributes.manufacturer.string
        return "*%s* <%s|%s> (by %s)" % (price, url, title, manufacturer)
    except:
        return ''


@app.route('/search', methods=['post'])
def search():
    '''
    Example:
        /amazon kindle 3g
    '''
    text = request.values.get('text')

    try:
        xml = amazon_client.ItemSearch(Keywords=text, SearchIndex='All')
    except UnicodeEncodeError:
        return Response(('Only English language is supported. '
                         '%s is not valid input.' % text),
                         content_type='text/plain; charset=utf-8')


    resp = [('Amazon Top Products for '
             '"<%s|%s>"\n') % (xml.items.moresearchresultsurl.string, text)]
    products = xml.find_all('item')[:MAX_PRODUCTS]
    resp.extend(map(get_response_string, products))

    if len(resp) is 1:
        resp.append(('No products found. Please try a broader search or '
                     'search directly on '
                     '<https://amazon.goel.io/amazon|Amazon>.'))

    return Response('\n'.join(resp), content_type='text/plain; charset=utf-8')


@app.route('/amazon')
def amazon():
    return redirect('http://amzn.to/1Gjm2pk', code=302)


@app.route('/')
def hello():
    return redirect('https://github.com/karan/slackzon')


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
