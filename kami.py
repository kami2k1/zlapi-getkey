import json
import requests
from Crypto.Cipher import AES
import base64
import hashlib
import end
from datetime import datetime

class ZaloAPI:
    def __init__(self, api_domain, api_type, api_version ):
        self.authDomain = api_domain
        self.apiType = api_type
        self.apiVersion = api_version

    def get_encrypt_key(self, imei):
        return hashlib.md5(imei.encode()).digest()

    def encode_aes(self, key, data):
        cipher = AES.new(key, AES.MODE_ECB)
        encoded = base64.b64encode(cipher.encrypt(self.pad(data)))
        return encoded.decode('utf-8')

    def decode_aes(self, key, encoded_data):
        cipher = AES.new(key, AES.MODE_ECB)
        decoded = self.unpad(cipher.decrypt(base64.b64decode(encoded_data)))
        return decoded.decode('utf-8')

    def pad(self, s):
        block_size = AES.block_size
        return s + (block_size - len(s) % block_size) * chr(block_size - len(s) % block_size)

    def unpad(self, s):
        return s[:-ord(s[len(s) - 1:])]

    def get_sign_key(self, data):
        return hashlib.sha256(data.encode()).hexdigest()

    async def encrypt_param(self, params, imei):
        encrypted_params = self._encrypt_param(params, imei)
        if encrypted_params:
            return {
                'params': {
                    **encrypted_params['encrypted_params'],
                    'params': encrypted_params['encrypted_data'],
                    'type': self.apiType,
                    'client_version': self.apiVersion,
                    'signkey': self.get_sign_key(encrypted_params['encrypted_data'])
                },
                'enk': encrypted_params['enk']
            }
        return {'params': params, 'enk': None}

    def _encrypt_param(self, params, imei):
        try:
            key = self.get_encrypt_key(imei)
            encrypted_data = self.encode_aes(key, json.dumps(params))
            return {
                'encrypted_data': encrypted_data,
                'encrypted_params': {'imei': imei},
                'enk': key
            }
        except Exception as e:
            print("Error during encryption:", e)
            return None

    async def decrypt_resp(self, enk, response):
        if not enk:
            return response
        try:
            decoded_data = self.decode_aes(enk, response['data']['data'])
            response['data'] = json.loads(decoded_data)
        except Exception as e:
            print("Error during decryption:", e)
            response['data'] = {
                'error_code': 18060,
                'error_message': "INVALID_ENCRYPTION_PROTOCOL"
            }
        return response

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
           
    

