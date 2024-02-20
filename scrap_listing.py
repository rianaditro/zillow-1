import hrequests


def send_request():
    url = "https://www.zillow.com/profile/RobertDekanski"
    r = hrequests.get(url)
    print(r.status_code)
    print(r.text)

send_request()

# if __name__=="__main__":
#     encodedZuid = "X1-ZUz9q7ndwbqqrt_aroy1"
#     size = 100

#     # text =

#     url = f"https://www.zillow.com/profile-page/api/public/v1/active-listings?encodedZuid={encodedZuid}&size={size}"
#     profile = "https://www.zillow.com/profile/RobertDekanski"
#     maps = "https://www.zillow.com/profile-page/api/public/v1/map-results?encodedZuid=X1-ZUz9q7ndwbqqrt_aroy1"

#     with hrequests.BrowserSession(mock_human=True,browser="firefox") as session:
#         r = session.get(maps)
#         print(r.status_code)
#         print(r.url)
#         html = r.html.text
#         r = session.get(url)
#         print(r.status_code)
#         print(r.url)
#         html = r.html.text


#     text_dict = json.loads(html)

#     listing_count = text_dict["listing_count"]
#     listings = text_dict["listings"]
#     house_list = []
#     for house in listings:
#         data = dict()
#         for item in house:
#             data[item] = house[item]
#             if item == "address":
#                 address = ",".join(house["address"].values())
#                 data["address"] = address
#         house_list.append(data)
#     # print(house_list)
#     # print(len(house_list))