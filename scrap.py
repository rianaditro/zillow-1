from bs4 import BeautifulSoup
from requests_html import HTMLSession


import json


def get_profile_urls(base_url):
    result = dict()

    headers = {"User-Agent":"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36"}
    session = HTMLSession()

    for i in range(1,26):
        r = session.get(f"{base_url}{i}",headers=headers)
        r.html.render()
        table = r.html.find("table", first=True)
        url = table.absolute_links
        print(f"getting page {i} response:{r.status_code} add {len(url)} of urls")
        
        result[i]=url

    return result

def get_profile(url):
    headers = {"User-Agent":"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36"}
    r = HTMLSession().get(url,headers=headers)
    r.html.render(timeout=32)
    html = r.html.find("script#__NEXT_DATA__",first=True).text
    return html


if __name__=="__main__":
    real_estate_agent_url = "https://www.zillow.com/professionals/real-estate-agent-reviews/chatham-nj/?page="

    profile_url = "https://www.zillow.com/profile/Charles-Vogel/#reviews"

    j = get_profile(profile_url)
    j = json.loads(j)
    prof_information = j.get("props").get("pageProps").get("professionalInformation")
    print(prof_information)

"""
[
    {'term': 'Broker address', 
    'lines': ['Weichert Realtors', '474 Morris Avenue', 'Summit, NJ 07901']}, 
    {'term': 'Cell phone', 
    'description': '(908) 447-1291'}, 
    {'term': 'Websites', 
    'links': [{'text': 'Website', 'url': 'http://www.homesbyvogel.com'}]}, 
    {'term': 'Screenname', 
    'description': 'Charles Vogel'}, 
    {'term': 'Member since', 
    'description': '02/17/2012'}, 
    {'term': 'Real Estate Licenses', 
    'description': 'Not provided'}]
"""
