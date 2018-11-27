import requests
import simplejson
from itertools import count #itertools es para contar la cantidad de instancias de una clase
import websocket
import threading
from time import sleep

# Imports for google sheets
import gspread
from oauth2client.service_account import ServiceAccountCredentials


class cROFEXSetUp():
    def __init__(self):

        self.usr = "pjseoane232"
        self.pswd = "AiZkiC5#"
        self.account = "REM232"
        endpointDemo = "http://pbcp-remarket.cloud.primary.com.ar/"
        wsEndpointDemo = "ws://pbcp-remarket.cloud.primary.com.ar/"
        self.activeEndpoint = endpointDemo
        self.activeWSEndpoint = wsEndpointDemo
        historyOHLC_endpoint = "http://h-api.primary.com.ar/MHD/TradesOHLC/{s}/{fi}/{ff}/{hi}/{hf}"
        self.entorno = 1
        self.type_ = "smd"
        self.level_ = "1"
        self.marketId_ = "ROFX"
        self.s = requests.Session()
        loginSuccess = False
        #----------------------------------------------------------------------
        #set up para google sheets
        # use creds to create a client to interact with the Google Drive API
        scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
        # creds = ServiceAccountCredentials.from_json_keyfile_name('Notebooks\client_rofex.json', scope)
        creds = ServiceAccountCredentials.from_json_keyfile_name('C:/Users/pauli/Documents/Python Projects/ROFEX/Classes/client_rofex.json', scope)
        client = gspread.authorize(creds)

        # Find a workbook by name and open the first sheet
        # Make sure you use the right name here.

        self.sheet = client.open("ROFEX-API").sheet1

        # Extract and print all of the values
        # list_of_hashes = sheet.get_all_records()
        # print(list_of_hashes)
        self.sheet.update_cell(1, 1, "Hello World V6.2!")
        #----------------------------------------------------------------------

        self.login()


    def login(self):
        # if (not self.isLogin):
        url = self.activeEndpoint + "auth/getToken"
        headers = {'X-Username': self.usr, 'X-Password': self.pswd}
        loginResponse = self.s.post(url, headers=headers, verify=False)
        # Checkeamos si la respuesta del request fue correcta, un ok va a ser un response code 200 (OK)

        if (loginResponse.ok):
            self.token = loginResponse.headers['X-Auth-Token']
            loginSuccess = True

            print("login() OK --->", self.token)
        else:
            print("Request Error.",__name__)
            loginSuccess = False

        return loginSuccess

    def requestAPI(self):
        headers = {'X-Auth-Token': self.token}
        self.r = requests.get(self.url, headers=headers, verify=False)

    def retReq(self):
        self.requestAPI()
        return simplejson.loads(self.r.content)

    def instrumentos(self):
        self.url = self.activeEndpoint + "rest/instruments/all"
        return self.retReq()

    def instrumentDetail(self,symbol, marketId):
        self.url = self.activeEndpoint + "rest/instruments/detail?symbol=" + symbol + "&marketId=" + marketId
        return self.retReq()

    def instrumentsDetailsAll(self):
        self.url = self.activeEndpoint + "rest/instruments/details"
        return self.retReq()

    def newSingleOrder(self, marketId, symbol, price, orderQty, ordType, side, timeInForce, account, cancelPrevious):
        self.url = self.activeEndpoint + "rest/order/newSingleOrder?marketId=" + marketId + "&symbol=" + symbol + "&price=" + price + "&orderQty=" + orderQty + "&ordType=" + ordType + "&side=" + side + "&timeInForce=" + timeInForce + "&account=" + account + "&cancelPrevious=" + cancelPrevious
        return self.retReq()

    def listaSegmentosDisp(self):
        self.url = self.activeEndpoint + "rest/segment/all"
        return self.retReq()

    def instrumentsByCFICode(self,CFIcode):
        self.url = self.activeEndpoint + "rest/instruments/byCFICode?CFICode=" + CFIcode
        return self.retReq()

    def instrumentsBySegments(self,segments):
        self.url = self.activeEndpoint + "rest/instruments/bySegment?MarketSegmentID=" + segments + "&MarketID=ROFX"
        return self.retReq()

    def newIcebergOrder(self, marketId, symbol, price, orderQty, ordType, side, timeInForce, account, cancelPrevious,
                        iceberg,
                        displayQty):

        self.url = self.activeEndpoint + "rest/order/newSingleOrder?marketId=" + marketId + "&symbol=" + symbol + "&price=" + price + "&orderQty=" + orderQty + "&ordType=" + ordType + "&side=" + side + "&timeInForce=" + timeInForce + "&account=" + account + "&cancelPrevious=" + cancelPrevious + "&iceberg=" + iceberg + "&displayQty=" + displayQty
        return self.retReq()

    def newGTDOrder(self,marketId, symbol, price, orderQty, ordType, side, timeInForce, account, expireDate):
        self.url = self.activeEndpoint + "rest/order/newSingleOrder?marketId=" + marketId + "&symbol=" + symbol + "&price=" + price + "&orderQty=" + orderQty + "&ordType=" + ordType + "&side=" + side + "&timeInForce=GTD" + "&account=" + account + "&expireDate=" + expireDate
        return self.retReq()

    def replaceOrderById(self,clOrdId, proprietary, price, orderQty):
        self.url = self.activeEndpoint + "rest/order/replaceById?clOrdId=" + clOrdId + "&proprietary=" + proprietary + "&price=" + price + "&orderQty=" + orderQty
        return self.retReq()

    def cancelOrderById(self, clOrdId, proprietary):
        self.url = self.activeEndpoint + "rest/order/cancelById?clOrdId=" + clOrdId + "&proprietary=" + proprietary
        return self.retReq()

    def consultarUltEstadoOrderById(self, clOrdId, proprietary):
        self.url = self.activeEndpoint + "rest/order/id?clOrdId=" + clOrdId + "&proprietary=" + proprietary
        return self.retReq()

    def consultarAllEstadoOrderById(self, clOrdId, proprietary):
        self.url = self.activeEndpoint + "rest/order/allById?clOrdId=" + clOrdId + "&proprietary=" + proprietary
        return self.retReq()

    def consultarOrden(self,orderId):
        self.url = self.activeEndpoint + "rest/order/byOrderId?orderId=" + orderId
        return self.retReq()

    def consultarOrdenesActivas(self,accountId):
        self.url = self.activeEndpoint + "rest/order/actives?accountId=" + accountId
        return self.retReq()

    def consultarOrdenesOperadas(self,accountId):
        self.url = self.activeEndpoint + "rest/order/filleds?accountId=" + accountId
        return self.retReq()

    def consultarOrdenesAllClientOrder(self,accountId):
        self.url = self.activeEndpoint + "rest/order/all?accountId=" + accountId
        return self.retReq()

    def consultarOrdenExecutionId(self, execId):
        self.url = self.activeEndpoint + "rest/order/byExecId?execId=" + execId
        return self.retReq()

    def getMarketData(self,marketId, symbol, p1, p2, p3, p4, p5, p6, p7, depth):
        self.url = self.activeEndpoint + "rest/marketdata/get?marketId=" + marketId + "&symbol=" + symbol + "&entries=" + p1 + "," + p2 + "," + p3 + "," + p4 + "," + p5 + "," + p6 + "," + p7 + "&depth=" + depth
        return self.retReq()

    def getMarketDataHist(self,marketId, symbol, date):
        self.url = self.activeEndpoint + "rest/data/getTrades?marketId=" + marketId + "&symbol=" + symbol + "&date=" + date
        return self.retReq()

    def getMarketDataHistRange(self,marketId, symbol, dateFrom, dateTo):
        self.url = self.activeEndpoint + "rest/data/getTrades?marketId=" + marketId + "&symbol=" + symbol + "&dateFrom=" + dateFrom + "&dateTo=" + dateTo
        return self.retReq()

