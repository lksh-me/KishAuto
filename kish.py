import threading
from queue import Queue
import requests
import random
import string
import json
import hashlib
from faker import Faker

print(f"""
FACEBOOK AUTO CREATOR
for testers only trial""")
print('\x1b[38;5;208m⇼'*60)
print('\x1b[38;5;22m•'*60)
print('\x1b[38;5;22m•'*60)
print('\x1b[38;5;208m⇼'*60)

def generate_random_string(length):
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for i in range(length))

def GetEmail():
    response = requests.post('https://api.internal.temp-mail.io/api/v3/email/new').json()
    return response['email']

def GetCode(email):
    try:
        response = requests.get(f'https://api.internal.temp-mail.io/api/v3/email/{email}/messages').text
        code = re.search(r'FB-(\d+)', response).group(1)
        return code     
    except Exception as e:
        print(f'[×] Error : {e}')
        return None
 
def register_facebook_account(email, password, first_name, last_name, birthday, proxy=None):
    api_key = '882a8490361da98702bf97a021ddc14d'
    secret = '62f8ce9f74b12f84c123cc23437a4a32'
    gender = random.choice(['M', 'F'])
    req = {'api_key': api_key,'attempt_login': True,'birthday': birthday.strftime('%Y-%m-%d'),'client_country_code': 'EN','fb_api_caller_class': 'com.facebook.registration.protocol.RegisterAccountMethod','fb_api_req_friendly_name': 'registerAccount','firstname': first_name,'format': 'json','gender': gender,'lastname': last_name,'email': email,'locale': 'en_US','method': 'user.register','password': password,'reg_instance': generate_random_string(32),'return_multiple_errors': True}
    sorted_req = sorted(req.items(), key=lambda x: x[0])
    sig = ''.join(f'{k}={v}' for k, v in sorted_req)
    ensig = hashlib.md5((sig + secret).encode()).hexdigest()
    req['sig'] = ensig
    api_url = 'https://b-api.facebook.com/method/user.register'
    reg = _call(api_url, req, proxy)
    id = reg['new_user_id']
    token = reg['session_info']['access_token']
    print(f'''
-----------SUCCESS-OK-----------
EMAIL : {email}
ID : {id}
PASSWORD : {password}
NAME : {first_name} {last_name}
OTP : {code}
BIRTHDAY : {birthday} 
GENDER : {gender}
-----------SUCCESS-OK-----------
Token : {token}
-----------kish cutiepie-----------''')
    open('username.txt', 'a')

def _call(url, params, proxy=None, post=True):
    headers = {'User-Agent': '[FBAN/FB4A;FBAV/35.0.0.48.273;FBDM/{density=1.33125,width=800,height=1205};FBLC/en_US;FBCR/;FBPN/com.facebook.katana;FBDV/Nexus 7;FBSV/4.1.1;FBBK/0;]'}
    if post:
        response = requests.post(url, data=params, headers=headers, proxies=proxy)
    else:
        response = requests.get(url, params=params, headers=headers, proxies=proxy)
    return response.json()

def test_proxy(proxy, q, valid_proxies):
    if test_proxy_helper(proxy):
        valid_proxies.append(proxy)
    q.task_done()

def test_proxy_helper(proxy):
    try:
        response = requests.get('https://api.mail.tm', proxies=proxy, timeout=5)
        print(f'Pass: {proxy}')
        return response.status_code == 200
    except:
        print(f'Fail: {proxy}')
        return False

def load_proxies():
    with open('proxies.txt', 'r') as file:
        proxies = [line.strip() for line in file]
    return [{'http': f'http://{proxy}'} for proxy in proxies]

def get_working_proxies():
    proxies = load_proxies()
    valid_proxies = []
    q = Queue()
    for proxy in proxies:
        q.put(proxy)
    
    for _ in range(10):  # 10 threads
        worker = threading.Thread(target=worker_test_proxy, args=(q, valid_proxies))
        worker.daemon = True
        worker.start()
    
    q.join()  # Block until all tasks are done
    return valid_proxies

def worker_test_proxy(q, valid_proxies):
    while True:
        proxy = q.get()
        if proxy is None:
            break
        test_proxy(proxy, q, valid_proxies)

working_proxies = get_working_proxies()

if not working_proxies:
    print('[×] No working proxies found. Please check your proxies.')
else:
    for i in range(int(input('[+] How Many Accounts You Want:  '))):
        proxy = random.choice(working_proxies)
        email, password, first_name, last_name, birthday = GetEmail(proxy)
        if email and password and first_name and last_name and birthday:
            register_facebook_account(email, password, first_name, last_name, birthday, proxy)

print('\x1b[38;5;208m⇼'*60)
