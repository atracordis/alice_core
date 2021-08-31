import requests
import os
import time
time.sleep(5)

username = str(os.environ["USERNAME"])
password = str(os.environ["PASSWORD"])

# définition de l'adresse de l'API
# api_address = 'fastapi_container'

api_address = '0.0.0.0'
# port de l'API
api_port = 8000


def get_token(username, password):
    r_token = requests.post("http://{address}:{port}/token".format(address=api_address, port=api_port),
                            data={"username": username, "password": password},
                            headers={"accept": "application/json"})

    return r_token.json()["access_token"]


def test_user(username, password):
    # requête
    token = get_token(username, password)
    r = requests.get(
        url='http://{address}:{port}/users/me'.format(address=api_address, port=api_port),
        headers={"accept": "application/json",
                 "Authorization": "Bearer {}".format(token)})

    output = '''
    ============================
        Authentication test
    ============================
    
    request done at "/users/me"
    | username={username}
    
    expected result = 200
    actual result = {status_code}
    
    ==>  {test_status}
    
    '''
    result = r.json()
    # statut de la requête
    status_code = r.status_code

    test_status = 'FAILURE'
    # affichage des résultats
    if status_code == 200:
        print("status_code ok")
        if ("username" in result):
            test_status = 'SUCCESS'

    output = output.format(username=username,status_code=status_code, test_status=test_status)
    print(output)


test_user(username, password)