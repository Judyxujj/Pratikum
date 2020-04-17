import requests
from bs4 import BeautifulSoup
import re


# extract user link
def get_comment_user(url):

    comment_user = []

    # request the website of rating list
    r = requests.get(url)

    if r.status_code == 200:
        soup: BeautifulSoup = BeautifulSoup(r.content, "html.parser")

        # get the voting table
        table = soup.find('table', {"class": "voting-table"})
        rows = table.findAll('tr')
        for row in rows[1:]:
            # use a dictionary to store the information of every user
            dict = { }

            # get the name of the user
            name = row.findAll('a')
            if len(name) > 1:

                # get the rating of the user
                rating = row.find('span', {"class": "rating-small"})
                rating = rating.findChild()
                rating = rating['class'][1]
                dict['rating'] = rating

                dict['name'] = name[0].get_text()
                profile_url = 'https://www.chefkoch.de' + name[0]['href']

                # get the age, sex of the user
                w = requests.get(profile_url)

                if w.status_code == 200:
                    soup2: BeautifulSoup = BeautifulSoup(w.content, "html.parser")
                    table = soup2.find('table', {"id": "user-details"})

                    # get the sex of user
                    img = table.findAll('img')
                    if img:
                        dict['sex'] = img[0]['alt']
                    else:
                        dict['sex'] = 'None'

                    # get the age of user
                    age = table.find('td', {"class": 'nobr'}).find_next('td').text.strip()
                    if age:
                        dict['age'] = age
                    else:
                        dict['age'] = 'None'

                    # get the marriage status of user
                    marriage_status = table.find('strong', text='Beziehungsstatus:')
                    if marriage_status:
                        marriage_status = marriage_status.find_next('td').text.strip()
                        dict['marriage_status'] = marriage_status
                    else:
                        dict['marriage_status'] = 'None'

                    # get the job of user
                    job = table.find('strong', text='Beruf:')
                    if job:
                        job = job.find_next('td').text.strip()
                        if job != 'n/a':
                            dict['job'] = job
                        else:
                            dict['job'] = 'None'

                    # if the dict contains 4 'None' then we do not append it
                    keys = list(dict.values())
                    if keys.count('None') < 4:
                        comment_user.append(dict)

    return comment_user


# extract useful information form the website
def get_recipe_info(categorize, url):
    # define a dictionary to store the information
    content: dict = {
        "categorize": [],
        "recipe_name": [],
        "tags": [],
        "avg_score": [],
        "difficulty": [],
        "ingredient": [],
        "rating_count": [],
        "calorie": [],
        "preparation_time": [],
        "comment_user": [],
        "recipe_url": [],
    }

    # categorize is hide in url
    categorize = categorize
    recipe_url = url

    r = requests.get(url)

    if r.status_code == 200:
        soup: BeautifulSoup = BeautifulSoup(r.content, "html.parser")

        # get recipe name
        recipe_name = soup.find('h1').get_text()

        # get the average score of recipes
        rating1 = soup.find('div', {"class": "ds-rating-avg"})
        avg_score = rating1.find('strong').get_text()

        # count the number of ratings
        rating2 = soup.find('div', {"class": "ds-rating-count"})
        rating_count = rating2.find('strong').get_text()

        # get the preparation time of recipe
        t = soup.find('span', {"class": "recipe-preptime"}).get_text()
        preparation_time = re.findall('[0-9]+[\s][A-Za-z]+', t)

        # get the difficulty of recipe
        diff = soup.find('span', {"class": "recipe-difficulty"}).get_text()
        difficulty = re.findall('[A-Za-z]+', diff)

        # get the calorie of the recipe
        try:
            caro = soup.find('span', {"class": "recipe-kcalories"}).get_text()
            calorie = re.findall('[A-Za-z0-9]', caro)
            calorie = ''.join(calorie)
        except:
            calorie = 'None'

        # get the ingredient of recipe
        table = soup.find('table', {"class": "ingredients table-header"})
        rows = table.findAll('span')
        ingredient = []
        for row in rows:
            row = row.get_text()
            row = row.strip().replace('\n', '')
            row = row.replace(" ", "")
            ingredient.append(row)

        # get tags of the recipe
        tags = []
        properties = soup.findAll('a', {"class":"ds-tag bi-tags"})
        for property in properties:
            tag = property.get_text()
            tag = tag.strip().replace('\n', '')
            tag = tag.replace(" ", "")
            tags.append(tag)

        # get the comment_user of the recipe
        try:
            rating_list = soup.find('span', {'class':"ds-from-m rat-show-action"})
            rating_list = rating_list.find('a')
            rating_url = rating_list['href']
            comment_user = get_comment_user(rating_url)

        except:
            comment_user = 'None'

        # write the data into dictionary
        content['categorize'] = categorize
        content['recipe_name'] = recipe_name
        content['tags'] = tags
        content['avg_score'] = avg_score
        content['difficulty'] = difficulty[0]
        content['ingredient'] = ingredient
        content['rating_count'] = rating_count
        content['calorie'] = calorie
        content['recipe_url'] = recipe_url
        content['preparation_time'] = preparation_time[0]
        content['comment_user'] = comment_user

    return content

