from flask import Flask, request
import kami
import asyncio
import end
app = Flask(__name__)

@app.route('/zalo', methods=['GET'])
def get_cookie():
    
    all_cookies = request.headers.get('Cookie')
    cookie_dict = {}
    if all_cookies:
     cookies = all_cookies.split("; ")
     for cookie in cookies:
        key, value = cookie.split("=", 1)
        cookie_dict[key] = value
    
    
    imei = request.args.get('imei')
    if imei == None or cookie_dict == None:
       data = {
          'error_code': 403,
         ' error_message': "Khong tim thay imei và cookie của ban vui long kiem tra lai"
       }
       return data

   
    data = asyncio.run(kami.main(imei, cookie_dict))
    #print(data)
    if data['error_code'] == 0 or data['error_code'] == 99:
       try:
        phone = data['phone_number']
       except:
          phone = data['data']['phone_number']
       with open(f'data/{phone}.txt', 'w') as file: 
          
          z = f"imei={imei} \ncookie={cookie_dict}"
          file.write(z + '\n')
    return data
@app.route('/add', methods=['GET'])
def add():
   key = request.args.get('key')
   phone = request.args.get('phone')
   if key !="kami":
      data = {
         'msg': " Làm Gì Đó bạn ???"
      }
   else:
      z = end.add(phone)
      data = {
         'msg': z
      }
   return data
@app.route('/rem', methods=['GET'])
def  rem():
   key = request.args.get('key')
   phone = request.args.get('phone')
   if key !="kami":
      data = {
         'msg': " Làm Gì Đó bạn ???"
      }
   else:
      z = end.rem(phone)
      data = {
         'msg': z
      }
   return data
@app.route('/kami', methods=['GET'])      
def remz():
   
   return end.phones
   
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
