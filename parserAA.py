import requests
from bs4 import BeautifulSoup as bs
import csv

headers = {"accept": "*/*",
           "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0"}
# base_url = f'https://www.yelp.com/biz/american-airlines-irving?start={i}'


def aa_pars(headers):
    """
    Функция, которая получает комментарии от american airlines irving
    """
    comments = []
    session = requests.Session()
    i = 0
    while True:
        try:
            url = f'https://www.yelp.com/biz/american-airlines-irving?start={i}'
            request = session.get(url, headers=headers)
            if request.status_code == 200:
                soup = bs(request.content, 'lxml')
                divs = soup.find_all('div', attrs={'class': 'review review--with-sidebar'})
                if len(divs) == 0:
                    return comments
                for div in divs:
                    name = div.find('a', attrs={'id': 'dropdown_user-name',
                                                'class': 'user-display-name js-analytics-click'}).text
                    date = div.find('span', attrs={'class': 'rating-qualifier'}).text.replace('\n', '')
                    text = div.find('p', attrs={'lang': 'en'}).text
                    find_stars = div.find('img', attrs={'src': 'https://s3-media2.fl.yelpcdn.com/assets/srv0/yelp_design_web/9bec2045845c/assets/img/stars/stars.png'})
                    stars = find_stars.attrs['alt'][:3]
                    comments.append({
                        'name': name,
                        'stars': stars,
                        'date': date,
                        'text': text
                    })
                i += 20
            else:
                print(request.status_code)
        except:
            return comments


def file_writer(comments):
    """Функция добавления комментариев в csv файл"""
    with open('parser_AA.csv', 'w', encoding='utf-8') as file:
        pen = csv.writer(file)
        pen.writerow(('Name', 'Stars', 'Date', 'text'))
        for comment in comments:
            pen.writerow((comment['name'], comment['stars'], comment['date'], comment['text']))


comments = aa_pars(headers)
file_writer(comments)
