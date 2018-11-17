import simplejson
from Classes import cUser as usr

class cSuscription(usr.CUser):

    def __init__(self,symbols):

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

