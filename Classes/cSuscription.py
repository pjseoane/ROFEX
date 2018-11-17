import simplejson
from Classes import cUser as usr
import websocket
import threading
from time import sleep


class cSuscription(usr.CUser):
    def __init__(self,usr,pswd,account,symbols):
        super(). __init__(usr,pswd,account)

        self.symbols=symbols
        self.mensajes=0
        self.messArray=[]
        if(self.loginSuccess):
            self.runWS()
        else:
            print ("No se logeo, salio en clase cSuscription ")

    def on_message(self, message):
        self.mensajes += 1
        try:

            # Valido Mensaje entrante
            self.msg = simplejson.loads(message)


            if (self.msg['status']=='ERROR'):
                print("Mensaje devuelto erroneo")
            else:
                print("Convertir este mensaje a array aca o en incomingMD \n:", self.msg)
                self.messArray.append(self.msg)


            msgType = self.msg['type'].upper()

            if msgType == 'MD':

                self.incomingMD()
                #self.goRobot()


            elif msgType == 'OR':
                print("En Mensaje OR")
                print(self.msg)
            else:
                print("Tipo de Mensaje Recibido No soportado: " + self.msg)

        except:
            #print("Error al procesar mensaje recibido:--->>> " + msg)
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

    def buildMessage(self, sym):
        return "{\"type\":\"" + self.type_ + "\",\"level\":" + self.level_ + ", \"entries\":[\"BI\", \"OF\"],\"products\":[{\"symbol\":\"" + sym + "\",\"marketId\":\"" + self.marketId_ + "\"}]}"

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

    if __name__ == '__main__':
        print('__main__')