class cROFEXSuscription(cROFEXSetUp):
    _ids = count(0)
    def __init__(self,symbols):
        self.id = next(self._ids)  # se cuenta la cantidad de instancias de una clase para imprimir en gsheets
        super().__init__()

        self.symbols=symbols

        #self.test()
        self.messages = []
        self.md = []
        self.numMessages = 0



        self.runWS()

    def test(self):
        print(self.token)
        print(self.usr)
        print(self.symbols)

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
        self.numMessages += 1

        try:
            # Valido Mensaje entrante
            self.msg = simplejson.loads(message)
            self.messages.append(self.msg)

            msgType = self.msg['type'].upper()

            if msgType == 'MD':

                # print("Pasa por msg MD: \n", self.messages[-1])
                # print("Last message :",self)
                # print("Mensajes :", self.mensajes)
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
        print("Salio por error: ", error)
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

        # for i in self.symbols:
        #    if(self.sym==self.symbols[i]):

            # print("Mensaje", self.msg, __name__)
            # self.md = []
            self.md.append([self.timestamp, self.sym, self.bid, self.offer, self.bidSize, self.offerSize])
            # print("MD Array :",self.md[-1])
            return

    def goRobot(self):

        #print("En goRobot***->",self.numMessages,"--",self.sym,"-->",self.bid,"/",self.offer,"    ",self.bidSize,"/",self.offerSize)
        print ("En goRobot md ****->", self.md[-1])
        #self.printToGoogleSheets()
        return
    def printToGoogleSheets(self):
        # use creds to create a client to interact with the Google Drive API
        #scope = ['https://spreadsheets.google.com/feeds',
         #        'https://www.googleapis.com/auth/drive']
        #creds = ServiceAccountCredentials.from_json_keyfile_name('Notebooks\client_rofex.json', scope)
        #creds = ServiceAccountCredentials.from_json_keyfile_name('Classes/client_rofex.json', scope)
        #client = gspread.authorize(creds)

        # Find a workbook by name and open the first sheet
        # Make sure you use the right name here.

        #sheet = client.open("ROFEX-API").sheet1

        # Extract and print all of the values
        # list_of_hashes = sheet.get_all_records()
        # print(list_of_hashes)
        #sheet.update_cell(1, 1, "Hello World V4.1!")
        #Aca hacer un pop() de md e imprimir len de md a ver cuantos elementos saltea la stack

        lastInStack=self.md[-1]
        #lastInStack=self.md.pop()
        for col in range (5):
            self.sheet.update_cell(self.id + 3, col + 1, self.md[-1][col + 1])
            self.sheet.update_cell(self.id + 3, col + 1, lastInStack[col + 1])
            self.sheet.update_cell(self.id + 3, 7, len(self.md))
        return
