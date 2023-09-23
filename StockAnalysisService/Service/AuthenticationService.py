from Utils.paths import *
import requests


def authenticate_user(request_values):
    """
    Function for user authentication. Sends mail and password to the user_service.
    If the request is 200, it returns true. Otherwise false
    :param request_values:
        dict:
            keys: ['mail','password']
    :return:
        True: if authentication was succesful
        False: if authentication was not successful (wrong mail, password or the user does not exist)
    """
    mail = request_values.get('mail')
    password = request_values.get('password')
    URL = USER_SERVICE + 'checkUser'
    response = requests.get(URL, params={"mail": mail, "password": password})
    if response.status_code == 200:
        print('Auth succesful',mail,password)
        return True
    else:
        return False
