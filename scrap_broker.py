import hrequests
import json
import pandas
import concurrent.futures


def render_page(url):
    session = hrequests.BrowserSession()
    try:
        resp = session.get(url)
        print(f"getting {resp.status_code} at {url}")
        page = resp.render(mock_human=True)
        session.close()
    except Exception as e:
        print(f"{e} at {url}")
    return page

def find_urls(url):
    urls = set()
    page = render_page(url)
    links = page.html.find("table.StyledTable-c11n-8-99-1__sc-11t7upb-0.fITKUU").absolute_links
    page.close()
    for link in links:
        urls.add(link.replace("#reviews",""))
    print(f"{len(urls)} of links found!")
    return urls

def find_profile(url):
    main_url = "https://www.zillow.com"
    if main_url not in url:
        url = f"https://www.zillow.com{url}"
    page = render_page(url)
    element = page.html.find("script#__NEXT_DATA__")
    page.close()
    data_dict = json.loads(element.text)
    data = parse_profile(data_dict)
    return data
    
def parse_profile(data_dict:dict)->pandas.DataFrame:
    profile = dict()

    data = data_dict["props"]["pageProps"]
    name = data["profileDisplay"]["contactCard"]["name"]
    profile["name"] = name

    info = data["professionalInformation"]
    for item in info:
        if item["term"] == "Broker address":
            profile["broker"] = item["lines"][0]
        elif item["term"] == "Cell phone":
            profile["cell_phone"] = item["description"]
        elif item["term"] == "Websites":
            for url in item["links"]:
                profile[url["text"]] = url["url"]

    zillow_url = data["currentUrl"]
    profile["zillow_url"] = zillow_url

    for_sale_listings = data["forSaleListings"]
    profile["for_sale_listing_count"] = for_sale_listings["listing_count"]
    listing_urls = []
    for listing in for_sale_listings["listings"]:
        listing_urls.append(f'https://www.zillow.com{listing["listing_url"]}')
    profile["for_sale_listings"] = listing_urls

    profile = pandas.DataFrame(profile)

    return profile
    
def save_excel(data,filename):
    df = pandas.DataFrame(data)
    df.to_excel(filename,index=False)
    print(f"{filename} saved!")

def get_all_links(base_url):
    profile_urls = []
    for page in range(1,26):
        url = f"{base_url}{page}"
        profile_urls.extend(find_urls(url))
        print(f"link to scrape : {len(profile_urls)}")
    return profile_urls


if __name__=="__main__":
    real_estate_agent_url = "https://www.zillow.com/professionals/real-estate-agent-reviews/chatham-nj/?page="

    result = pandas.DataFrame()
    all_links = get_all_links(real_estate_agent_url)

    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as excecutor:
        try:
            future_result = excecutor.map(find_profile,all_links)
            for index, future in enumerate(future_result):
                print(f"link #{index} {all_links[index]}")
                result = pandas.concat([result,future],ignore_index=True)
        except Exception as e:
            print(e)

    result.to_excel("broker.xlsx",index=False)
    print("file saved!")

    