import azure.functions as func

import tempfile
import json

from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
VIEW_ID = '<Replace with your View ID>'
DATA = '<Replace with your credentials>'

def initialize_analyticsreporting():
  """Initializes an Analytics Reporting API V4 service object.

  Returns:
    An authorized Analytics Reporting API V4 service object.
  """
  dir_path = tempfile.gettempdir()
  with open(dir_path + "/cred.json", "w") as outfile:
    json.dump(DATA, outfile)

  KEY_FILE_LOCATION = dir_path + "/cred.json"
  credentials = ServiceAccountCredentials.from_json_keyfile_name(
      KEY_FILE_LOCATION, SCOPES)

  # Build the service object.
  analytics = build('analyticsreporting', 'v4', credentials=credentials)
  return analytics


def get_report(analytics):
  """Queries the Analytics Reporting API V4.

  Args:
    analytics: An authorized Analytics Reporting API V4 service object.
  Returns:
    The Analytics Reporting API V4 response.
  """
  return analytics.reports().batchGet(
      body={
        'reportRequests': [
        {
          'viewId': VIEW_ID,
          'dateRanges': [{'startDate': '7daysAgo', 'endDate': 'today'}],
          'metrics': [{'expression': 'ga:sessions'}],
          'dimensions': [{'name': 'ga:country'}]
        }]
      }
  ).execute()

def main(req: func.HttpRequest) -> func.HttpResponse:
    """Pulls a GA View
    
    Returns:
        GA APIs response.
    """
    analytics = initialize_analyticsreporting()
    response = get_report(analytics)

    return json.dumps(response)