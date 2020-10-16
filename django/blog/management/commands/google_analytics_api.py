"""Hello Analytics Reporting API V4."""
import argparse
import os

from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

import httplib2
from oauth2client import client
from oauth2client import file
from oauth2client import tools

from django.conf import settings

SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
DISCOVERY_URI = ('https://analyticsreporting.googleapis.com/$discovery/rest')

def initialize_analyticsreporting():
    """Initializes an analyticsreporting service object.

    Returns:   analytics an authorized analyticsreporting service
    object.

    """

    credentials = ServiceAccountCredentials.from_p12_keyfile(
        settings.SERVICE_ACCOUNT_EMAIL,
        settings.KEY_FILE_LOCATION,
        scopes=SCOPES
    )

    http = credentials.authorize(httplib2.Http())

    # Build the service object.
    analytics = build('analytics', 'v4', http=http,
                      discoveryServiceUrl=DISCOVERY_URI,
                      cache_discovery=False)

    return analytics

def get_report(analytics):
    # Use the Analytics Service Object to query the Analytics Reporting API V4.
    return analytics.reports().batchGet(
        body={
            'reportRequests': [
                {
                    'viewId': settings.VIEW_ID,
                    'pageSize': 30,
                    'dateRanges': [
                        {
                            'startDate': '365daysAgo',
                            'endDate': 'today'
                        }
                    ],
                    'metrics': [
                        {
                            'expression': 'ga:pageviews'
                        },
                    ],
                    'dimensions': [
                        {
                            'name': 'ga:pagePath'
                        },
                        {
                            'name': 'ga:pageTitle'
                        }
                    ],
                    'dimensionFilterClauses': [
                        {
                            'filters': [
                                {
                                    'dimensionName': 'ga:pagePath',
                                    'expressions': ['^/detail/']
                                }
                            ]
                        }
                    ],
                    'orderBys': [
                        {
                            'fieldName': 'ga:pageviews',
                            'sortOrder': 'DESCENDING'
                        },
                    ]
                }
            ]
        }
    ).execute()

""" ページビューが多い記事を pageSize の分だけ取得 """
def get_popular():
    analytics = initialize_analyticsreporting()
    response = get_report(analytics)
    for report in response.get('reports', []):
        rows = report.get('data', {}).get('rows', [])
        for row in rows:
            link = row['dimensions'][0]
            title = row['dimensions'][1]
            page_view = row['metrics'][0]['values'][0]
            yield link, title, int(page_view)

if __name__ == '__main__':
    for link, title, page_view in get_popular():
        print(link, title, page_view)