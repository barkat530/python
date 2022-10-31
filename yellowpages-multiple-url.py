import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

if not os.path.exists('D:\Dropbox\Python\YellowPages/'):
    os.makedirs('D:\Dropbox\Python\YellowPages/')
os.chdir('D:\Dropbox\Python\YellowPages/')

total_list = []

for j in range(1, 3):
    try:

        print(f'Scraping Page {j}')

        url = f'https://www.yellowpages.com/search?search_terms=breeder&geo_location_terms=New%20York%2C%20NY&page={j}'
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36'}
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.content, 'html.parser')

        divs = soup.find_all('div', {'class' : 'result'})
        for items in divs:

            #Company Name
            try:
                var1 = items.find('h2', class_ = 'n').find('a', {'class' : 'business-name'}).find('span').text.strip().replace('\n', '')
            except:
                var1 = ''

            #Website
            try:
                var2 = items.find('a', class_ = 'track-visit-website')['href']
            except:
                var2 = ''

            #YellowPages URL
            try:
                var3 = 'https://www.yellowpages.com' + items.find('h2', class_ = 'n').find('a', {'class' : 'business-name'})['href']
            except:
                var3 = ''

            #Company Phone
            try:
                var4 = items.find('div', class_ = 'phones phone primary').text.strip().replace('\n', '')
            except:
                var4 = ''

            #Address
            try:
                var5 = items.find('div', class_ = 'street-address').text.strip().replace('\n', '')
            except:
                var5 = ''

            #City, State, Zip
            try:
                var6 = items.find('div', class_ = 'locality').text.strip().replace('\n', '')
            except:
                var6 = ''
            
            #Category
            try:
                jod = items.find('div', class_ = 'categories').find_all('a')
                var7 = ', '.join(jod[i].text.strip().replace('\n', '') for i in range(len(jod)))
            except:
                var7 = ''

            # #Avg. Rating
            # try:
            #     var8 = items.find('span', class_ = 'count').text.replace('\n', '').replace(')', '').replace('(', '')
            # except:
            #     var8 = ''

            #No of Reviews
            try:
                var9 = items.find('span', class_ = 'count').text.replace('\n', '').replace(')', '').replace('(', '')
            except:
                var9 = ''
            
            total = {
                'Company Name': var1,
                'Website': var2,
                'YellowPages URL': var3,
                'Company Phone': var4,
                'Address': var5,
                'City, State, Zip': var6,
                'Category': var7,
                # 'Avg. Rating': var8,
                'No of Reviews': var9,
            }
            total_list.append(total)


        try:
            nxt = soup.find('a', {'class' : 'next ajax-page'}).text
        except:
            break

    except:
        pass
  


df = pd.DataFrame(total_list)
df.to_csv('count1.csv', index=False)

import gspread
import gspread_dataframe as gd

gc = gspread.service_account(filename=r'D:\Dropbox\Python\l4l\fulker.json')
sht1 = gc.open_by_url('https://docs.google.com/spreadsheets/d/1IAPJK6eWsEx4C5JW6irn8yi_AVFgs8L1fbGjzfKEiUw/edit#gid=0').sheet1

df = pd.DataFrame(total_list)
gd.set_with_dataframe(sht1, df)
