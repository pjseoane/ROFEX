import requests
import websocket
import threading
import simplejson
from time import sleep
from Classes import cSetUpEntorno as cSetup
#1

class cSuscriptSymbol(cSetup.cEnvironment):
    def __init__(self,usr,pswd,account,symbols):
        super().__init__(usr,pswd,account)
        self.symbols = symbols
        self.wsEndpointDemo = "ws://pbcp-remarket.cloud.primary.com.ar/"
        self.activeWSEndpoint = self.wsEndpointDemo
        self.messages = []
        self.md=[]
        self.mensajes = 0

        #if (self.loginSuccess):
        self.runWS()

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

                print("Sent Suscription msg", self.sym)
                print("Receiving...", )

                sleep(1)  # y nada

    def on_message(self, message):
        self.mensajes += 1
        try:
            # Valido Mensaje entrante
            self.msg = simplejson.loads(message)
            self.messages.append(self.msg)

            msgType = self.msg['type'].upper()

            if msgType == 'MD':

                #print("Pasa por msg MD: \n", self.messages[-1])
                #print("Last message :",self)
                print("Mensajes :", self.mensajes)
                self.incomingMD()
                #self.goRobot()


            elif msgType == 'OR':
                print("En Mensaje OR")
                print(self.msg)
            else:
                print("Tipo de Mensaje Recibido No soportado: " + self.msg)
        except:
            # print("Error al procesar mensaje recibido:--->>> " + msg)
            print("Error al procesar mensaje recibido:--->>> " + self.msg)

    def on_error(self, error):
        print("Salio por error")
        print(error)
        self.ws.close()

    def on_close(ws):
        print("### connection closed ###")

    def on_open(ws):
        pass
        # print("WS Conection Open...")


    def buildMessage(self, sym):
        return "{\"type\":\"" + self.type_ + "\",\"level\":" + self.level_ + ", \"entries\":[\"BI\", \"OF\"],\"products\":[{\"symbol\":\"" + sym + "\",\"marketId\":\"" + self.marketId_ + "\"}]}"


    def incomingMD(self):

        self.timestamp = self.msg['timestamp']
        self.sym = self.msg['instrumentId']['symbol']
        # Aca hay un problema si no hay bid u offer pq solo viene ['marketData']
        self.bidMsg = self.msg['marketData']['BI']
        self.offerMsg = self.msg['marketData']['OF']

        if self.bidMsg == []:
            # >No BID detected")
            self.bid = 0
            self.bidSize = 0
        else:
            self.bid = self.msg['marketData']['BI'][0]['price']
            self.bidSize = self.msg['marketData']['BI'][0]['size']

        if self.offerMsg == []:
            # >No OFFER detected")
            self.offer = 0
            self.offerSize = 0
        else:
            self.offer = self.msg['marketData']['OF'][0]['price']
            self.offerSize = self.msg['marketData']['OF'][0]['size']

        #print("Mensaje", self.msg, __name__)
        #self.md = []
        self.md.append([self.timestamp,self.sym,self.bid,self.bidSize,self.offer,self.offerSize])
        print("MD Array :",self.md[:])


        return

    def goRobot(self):

        print("En goRobot**")
        print("Mensajes ", self.mensajes)

        print("sym1")
        print("Time stamp: ", self.sym1[0], "Symbol: ", self.sym1[1], " ", self.sym1[2], "/", self.sym1[3], " ",
              self.sym1[4], "/", self.sym1[5])

        print("sym2")
        print("Time stamp: ", self.sym2[0], "Symbol: ", self.sym2[1], " ", self.sym2[2], "/", self.sym2[3], " ",
              self.sym2[4], "/", self.sym2[5])

        if (self.sym2[5] < 10):
            # completa el vol hasta 10
            print("offer < 5")
        return


