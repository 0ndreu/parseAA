import requests
from bs4 import BeautifulSoup as bs
import lxml

headers = {"accept": "*/*",
           "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0"}

base_url = 'https://www.yelp.com/biz/american-airlines-irving?start=0'


def aa_pars(base_url, headers):
    """
    Функция, которая получает комментарии от american airlines irving
    """
    comments = []
    session = requests.Session()
    request = session.get(base_url, headers=headers)
    if request.status_code == 200:
        soup = bs(request.content, 'lxml')
        divs = soup.find_all('div', attrs={'class': 'review review--with-sidebar'})
        for div in divs:
            name = div.find('a', attrs={'id': 'dropdown_user-name',
                                        'class': 'user-display-name js-analytics-click'}).text
            date = div.find('span', attrs={'class': 'rating-qualifier'}).text.replace('\n', '')
            text = div.find('p', attrs={'lang': 'en'}).text     # Доделать, чтобы выводилось с \n
            find_stars = div.find('img', attrs={'src': 'https://s3-media2.fl.yelpcdn.com/assets/srv0/yelp_design_web/9bec2045845c/assets/img/stars/stars.png'})
            stars = find_stars.attrs['alt'][:3]
            comments.append({
                'name': name,
                'stars': stars,
                'date': date,
                'text': text
            })
    else:
        print(request.status_code)


aa_pars(base_url, headers)

