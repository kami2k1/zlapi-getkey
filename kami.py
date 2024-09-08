import json
import requests

import end
from datetime import datetime

class ZaloAPI:
    def __init__(self, api_domain, api_type, api_version ):
        self.authDomain = api_domain
        self.apiType = api_type
        self.apiVersion = api_version
    async def get_login_info(self, imei,cookie, language="vi", local_ip="", screen_size=None, info="", source_install=None, additional_params=None, is_new=0 ,):
        url = f"{self.authDomain}/api/login/getLoginInfo"
        params = {
            'imei': imei,
            'computer_name': "web",
            'language': language,
            'ts':int(datetime.utcnow().timestamp() * 1000)
        }
        # if local_ip and screen_size:
        #     params.update({'localIP': local_ip, 'width': screen_size['width'], 'height': screen_size['height']})
        # if info:
        #     params['info'] = json.dumps(info)
        # if source_install:
        #     params['source_install'] = source_install
        # if additional_params:
        #     params.update(additional_params)
        # if is_new:
        #     params['is_new'] = is_new

        # encrypted = await self.encrypt_param(params, imei)
        HEADERS = {
	"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
	"Accept": "application/json, text/plain, */*",
	"sec-ch-ua": "\"Not-A.Brand\";v=\"99\", \"Chromium\";v=\"124\"",
	"sec-ch-ua-mobile": "?0",
	"sec-ch-ua-platform": "\"Linux\"",
	"origin": "https://chat.zalo.me",
	"sec-fetch-site": "same-site",
	"sec-fetch-mode": "cors",
	"sec-fetch-dest": "empty",
	"referer": "https://chat.zalo.me/",
	"accept-language": "vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5",
}
#         proxy = {
#     'http': 'http://admin:admin@15.235.186.150:8080',
#     'https': 'http://admin:admin@15.235.186.150:8080'
# }

        response = requests.get(url, headers=HEADERS,params=params,cookies=cookie).json()
  

        return response



async def main(imei,cokie):
    api = ZaloAPI("https://wpa.chat.zalo.me", "30", "637")
    
    
    
    response = await api.get_login_info(imei, cokie)
    
    #print(response)
    if response['error_code'] == 0:
       
       zpw_enk = response['data']['zpw_enk']
       
       phone = response['data']['phone_number']
       semid_2 = response['data']['send2me_id']
       if not end.check(phone):
           data = {
               'error_code':99, 
                ' error_message' : f"  Số điện Thoại Chưa có Trong list NT cho admin để được thêm zalo: @quangz3 phone you: {phone}",
                 'phone_number':phone
           }
       else:
          data = {
             'error_code':0,
              'data':{
                  'secret_key': zpw_enk,
                  'send2me_id' :semid_2,
                  'phone_number' :phone
   
              }
          }
       return data
    else :
        data = {
            'error_code' : response['error_code'],
           ' error_message' : f"{response['error_message']  } " 
        }
        return data
           
    

