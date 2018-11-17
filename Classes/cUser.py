import requests
import websocket
import threading
import simplejson
from time import sleep


# 4


class cRofexSuscript():

    def __init__(self, usr, pswd, account, symbols):
        self.usr = usr
        self.pswd = pswd
        self.account = account
        self.symbols = symbols
        self.endpointDemo = "http://demo-api.primary.com.ar/"
        self.wsEndpointDemo = "ws://demo-api.primary.com.ar/"
        self.activeEndpoint = self.endpointDemo
        self.activeWSEndpoint = self.wsEndpointDemo
        self.historyOHLC_endpoint = "http://h-api.primary.com.ar/MHD/TradesOHLC/{s}/{fi}/{ff}/{hi}/{hf}"
        self.entorno = 1
        self.s = requests.Session()
        self.type_ = "smd"
        self.level_ = "1"
        self.marketId_ = "ROFX"
        self.messages = []
        self.mensajes = 0

        if self.login():
            self.runWS()

    def on_message(self, message):
        self.mensajes += 1
        try:
            # Valido Mensaje entrante
            self.msg = simplejson.loads(message)
            self.messages.append(self.msg)

            msgType = self.msg['type'].upper()

            if msgType == 'MD':

                self.incomingMD()
                self.goRobot()


            elif msgType == 'OR':
                print("En Mensaje OR")
                print(self.msg)
            else:
                print("Tipo de Mensaje Recibido No soportado: " + self.msg)
        except:
            # print("Error al procesar mensaje recibido:--->>> " + msg)
            print("Error al procesar mensaje recibido:--->>> " + message)

    def on_error(self, error):
        print("Salio por error")
        print(error)
        self.ws.close()

    def on_close(ws):
        print("### connection closed ###")

    def on_open(ws):
        print("WS Conection Open...")

    def runWS(self):
        headers = {'X-Auth-Token:{token}'.format(token=self.token)}
        self.ws = websocket.WebSocketApp(self.activeWSEndpoint,
                                         on_message=self.on_message,
                                         on_error=self.on_error,
                                         on_close=self.on_close,
                                         on_open=self.on_open,
                                         header=headers)

        wst = threading.Thread(target=self.ws.run_forever, kwargs={"ping_interval": 5})

        wst.start()

        # Esperamos a que la conexion ws se establezca
        conn_timeout = 5
        # conn_timeout = 50 #y nada
        sleep(1)

        while not self.ws.sock.connected and conn_timeout:
            sleep(1)
            conn_timeout -= 1
        else:

            for self.sym in self.symbols:
                aaa = self.buildMessage(self.sym)
                self.ws.send(aaa)

                print("Sent Suscription msg", aaa)

                print("Receiving...")

                sleep(1)  # y nada

    def incomingMD(self):

        timestamp = self.msg['timestamp']
        sym = self.msg['instrumentId']['symbol']
        # Aca hay un problema si no hay bid u offer pq solo viene ['marketData']
        bidMsg = self.msg['marketData']['BI']
        offerMsg = self.msg['marketData']['OF']

        if bidMsg == []:
            # >No BID detected")
            bid = 0
            bidSize = 0
        else:
            bid = self.msg['marketData']['BI'][0]['price']
            bidSize = self.msg['marketData']['BI'][0]['size']

        if offerMsg == []:
            # >No OFFER detected")
            offer = 0
            offerSize = 0
        else:
            offer = self.msg['marketData']['OF'][0]['price']
            offerSize = self.msg['marketData']['OF'][0]['size']

        # en sym1 y sym2 siempre quedanel ultimo valor del mkt
        # trabajar sobre esto  2 array?
        if (sym == self.symbols[0]):
            self.sym1 = []
            self.sym1.append(timestamp)
            self.sym1.append(sym)
            self.sym1.append(bid)
            self.sym1.append(offer)
            self.sym1.append(bidSize)
            self.sym1.append(offerSize)
        else:
            self.sym2 = []
            self.sym2.append(timestamp)
            self.sym2.append(sym)
            self.sym2.append(bid)
            self.sym2.append(offer)
            self.sym2.append(bidSize)
            self.sym2.append(offerSize)
        return

    def goRobot(self):

        print("En goRobot****************")
        print("Time stamp: ", self.sym1[0], "Symbol: ", self.sym1[1], " ", self.sym1[2], "/", self.sym1[3], " ",
              self.sym1[4], "/", self.sym1[5])
        print("Time stamp: ", self.sym2[0], "Symbol: ", self.sym2[1], " ", self.sym2[2], "/", self.sym2[3], " ",
              self.sym2[4], "/", self.sym2[5])

        if (self.sym2[5] < 10):
            # completa el vol hasta 10
            print("offer < 5")
            print(self.marketId_, self.sym2[1], str(self.sym2[3]), str(10 - self.sym2[5]), "LIMIT", "SELL", "DAY",
                  "555", True)

            self.newSingleOrder(self.marketId_, self.sym2[1], str(self.sym2[3]), str(10 - self.sym2[5]), "LIMIT",
                                "SELL", "DAY", "555", "True")
        # sys.stdout.flush()

    def buildMessage(self, sym):
        return "{\"type\":\"" + self.type_ + "\",\"level\":" + self.level_ + ", \"entries\":[\"BI\", \"OF\"],\"products\":[{\"symbol\":\"" + sym + "\",\"marketId\":\"" + self.marketId_ + "\"}]}"

    def newSingleOrder(self, marketId, symbol, price, orderQty, ordType, side, timeInForce, account, cancelPrevious):
        self.url = self.activeEndpoint + "rest/order/newSingleOrder?marketId=" + marketId + "&symbol=" + symbol + "&price=" + price + "&orderQty=" + orderQty + "&ordType=" + ordType + "&side=" + side + "&timeInForce=" + timeInForce + "&account=" + account + "&cancelPrevious=" + cancelPrevious
        # &iceberg=False&displayQty=0"
        self.requestAPI()
        return simplejson.loads(self.r.content)

    def requestAPI(self):

        headers = {'X-Auth-Token': self.token}
        self.r = requests.get(self.url, headers=headers, verify=False)
        # return self.r

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