import requests
from bs4 import BeautifulSoup
import json
import gevent
import random

useragents = ['Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.3; WOW64; Trident/7.0; .NET4.0E; .NET4.0C; InfoPath.3; MS-RTC LM 8)',
'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)',
'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)',
'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'
]
useragents_len = len(useragents)


def download_user(url):
    useragent = useragents[random.randint(0, useragents_len-1)]
    headers = {'User-Agent': useragent}
    try:
        response = requests.get(url, headers = headers)
    except Exception as e:
        print 'error, will sleep 100 seconds.......'
        print e
        gevent.sleep(100)
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

