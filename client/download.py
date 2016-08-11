import requests
from bs4 import BeautifulSoup
import json
import gevent

def download_user(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0'}
    try:
        response = requests.get(url, headers = headers)
    except:
        gevent.sleep(20)
        return None

    text = response.text

    try:
        soup = BeautifulSoup(text, 'html.parser')
        namehtml = soup.select("span.name")
        if namehtml == []:
            return None
        name = namehtml[0].string

        locationhtml = soup.select("span.location")
        if locationhtml == []:
            location = ''
        else:
            location = locationhtml[0]['title']

        businesshtml = soup.select("span.business")
        if businesshtml == []:
            business = ''
        else:
            business = businesshtml[0]['title']

        genderhtml = soup.select("span.gender")
        if genderhtml == []:
            gender = ''
        else:
            genstr = str(genderhtml[0])
            if genstr.find('female') != -1:
                gender = '0'
            else:
                gender = '1'
            
        employmenthtml = soup.select("span.employment")
        if employmenthtml == []:
            employment = ''
        else:
            employment = employmenthtml[0]['title']
        
        positionhtml = soup.select("span.position")
        if positionhtml == []:
            position = ''
        else:
            position = positionhtml[0]['title']

        educationhtml = soup.select("span.education")
        if educationhtml == []:
            education = ''
        else:
            education = educationhtml[0]['title']

        education_extrahtml = soup.select("span.education-extra")
        if education_extrahtml == []:
            education_extra = ''
        else:
            education_extra = education_extrahtml[0]['title']

        agreehtml = soup.select("span.zm-profile-header-user-agree > strong")
        if agreehtml == []:
            agree = '0'
        else:
            agree = agreehtml[0].get_text()

        thankshtml = soup.select("span.zm-profile-header-user-thanks > strong")
        if thankshtml == []:
            thanks = '0'
        else:
            thanks = thankshtml[0].get_text()

        profilehtml = soup.find_all('div', class_='profile-navbar clearfix')
        if profilehtml == []:
            asks = '0'
            answsers = '0'
            posts = '0'
            collections = '0'
            logs = '0'
        else:
            profilehtml = profilehtml[0]
            asks = profilehtml.select("a:nth-of-type(2) > .num")[0].get_text()
            answsers = profilehtml.select("a:nth-of-type(3) > .num")[0].get_text()
            posts = profilehtml.select("a:nth-of-type(4) > .num")[0].get_text()
            collections = profilehtml.select("a:nth-of-type(5) > .num")[0].get_text()
            logs = profilehtml.select("a:nth-of-type(6) > .num")[0].get_text()

        followinghtml = soup.find_all('div', class_='zm-profile-side-following zg-clear')
        if followinghtml == []:
            following = '0'
            follower = '0'
        else:
            followinghtml = followinghtml[0]
            following = followinghtml.select("strong")[0].get_text()
            follower = followinghtml.select("strong")[1].get_text()

        linkhtml = soup.find_all('a', class_='zm-profile-header-user-detail zg-link-litblue-normal')
        if linkhtml == []:
            return None
        linkhtml = linkhtml[0]
        link = linkhtml['href'][8:][:-5]

        item = [url[23:], link, name, location, business, gender, employment, position, education, education_extra,\
                agree, thanks, asks, answsers, posts, collections, logs, following, follower]
        
        return item
    except:
        gevent.sleep(2)
        print url
        return None

