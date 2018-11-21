import requests
import simplejson
#2


class cEnvironment():
    def __init__(self,usr,pswd,account):

        self.usr = usr
        self.pswd = pswd
        self.account = account
        #self.endpointDemo = "http://demo-api.primary.com.ar/"
        #self.wsEndpointDemo = "ws://demo-api.primary.com.ar/"
        self.endpointDemo ="http://pbcp-remarket.cloud.primary.com.ar/"
        self.wsEndpointDemo ="ws://pbcp-remarket.cloud.primary.com.ar/"
        self.activeEndpoint = self.endpointDemo
        self.activeWSEndpoint = self.wsEndpointDemo
        self.historyOHLC_endpoint = "http://h-api.primary.com.ar/MHD/TradesOHLC/{s}/{fi}/{ff}/{hi}/{hf}"
        self.entorno = 1
        self.type_ = "smd"
        self.level_ = "1"
        self.marketId_ = "ROFX"
        self.s = requests.Session()
        self.loginSuccess=False


        self.login()

    def login(self):
        # if (not self.isLogin):
        url = self.activeEndpoint + "auth/getToken"
        headers = {'X-Username': self.usr, 'X-Password': self.pswd}
        loginResponse = self.s.post(url, headers=headers, verify=False)
        # Checkeamos si la respuesta del request fue correcta, un ok va a ser un response code 200 (OK)

        if (loginResponse.ok):
            self.token = loginResponse.headers['X-Auth-Token']
            self.loginSuccess = True

            print("login() OK --->", self.token)
        else:
            print("Request Error.",__name__)
            self.loginSuccess = False

        return self.loginSuccess

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

