import requests
from bs4 import BeautifulSoup
import wen_sun.data_csv as data_csv
import wen_sun.get_recipe_info as get_recipe_info
import urllib
import random
import re
import sys
import time

recipe_detail_list = []
URL = "https://www.chefkoch.de/rezepte/kategorien/"


def setup(url):
    headers = {'user-agent': 'Mozilla/5.0'}
    html = requests.get(url, headers=headers)
    if html.status_code == 200:
        soup = BeautifulSoup(html.text, 'html.parser')
    return (soup)

def parse_html(url):
    soup = setup(url)
    # 页面跳转
    link = soup.find('div', {'class', 'category-column'}).find('h2').find('a')['href']
    subpage = "https://www.chefkoch.de" + link
    soup_cat = setup(subpage)

    for i in range(1, 2):
        page = soup_cat.find('ul', {'class', 'ds-pagination'})
        for li in page.find_all('li'):
            link_a = li.find('a', {'class', 'ds-page-link bi-paging-jump'})
            if link_a != None:
                link = link_a['href']
                soup_recipe = setup(link)
                for article in soup_recipe.find_all('article', {'class', 'rsel-item ds-grid-float ds-col-12 ds-col-m-8'}):
                    new_url = article.find('a')['href']
                    # detail_soup = setup(new_url)
                    get_recipe_info(new_url)
                    break


# def categorien_name(url):
#     cat_name = []
#     r = requests.get(url, headers=headers)
#     if r.status_code == 200:
#         soup = BeautifulSoup(r.content, "html.parser")
#     cat_name = soup.find('h2', {'class', 'category-level-1'}).get_text()
#     return (cat_name)


# def get_recipe_info(recipe):
#     content = {
#         "categorien": [],
#         "recipe_name": [],  # *
#         "avg_score": [],  # *
#         "difficulty": [],  # *
#         "rating_count": [],  # *
#         "pre_time": [],  # *
#         "calorie": [],
#         "comment_user": [],
#         "recipe_url": []  # *
#     }
#
#     soup = setup(recipe)
#     # cat_name = soup.find('span',{'itemprop':'name'}).get_text()
#     # # print(cat_name)
#     # content['categorien'] = cat_name
#     # crawl the name of recipes
#     recipe_name = soup.find('h1').get_text()
#     content['recipe_name'] = recipe_name
#
#     # crawl the average score of recipes
#     rating1 = soup.find('div', {"class": "ds-rating-avg"})
#     avg_score = rating1.find('strong').get_text()
#     content['avg_score'] = avg_score
#
#     # crawl the number of users, who make evaluation
#     rating2 = soup.find('div', {"class": "ds-rating-count"})
#     rating_count = rating2.find('strong').get_text()
#     content['rating_count'] = rating_count
#
#     # crawl the prepare time of recipe
#     t = soup.find('span', {"class": "recipe-preptime"}).get_text()
#     pre_time = re.findall('[A-Za-z0-9]', t)
#     pre_time = ''.join(pre_time)
#     content['pre_time'] = pre_time
#
#     # difficulty of recipe
#     diff = soup.find('span', {"class": "recipe-difficulty"}).get_text()
#     difficulty = re.findall('[A-Za-z0-9]', diff)
#     difficulty = ''.join(difficulty)
#     content['difficulty'] = difficulty
#
#     # get the url of all the recipes
#     content['recipe_url'] = recipe
#
#     print(content)
#
#     recipe_detail_list.append(content)
#     return (recipe_detail_list)



# crawl all the recipe in the first categorien in several pages


if __name__ == "__main__":
    parse_html(URL)
    data_csv.writeCSV(recipe_detail_list)