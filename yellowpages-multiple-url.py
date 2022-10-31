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

credentials = {
  "type": "service_account",
  "project_id": "dev-airlock-333102",
  "private_key_id": "2180a5cd683ba7cedc0f9801849e988b13925286",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCqazFtaY9AGBKT\n3cm1/MSrZu3cxfDReAP9qm8VjdoVRHSLdxiYBXKGnoP4Y+9Qgtp+AS3j5NBNE0Ux\nUF/fwqXfFX7N8qoERs2kM2H5LA0RwqMoWAjvelBwsTcswcqNXEoaiX7kkER3OVd/\n4Fb8d2QemQP35/T7kSLo5hTeyQJJwa0HKcA6spmwU1qZJXTuOvyohHKsISQ1KRlO\n0zeIwsl+dPtfPJZBYkKSNuF9InwJweIgua+bFZJGpgzYG2zr+8mzfSkUSODjeY4C\nrshdTQLjvFIo8dL1A4yhIiFu/g5Iy5D7LF+66qkY4wOgjT3ZU6H0EZAZNzCmz8tV\nyv0wxSKXAgMBAAECggEAE9ncrhQHvb2QHG1PW8WP2y9oMblU7fF+9YNu4SHe729D\n7CL5WGv6BThdwwdRDx3O+bKFd/BlWzUNcEsef+AaljvYw4Cq0Ui2F5Rsqyu4cgMs\nIjzu/YZP7HCYLrx8La88ao7tmw47C3BAgwLM3yfBH9dPIQeB//PODzcN402i2Jhn\nwFhO8IADJLZ4yw0x7r/eJG4T/T86JxKarty4BhSfr+8IuH6MjCJsA2iQjpSyTthi\nP3LgsdfdfEZNXjAko7P9+T1fNGDwJ8oh8gpiaV+dRukZxe3s4XboaikOoa8+J5Wa\n+bEYgPSPUt5td4vQ7l7XccvMa950VKyiSEwgNzvUAQKBgQDv6k6IpERBApk8FUu5\n9IC6FsTaE2ynDKF34dALcBcLvOgCnjuWNei0ljR3oUctE1JcXbdiz2Q+u+MqzKHC\nF79FfeSCJT8vosgh+OcicBcia8thVYAaQpmxKhlBeJCoo8PViiez3/54z1/Mesco\n/Q5j+zBzlmmRhZK+QBiv0oGhlwKBgQC12Bv2TZAYABmS9jPWV1yaSOefMRxUtL6R\nWOl0kgr8ckBsuyBabhmTJ4R1010wqcDW/LeUvGHfcSX0eOFTx4oO7roas76f/eIf\nX4yc4WfSKlSU1zXNX9wC/98y5rzPuBXukjb3Ti1v0fAfilVS00p6yCVhMzsSDBRg\nJrfaCDanAQKBgQCY3MSvIWLvvRUfiD4YvKXsa6d/f5LiGRUkijeBoii87N8zE9jJ\ni426yl2hv5vXJ5F5kqjPB29K3XIPihSi03imcWFQXyUUV/aGVs4GTj8fSmlqmgym\nLrs4e6dd5NDe8oFLpNxJKrY8CX1zjuMoxZwOrjSf4T1gYCgwmixgkpLP/wKBgQCi\n3YjFw9g/tq8xEfOBkMMuqAdTa//s2ekoctK9BiRyz71l5P9oHt4nDyizAvifIhrG\nMpgVzdd28XdGC5H8oGXFVAk46y3bS99frAtbYwLCmAkjOdFFPQrnYNY+V6xZ+o0i\nHLDANLO7R/NhvFsJEJbPez0HXoQUeN8y8tqNm/efAQKBgBe7e8NkK7yssfXmWpOU\n55O6odWwJD1HFElwEZob5Et23UykZzXIM5gTZcO/+Bn0DCHHg+n5pDaiY0A4Fsw0\n/B+ckViQSSq7feZkITB50+bL2uGwXVCjjfoPt+pTVKeTbydxtgPTEncc8rbXNnoI\nGxwYs5DzIC2s7ebybJ7MY+ED\n-----END PRIVATE KEY-----\n",
  "client_email": "fulker@dev-airlock-333102.iam.gserviceaccount.com",
  "client_id": "116643256588791743728",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/fulker%40dev-airlock-333102.iam.gserviceaccount.com"
}

gc = gspread.service_account_from_dict(credentials)
sht1 = gc.open_by_url('https://docs.google.com/spreadsheets/d/1IAPJK6eWsEx4C5JW6irn8yi_AVFgs8L1fbGjzfKEiUw/edit#gid=0').sheet1

df = pd.DataFrame(total_list)
gd.set_with_dataframe(sht1, df)
