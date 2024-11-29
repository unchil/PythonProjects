import pandas as pd
import requests
import xmltodict
from sqlalchemy import create_engine
from datetime import datetime

DB_URL = 'sqlite:////Volumes/WorkSpace/PythonProjects/power_exchange/db.sqlite3'
ENGIN = create_engine(DB_URL, echo=False)
BASE_URL = 'https://openapi.kpx.or.kr/openapi'

EncodingKey = '5n1IN38zxdvnUX9sRlSNdTG9xdkLV3gLzBVEuFn9zjdols8ci8U6V%2F7GeZDujqbHE4KShW0iI6%2BR50vGP7j9CA%3D%3D'
DecodingKey = '5n1IN38zxdvnUX9sRlSNdTG9xdkLV3gLzBVEuFn9zjdols8ci8U6V/7GeZDujqbHE4KShW0iI6+R50vGP7j9CA=='
ActiveKey = EncodingKey
endpoint_today =   f'{BASE_URL}/sukub5mToday/getSukub5mToday'
url = f'{endpoint_today}?serviceKey={ActiveKey}'
table_today =   'supplydemand_dayfiveminsupplydemand'


result = requests.get(url)
if result.status_code == 200:
    try:
        result_dict = xmltodict.parse(result.text)
        if result_dict['response']['header']['resultCode'] == '00':
            items = result_dict['response']['body']['items']['item']
            df = pd.DataFrame(items)
            df.to_sql(name=table_today, con=ENGIN, if_exists='append', index=False,  method='multi')
        else:
            print(f"{datetime.now().strftime('%Y%m%d%H%M%S')}:{result_dict['response']['header']['resultMsg']}")
    except Exception as e:
        print(f"{datetime.now().strftime('%Y%m%d%H%M%S')}:{e}")

else:
    print(f"{datetime.now().strftime('%Y%m%d%H%M%S')}:{result.status_code}")
