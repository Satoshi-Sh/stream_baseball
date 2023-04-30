import requests
import pandas as pd
import base64
from io import StringIO
import japanize_matplotlib

# read a data from github repositry. This data is updated daily.
url = 'https://api.github.com/repos/satoshi-sh/baseball-git-scraper/contents/data/central.csv'
response = requests.get(url)

if response.status_code == 200:
   response_json = response.json()
   file_contents = base64.b64decode(response_json['content']).decode('utf-8')
   df = pd.read_csv(StringIO(file_contents))
   df['date'] = pd.to_datetime(df['date'])
   df.to_csv('data/central.csv',index=False)

else:
    print('Error:', response.status_code, response.json()['message'])