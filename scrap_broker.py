from bs4 import BeautifulSoup

import concurrent.futures
import hrequests
import pandas
import json, time

def check_url(url_str):
    base_url = "https://www.zillow.com"
    if base_url not in url_str:
        url_str = f"{base_url}{url_str}"
    return url_str

def open(url)->str:
    url = check_url(url)
    with hrequests.BrowserSession(browser="firefox",mock_human=True) as session:
        request = session.get(url)
        print(f"getting {request.status_code} at {url}")
        # add non 200 handling here
        html = request.html.html
    return html

def get_data(url)->dict:
    # get data from tag script#__NEXT_DATA__
    html = open(url)
    soup = BeautifulSoup(html,"html.parser")
    next_data = soup.find("script",{"id":"__NEXT_DATA__"}).text
    data_dict = json.loads(next_data)
    return data_dict

def extract_urls_from_page(url_page)->tuple:
    data_dict = get_data(url_page)
    profile_urls = set()
    data_dict = data_dict["props"]["pageProps"]["proResults"]["results"]["professionals"]
    for data in data_dict:
        profile_urls.add(data["profileLink"])
    print(f"success extract {len(profile_urls)} of urls")
    return tuple(profile_urls)

def get_profile(url)->dict:
    profile_data = dict()
    data_dict = get_data(open(check_url(url)))
    # get name
    name = data_dict["props"]["pageProps"]["profileDisplay"]["name"]
    profile_data["name"] = name
    # get professional info
    professional_info = data_dict["props"]["pageProps"]["professionalInformation"]
    for info in professional_info:
        data = info.values()
        profile_data[data[0]] = data[1]

        if data[0] == "Broker address":
            address = ','.join(data[1])
            profile_data["Broker address"] = address

        elif data[0] == "Websites":
            for websites in data[1]:
                text_url = websites.values()
                profile_data[text_url[0]] = text_url[1]
            del profile_data["Websites"]
    # get listings
    for_sale = data_dict["props"]["pageProps"]["forSaleListings"]["listing_count"]
    profile_data["sale_listing_count"] = for_sale
    for_rent = data_dict["props"]["pageProps"]["forRentListings"]["listing_count"]
    profile_data["rent_listing_count"] = for_rent

    encodedZuid = data_dict["props"]["pageProps"]["profileDisplay"]["profileInfo"]["encodedZuid"]
    profile_data["encodedZuid"] = encodedZuid
    print(f"extract : {profile_data.values()}")
    return profile_data

def get_profile_from_pages(main_url):
    all_profile_urls = tuple()
    # 25 pages available
    all_pages = [f"{main_url}{i}" for i in range(4,5)]
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        threads = executor.map(extract_urls_from_page, all_pages)
        for index, tuple_urls in enumerate(threads):
            all_profile_urls = all_profile_urls+tuple_urls
            print(f"#{index+1} current profile urls : {len(all_profile_urls)}")
    return all_profile_urls

def main(main_url):
    profile_result = set()
    all_profile_urls = get_profile_from_pages(main_url)
    print(all_profile_urls)
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        profiles = executor.map(get_profile,all_profile_urls)
        for index,profile in enumerate(profiles):
            df = pandas.DataFrame(profile)
            profile_result.add(df)
            print(f"#{index+1} containing : {len(profile_result)} of result")
    return tuple(profile_result)

if __name__=="__main__":

    #https://www.zillow.com/profile-page/api/public/v1/map-results?encodedZuid=X1-ZUza7jt9n9hzwp_5gnlt

    profile_result = set()
    # looking agency for area New Jersey, Chatham
    profile_pages_url = "https://www.zillow.com/professionals/real-estate-agent-reviews/chatham-nj/?page="
    urls = ['/profile/justinkiliszek/', '/profile/LarryWeissYourRealto/', '/profile/KarenTorrente/', '/profile/Remax-Achievers/', '/profile/READ-MY-REVIEWS/', '/profile/zuser20150211075012714/', '/profile/Michelle-Pais/', '/profile/Maureen-Bizub/', '/profile/keith-kirkwood/', '/profile/Marilyn07090/']
    for url in urls:
        print(url)
        data_profile = get_profile(url)
        time.sleep(1)
        profile_result.add(data_profile)
    print(profile_result)
    print(type(profile_result))
