from Path.paths import *
import requests


def authenticate_user(request_values):
    mail = request_values.get('mail')
    password = request_values.get('password')
    URL = USER_SERVICE + 'checkUser'
    response = requests.get(URL, params={"mail": mail, "password": password})
    if response.status_code == 200:
        print('Auth succesful',mail,password)
        return True
    else:
        return False
