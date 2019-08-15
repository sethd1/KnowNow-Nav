# Anne Wang
import csv
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def convert_googlesheets_into_csv_file():
	# In order to use this method, you must first follow the steps that I have provided. 
	# This method uses gpsread which is the Python API for Google Sheets. To use it, one must
	# have credentials to access to the sheet. 

	# refer to gspread_instructions.txt 

	# use creds to create a client to interact with the Google Drive API
	scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
	creds = ServiceAccountCredentials.from_json_keyfile_name('client-secret.json', scope)
	client = gspread.authorize(creds)

	# Find a workbook by name and open the first sheet
	# Make sure you use the right name here.
	sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1Fi9ZV8zP8iKOWwZsJ342e0sasKJ357l7CZY9_PPn0n4/edit?usp=drive_web&ouid=113237862202116211721").sheet1

	# Extract and print all of the values
	list_of_hashes = sheet.get_all_records()
	print(list_of_hashes)


def associate_header_with_insights(header: str, entered_search: str) -> list:
	# This function returns a list that is filled with dictionaries at each index.
	# You can choose which header you want and the specific text you're looking for.
	# The keys are the searches that include entered_search, and its value is
	# its respective patient insight. 

	with open('Finalized Cohort - Sheet1.csv', 'r', newline="") as f:

		patient_insights_list = []

		reader = csv.DictReader(f)
		data = list(reader) 
		headers = reader.fieldnames

		for dictionary in data:
			if entered_search.strip() in dictionary[header]:
				new_dict = {}

				new_dict[dictionary[header]] = dictionary['Patient insight']
				patient_insights_list.append(new_dict)

	return patient_insights_list

def main():
	convert_googlesheets_into_csv_file()
	print(associate_header_with_insights('Category tag', 'Oncotype'))

if __name__ == '__main__':
	main()