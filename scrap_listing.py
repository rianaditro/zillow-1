"""
this scraping flow is :
from encodedZuid : X1-ZUza7jt9n9hzwp_5gnlt (you get this from every broker profile)
you go to :
https://www.zillow.com/profile-page/api/public/v1/map-results?encodedZuid=X1-ZUza7jt9n9hzwp_5gnlt

there are list like this :
[{"lat":40.85839,"long":-74.1519,"statusType":"SOLD","zpid":39726607},
{"lat":40.97063,"long":-74.31918,"statusType":"SOLD","zpid":2055704942},
{"lat":40.94351,"long":-74.21878,"statusType":"SOLD","zpid":39791397}]

grab the zpid then go to :
https://www.zillow.com/homedetails/63738098_zpid/

its redirected to :
https://www.zillow.com/homedetails/263-Boulevard-Pompton-Plains-NJ-07444/63738098_zpid/

Happy Scraping
"""

from scrap_broker import get_html, get_data

import json
import concurrent.futures
import pandas


def get_house_urls(text):
    list_of_dict = convert_to_dicts(text)
    zpid_list = [f'https://www.zillow.com/homedetails/{item["zpid"]}_zpid' for item in list_of_dict if item["statusType"]=="FOR_SALE" or item["statusType"]=="FOR_RENT"]
    return tuple(zpid_list)

def convert_to_dicts(text):
     text = text.replace("<html><head></head><body>[","").replace("]</body></html>","").replace("},","}},").split("},")
     result = [json.loads(item) for item in text]
     return result

def parse_home_details(url)->dict:
     text = get_data(url)["props"]["pageProps"]["componentProps"]["gdpClientCache"]
     dict_text = json.loads(text)

     result = {
          "zpid":"",
          "homeStatus":"",
          "price":"",
          "homeType":"",
          "streetAddress":"",
          "city":"",
          "state":"",
          "zipcode":"",
          "latitude":"",
          "longitude":"",
          "bedrooms":"",
          "bathrooms":"",
          "yearBuilt":"",
          "pageViewCount":"",
          "favoriteCount":"",
          "daysOnZillow":"",
          "hdpUrl":"",
          "agentName":"",
          "agentPhoneNumber":"",
          "brokerName":"",
          "brokerPhoneNumber":"",
          "lastUpdated":""
     }
     dict_text = list(dict_text.items())[0][1]["property"]

     get_only = ["zpid","city","state","homeStatus","bedrooms","bathrooms","price","yearBuilt","streetAddress","zipcode","hdpUrl","homeType","pageViewCount","favoriteCount","daysOnZillow","latitude","longitude","attributionInfo"]
     
     dict_keys = [item for item in dict_text.keys() if item in get_only]
     #dict_value = [dict_text[item] for item in get_only if item in dict_text]
     for i in range(len(dict_keys)):
          result[dict_keys[i]] = dict_text[dict_keys[i]]

          if dict_keys[i] == "attributionInfo":
               get_only_sub = ["agentName","agentPhoneNumber","brokerName","brokerPhoneNumber","lastUpdated"]
               dict_keys_sub = [item for item in result["attributionInfo"].keys() if item in get_only_sub if item in result["attributionInfo"]]
               for i in range(len(dict_keys_sub)):
                    result[dict_keys_sub[i]] = result["attributionInfo"][dict_keys_sub[i]]
               del result["attributionInfo"]
     print(result)
     return result

def get_zpid_from_map(encodedZuid):
    url = f"https://www.zillow.com/profile-page/api/public/v1/map-results?encodedZuid={encodedZuid}"    
    html = get_html(url)
    list_of_house_urls = get_house_urls(html)
    print(f"from {encodedZuid} found for-sale/rent: {len(list_of_house_urls)} houses ")
    return tuple(list_of_house_urls)

def encodedZuid_to_home_details(encodedZuid):
    list_of_house_urls = get_zpid_from_map(encodedZuid)
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
          home_details = executor.map(parse_home_details,list_of_house_urls)
          df = pandas.DataFrame(home_details)
    return df
          

if __name__=="__main__":
     h = encodedZuid_to_home_details("X1-ZUu63jgpzv25u1_2avjk")
     h.to_excel("house_listings.xlsx",index=False)
     
