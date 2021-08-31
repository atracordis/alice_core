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

valid_branches = ["agnostic_model", "Disneyland_HongKong", "Disneyland_California", "Disneyland_Paris"]


def get_token(username, password):
    r_token = requests.post("http://{address}:{port}/token".format(address=api_address, port=api_port),
                            data={"username": username, "password": password},
                            headers={"accept": "application/json"})

    return r_token.json()["access_token"]


def test_score(token, branch):
    # requête
    r = requests.get(
        url='http://{address}:{port}/get_score'.format(address=api_address, port=api_port),
        params={"branch": branch},
        headers={"accept": "application/json",
                 "Authorization": "Bearer {}".format(token)})

    output = '''
    ============================
        Get score test
    ============================
    
    request done at "/get_score"
    
    expected result = 200
    actual result = {status_code}
    
    branch : {branch}
    score : {score}
    
    ==>  {test_status}
    
    '''
    result = r.json()
    # statut de la requête
    status_code = r.status_code
    score = "ERROR"
    test_status = 'FAILURE'
    # affichage des résultats
    if status_code == 200:
        print("status_code ok")
        if ("score" in result):
            test_status = 'SUCCESS'
            score = str(result["score"])

    output = output.format(username=username, status_code=status_code, test_status=test_status, score=score,
                           branch=branch)
    print(output)


token = get_token(username, password)

for branch in valid_branches:
    test_score(token, branch)
