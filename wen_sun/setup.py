
import requests
from bs4 import BeautifulSoup


def setup(url):
    headers = {'user-agent': 'Mozilla/5.0'}
    html = requests.get(url, headers=headers)
    if html.status_code == 200:
        soup = BeautifulSoup(html.text, 'html.parser')
    return (soup)