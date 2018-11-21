import requests
import websocket
import threading
import simplejson
from time import sleep
from Classes import cSetUpEntorno as cSetup
from itertools import count #itertools es para contar la cantidad de instancias de una clase
#--------------------------
# Imports for google sheets
import gspread
from oauth2client.service_account import ServiceAccountCredentials

#1

class cSuscriptSymbol(cSetup.cEnvironment):
    _ids=count(0)
    def __init__(self,usr,pswd,account,marketID,symbols):
        self.id=next(self._ids) # se cuenta la cantidad de instancias de una clase para imprimir en gsheets

        super().__init__(usr,pswd,account)
        self.symbols = symbols
        #self.wsEndpointDemo = "ws://pbcp-remarket.cloud.primary.com.ar/"
        self.marketId_ = marketID
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
                #print("Mensajes :", self.mensajes)
                self.incomingMD()
                self.goRobot()


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

        #for i in self.symbols:
        #    if(self.sym==self.symbols[i]):


        #print("Mensaje", self.msg, __name__)
        #self.md = []
        self.md.append([self.timestamp,self.sym,self.bid,self.offer,self.bidSize,self.offerSize])
        #print("MD Array :",self.md[-1])


        return

    def goRobot(self):

        print("En goRobot**->",self.mensajes,"--",self.sym,"-->",self.bid,"/",self.offer,"    ",self.bidSize,"/",self.offerSize)
        self.printToGoogleSheets()
        return

    def printToGoogleSheets(self):
        # use creds to create a client to interact with the Google Drive API
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name('Notebooks\client_secret.json', scope)
        client = gspread.authorize(creds)

        # Find a workbook by name and open the first sheet
        # Make sure you use the right name here.

        sheet = client.open("ROFEX-API").sheet1

        # Extract and print all of the values
        # list_of_hashes = sheet.get_all_records()
        # print(list_of_hashes)

        for col in range (5):
            sheet.update_cell(self.id+3, col + 1, self.md[-1][col + 1])

        return