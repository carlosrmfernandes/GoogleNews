import ssl
import urllib.request
from GoogleNews import GoogleNews
from newspaper import Config
import mysql.connector
import pandas as pd

ssl._create_default_https_context = ssl._create_unverified_context

user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
config = Config()
config.browser_user_agent = user_agent
googlenews=GoogleNews()
googlenews.set_lang('pt')
googlenews.set_period('7d')
googlenews.set_time_range('02/02/2018','02/28/2020')
googlenews.set_encode('utf-8')
googlenews.search('pretos ')
result=googlenews.result()
df=pd.DataFrame(result)

df=df.drop(columns=["img","datetime"])

df.head()

config = {
  'user': 'root',
  'password': 'root',
  'host': '127.0.0.1',
  'port': 8889,
  'database': 'news',
  'raise_on_warnings': True
}

connection = mysql.connector.connect(**config)

cursor = connection.cursor()

for res in result:
    insert_query = "INSERT INTO news (title, media) VALUES (%s, %s)"
    values = (res["title"], res["media"])    
    cursor.execute(insert_query, values)

connection.commit()
cursor.close()
connection.close()