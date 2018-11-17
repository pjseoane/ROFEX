import requests

class CUser():
    def __init__(self,usr,pswd,account):

        self.usr = usr
        self.pswd = pswd
        self.account = account
        self.endpointDemo = "http://demo-api.primary.com.ar/"
        self.wsEndpointDemo = "ws://demo-api.primary.com.ar/"
        self.activeEndpoint = self.endpointDemo
        self.activeWSEndpoint = self.wsEndpointDemo
        self.historyOHLC_endpoint = "http://h-api.primary.com.ar/MHD/TradesOHLC/{s}/{fi}/{ff}/{hi}/{hf}"
        self.entorno = 1
        self.type_ = "smd"
        self.level_ = "1"
        self.marketId_ = "ROFX"
        self.s = requests.Session()

        self.login()

    def login(self):
        # if (not self.isLogin):
        url = self.activeEndpoint + "auth/getToken"
        headers = {'X-Username': self.usr, 'X-Password': self.pswd}
        loginResponse = self.s.post(url, headers=headers, verify=False)
        # Checkeamos si la respuesta del request fue correcta, un ok va a ser un response code 200 (OK)

        if (loginResponse.ok):
            self.token = loginResponse.headers['X-Auth-Token']
            success = True

            print("login() OK --->", self.token)
        else:
            print("Request Error.")
            success = False
        return success