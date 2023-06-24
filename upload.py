from Google import Create_Service
from datetime import datetime

API_NAME = 'sheets'
API_VERSION = 'v4'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# now=datetime.now()
# timestamp = datetime.timestamp(now)
# dt_object = datetime.fromtimestamp(timestamp)
# a = str(dt_object)
dt_now = (datetime.now().strftime('%b %d %Y , %H:%M'))

def sheetsupdate(task,method,remark):
	try:
		CLIENT_SECRET_FILE_data_log = 'creds.json'
		service_data_log = Create_Service(CLIENT_SECRET_FILE_data_log, API_NAME, API_VERSION, SCOPES)

		spreadsheet_id_data_log = '12iDVTvh36UQTMPm-Hz4_SaF4OG5Fqt2eTq_-RUIME2s' #Enter Google Sheet ID Here
		mySpreadsheets = service_data_log.spreadsheets().get(spreadsheetId=spreadsheet_id_data_log).execute()

		worksheet_name = 'Sheet1!' #Enter Worksheet Name
		cell_range_insert = 'A1' #Enter Starting Rangee
		values = ((dt_now,task,method,remark),()) #Pass Values here

		value_range_body = {
		'majorDimension': 'ROWS',
		'values': values
		}
		service_data_log.spreadsheets().values().append(
			spreadsheetId=spreadsheet_id_data_log,
			valueInputOption='USER_ENTERED',
			range=worksheet_name + cell_range_insert,
			body=value_range_body
		).execute()

		print("End of Updating Sheets")

	except Exception as e:
		print("[INFO] caught a RuntimeError : ")
		print(e)

