#ver https://gspread.readthedocs.io/en/latest/



import gspread
from oauth2client.service_account import ServiceAccountCredentials
#import oauth2client as oa

# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

# Find a workbook by name and open the first sheet
# Make sure you use the right name here.
sheet = client.open("Legislators 2017-a").sheet1

# Extract and print all of the values
list_of_hashes = sheet.get_all_records()
print(list_of_hashes)

sheet.update_cell(2, 1, "I just wrote to a spreadsheet using Python!")