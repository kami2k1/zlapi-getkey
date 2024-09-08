import requests
from datetime import datetime
def logiut(imei,cookie):
          url = "https://wpa.chat.zalo.me/api/login/logOut"
          params = {
              "zpw_ver": "637",
              "zpw_type": "30",
              "time": int(datetime.now().timestamp() * 1000),
              "client_version": "637",
              "type": "30",
              "imei": imei,
              "computer_name": "Web"
          }    
          headers = {
              "accept": "application/json, text/plain, */*",
              "accept-encoding": "gzip, deflate, br, zstd",
              "accept-language": "vi-VN,vi;q=0.9,en;q=0.8",
              "content-type": "application/x-www-form-urlencoded",          
              "origin": "https://chat.zalo.me",
              "referer": "https://chat.zalo.me/",
              "sec-ch-ua": '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
              "sec-ch-ua-mobile": "?0",
              "sec-ch-ua-platform": '"Windows"',
              "sec-fetch-dest": "empty",
              "sec-fetch-mode": "cors",
              "sec-fetch-site": "same-site",
              "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"
          }      
          h1 = requests.get(url, headers=headers,params=params,cookies=cookie).status_code
          try:
               if h1 == 200 :
                   print("oke")
                   h2 = requests.post("https://id.zalo.me/account/logout?continue=https%3A%2F%2Fchat.zalo.me%2F", headers=headers,cookies=cookie).json()
                   token = h2['data']['token']
                   h3 =requests.get(f"https://id.zalo.me/account/logout?token={token}&continue=https%3A%2F%2Fchat.zalo.me%2F",headers=headers,cookies=cookie).status_code
                   if h3 == 200:
                       print('Logut Oke')
                       return True
               return False                 
          except:
                return False
             
               
          
          