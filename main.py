from scrap_broker import broker_profile
from scrap_listing import encodedZuid_to_home_details
from openpyxl import load_workbook

import pandas
import concurrent.futures


if __name__=="__main__":
	base_url = "https://www.zillow.com/professionals/real-estate-agent-reviews/chatham-nj/?page="
	result = []
	df = broker_profile(base_url)

	df.to_excel("final_result.xlsx",sheet_name="broker_profile",index=False)

	encodedZuid_list = df["encodedZuid"].tolist()
	forSale_list =  df["for_sale_count"].tolist()
	forRent_list = df["for_rent_count"].tolist()

	encodedZuid = [encodedZuid_list[i] for i in range(len(encodedZuid_list)) if (forSale_list[i]+forRent_list[i])>0]
	with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
		list_df = executor.map(encodedZuid_to_home_details,encodedZuid)
		for index, df in enumerate(list_df):
			result.append(df)
			print(f"broker #{index+1} of {len(encodedZuid)}")
	house_listing = pandas.concat(result)

	with pandas.ExcelWriter("final_result.xlsx",engine="openpyxl",mode="a") as writer:
		house_listing.to_excel(writer,sheet_name="house_listing",index=False)
	print("saved")