import requests
import os
import pandas as pd
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
sentences = pd.read_csv("test_data.csv", encoding='cp1252')


def get_token(username, password):
    r_token = requests.post("http://{address}:{port}/token".format(address=api_address, port=api_port),
                            data={"username": username, "password": password},
                            headers={"accept": "application/json"})

    return r_token.json()["access_token"]


def get_sentiment(token, branch, text):
    r = requests.get(
        url='http://{address}:{port}/sentiment'.format(address=api_address, port=api_port),
        params={"branch": branch, "sentence": text},
        headers={"accept": "application/json",
                 "Authorization": "Bearer {}".format(token)})
    return r.json()["sentiment"]


def test_sentiment(token, branch, sentences):
    # requête
    nb_ok, nb_all, success_rate = "", "", 0
    status_code = 404
    try:
        sentences[branch + "_test"] = sentences.Review_Text.apply(lambda text: get_sentiment(token, branch, text))
        nb_ok = (sentences[branch + "_test"].astype(str) == sentences[branch].astype(str) ).sum()
        nb_all = sentences.shape[0]
        success_rate = nb_ok / nb_all
    except:
        pass

    output = '''
    ============================
        Sentiment test
    ============================

    request done at "/sentiment"
    
    expected result = 200
    actual result = {status_code}

    branch : {branch}
    validation : {success_rate}
    Valid lines : {nb_ok}
    Total lines : {nb_all}

    ==>  {test_status}

    '''
    # statut de la requête

    test_status = 'FAILURE'
    # affichage des résultats
    if success_rate > 0.9:
        test_status = 'SUCCESS'
        status_code = 200

    output = output.format(username=username, status_code=status_code, test_status=test_status,
                           success_rate=success_rate,
                           branch=branch, nb_ok=nb_ok, nb_all=nb_all)
    print(output)


token = get_token(username, password)
for branch in valid_branches:
    test_sentiment(token, branch, sentences)
