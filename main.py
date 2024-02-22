from scrap_broker import broker_profile
from scrap_listing import encodedZuid_to_home_details

import pandas
import concurrent.futures

def skip_empty_listing(df:pandas.DataFrame)->list:
	pass

	"""read the zpid, for sale, for return
	compare for sale+for rent > 0
	get the zpid"""


if __name__=="__main__":
	base_url = "https://www.zillow.com/professionals/real-estate-agent-reviews/chatham-nj/?page="
	result = []
	df_broker_profile = broker_profile(base_url)
	encodedZuid = df_broker_profile["encodedZuid"].tolist()
	with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
		list_df = executor.map(encodedZuid_to_home_details,encodedZuid)
		for index, df in enumerate(list_df):
			result.append(df)
			print(f"broker #{index+1} of {len(encodedZuid)}")
	house_listing = pandas.concat(result)

	with pandas.ExcelWriter("final_result.xlsx") as writer:
		df_broker_profile.to_excel(writer, sheet_name="broker_profile",index=False)
		house_listing.to_excel(writer, sheet_name="house_listing",index=False)
	print("saved!")