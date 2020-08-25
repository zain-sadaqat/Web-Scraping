import urllib
from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
from urllib.parse import quote_plus, quote
from . import models

# BASE_URL_ = 'https://www.olx.com.pk/'
# BASE_URL_ = 'https://www.amazon.com/'
# BASE_URL_ = 'https://www.udemy.com/'

BASE_URL_ = 'https://newyork.craigslist.org/search/bbb?query={}'
BASE_IMAGE_URL = 'https://images.craigslist.org/{}_300x300.jpg'


def home(request):
    return render(request, 'base.html')

def search(request):
    search = request.POST.get('search')      # .get is a dictionary method to get data
    models.Search.objects.create(search=search)     #storing searches in database
    base_url = BASE_URL_ + (urllib.parse.quote(str(search)))
    response = requests.get(base_url)    # for library we use requests plural
    data = response.text
    soup = BeautifulSoup(data, features='html.parser')

    post_listings = soup.find_all('li', {'class': 'result-row'})
    final_postings = []

    for post in post_listings:
        post_title = post.find(class_="result-title").text
        post_url = post.find('a').get('href')
        if post.find(class_="result-price"):
            post_price = post.find(class_="result-price").text
        else:
            post_price = 'N/A'

        if post.find(class_='result-image').get('data-ids'):
            post_image_id = post.find(class_='result-image').get('data-ids').split(',')[0].split(':')[1]
            post_image_url = BASE_IMAGE_URL.format(post_image_id)
        else:
            post_image_url = 'https://craigslist.org/images/peace.png'
        final_postings.append((post_title, post_url, post_price, post_image_url))
    context = {
        'search': search,
        'final_postings': final_postings,
    }
    return render(request, 'web_scraping/search.html', context)