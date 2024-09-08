import json
import zalologut
phones = []
with open('phone.txt', 'r') as file:
    phones = [line.strip() for line in file]

def add(phone):
    if phone not in phones:
        phones.append(phone)
        with open('phone.txt', 'a') as file:
            file.write(phone + '\n')
        return "Thêm Thành Công"
    else:
        return "Số điện thoại này đã có trong danh sách của tôi rồi"

def rem(phone):
    if phone in phones:
        phones.remove(phone)
        with open('phone.txt', 'w') as file:  
            for phonez in phones:
                file.write(phonez + '\n')
        try:        
          with open(f'data/{phone}.txt', 'r') as file:
              lines = file.readlines()
              imei = lines[0].split('=')[1].strip()
              cookie_str = lines[1].split('=', 1)[1].strip()
              cookie = json.loads(cookie_str.replace("'", "\"")) 
              if zalologut.logiut(imei,cookie):
                  print("Hệ Thống Đã Xuất Xuất")   

        except:
            return"Xoá Sdt Thành Công nhưng Chưa Get Key lần nào Cả"        
        return "Xóa số điện thoại thành công"
    else:
        return "Chưa có trong danh sách"

def check (phone):
    if phone in phones:
        return True
    else:
        return False
