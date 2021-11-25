import requests, json


def token():

    url = 'https://school-web.ai-classes.com/authentication-center/authentication/login'

    headers = {
        # 'User-agent':'Mozilla 5.10',
        # 'cache-control': 'no-cache',
        'Authorization':'Basic RkE5RTIxNUJFNTY2RUU5MjYxNEZCQzExQUJFREY5Njg6M0Y2OEMwQkJERDM2NTYyODY2MEFDRDZDNEE4QUY2RjY=',
        'CURRENT_APP':'FA9E215BE566EE92614FBC11ABEDF968',
        # 'postman-token':'220d2989-c111-fea3-874f-f5c31111db49',
        # "Content-Type": "application/x-www-form-urlencoded",
        # "Accept":"*/*",
        # "Accept-Encoding":'gzip, deflate, br',
        # "Connection":"keep-alive",
    }

    user = {
        "username": "大连测试001",
        "password": "a11111_"
    }
    token = requests.post(url, data= user, headers= headers)

    return token.json()['access_token']
