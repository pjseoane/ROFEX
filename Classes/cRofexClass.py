import simplejson
import requests


class cRofexSetup:
    def __init__(self,usr,pswd,account):
        self.usr = usr
        self.pswd = pswd
        self.account = account
        #self.symbols = symbols
        self.endpointDemo = "http://demo-api.primary.com.ar/"
        self.wsEndpointDemo = "ws://demo-api.primary.com.ar/"
        self.activeEndpoint = self.endpointDemo
        self.activeWSEndpoint = self.wsEndpointDemo
        self.historyOHLC_endpoint = "http://h-api.primary.com.ar/MHD/TradesOHLC/{s}/{fi}/{ff}/{hi}/{hf}"
        self.entorno = 1
        #self.s = requests.Session()
        self.type_ = "smd"
        self.level_ = "1"
        self.marketId_ = "ROFX"

    def requestAPI(url):
        # if(not login): raise PMYAPIException("Usuario no Autenticado.")
        # else:
        #    global token
        headers = {'X-Auth-Token': token}
        r = requests.get(url, headers=headers, verify=verifyHTTPs)
        return r

    def listaSegmentosDisp(self):
        url = self.activeEndpoint + "rest/segment/all"
        r = requestAPI(url)
        return simplejson.loads(r.content)

    def instrumentos(self):
        url = self.activeEndpoint + "rest/instruments/all"
        r = requestAPI(url)
        return simplejson.loads(r.content)

    def instrumentsDetailsAll(self):
        url = self.activeEndpoint + "rest/instruments/details"
        r = requestAPI(url)
        return simplejson.loads(r.content)

    def instrumentDetail(self,symbol, marketId):
        url = self.activeEndpoint + "rest/instruments/detail?symbol=" + symbol + "&marketId=" + marketId
        r = requestAPI(url)
        return simplejson.loads(r.content)

    def instrumentsByCFICode(self,CFIcode):
        url = self.activeEndpoint + "rest/instruments/byCFICode?CFICode=" + CFIcode
        r = requestAPI(url)
        return simplejson.loads(r.content)

    def instrumentsBySegments(self,segments):
        url = self.activeEndpoint + "rest/instruments/bySegment?MarketSegmentID=" + segments + "&MarketID=ROFX"
        r = requestAPI(url)
        return simplejson.loads(r.content)

    def newSingleOrder(self,marketId, symbol, price, orderQty, ordType, side, timeInForce, account, cancelPrevious):
        url = self.activeEndpoint + "rest/order/newSingleOrder?marketId=" + marketId + "&symbol=" + symbol + "&price=" + price + "&orderQty=" + orderQty + "&ordType=" + ordType + "&side=" + side + "&timeInForce=" + timeInForce + "&account=" + account + "&cancelPrevious=" + cancelPrevious

        # &iceberg=False&displayQty=0"
        r = requestAPI(url)
        return simplejson.loads(r.content)

    def newIcebergOrder(self,marketId, symbol, price, orderQty, ordType, side, timeInForce, account, cancelPrevious, iceberg,
                        displayQty):
        url = self.activeEndpoint + "rest/order/newSingleOrder?marketId=" + marketId + "&symbol=" + symbol + "&price=" + price + "&orderQty=" + orderQty + "&ordType=" + ordType + "&side=" + side + "&timeInForce=" + timeInForce + "&account=" + account + "&cancelPrevious=" + cancelPrevious + "&iceberg=" + iceberg + "&displayQty=" + displayQty

        # &iceberg=False&displayQty=0"
        r = requestAPI(url)
        return simplejson.loads(r.content)

    def newGTDOrder(self,marketId, symbol, price, orderQty, ordType, side, timeInForce, account, expireDate):
        url = self.activeEndpoint + "rest/order/newSingleOrder?marketId=" + marketId + "&symbol=" + symbol + "&price=" + price + "&orderQty=" + orderQty + "&ordType=" + ordType + "&side=" + side + "&timeInForce=GTD" + "&account=" + account + "&expireDate=" + expireDate

        r = requestAPI(url)
        return simplejson.loads(r.content)

    def replaceOrderById(self,clOrdId, proprietary, price, orderQty):
        url = self.activeEndpoint + "rest/order/replaceById?clOrdId=" + clOrdId + "&proprietary=" + proprietary + "&price=" + price + "&orderQty=" + orderQty

        r = requestAPI(url)
        return simplejson.loads(r.content)

    def cancelOrderById(self,clOrdId, proprietary):
        url = self.activeEndpoint + "rest/order/cancelById?clOrdId=" + clOrdId + "&proprietary=" + proprietary

        r = requestAPI(url)
        return simplejson.loads(r.content)

    def consultarUltEstadoOrderById(self,clOrdId, proprietary):
        url = self.activeEndpoint + "rest/order/id?clOrdId=" + clOrdId + "&proprietary=" + proprietary

        r = requestAPI(url)
        return simplejson.loads(r.content)

    def consultarAllEstadoOrderById(self,clOrdId, proprietary):
        url = self.activeEndpoint + "rest/order/allById?clOrdId=" + clOrdId + "&proprietary=" + proprietary

        r = requestAPI(url)
        return simplejson.loads(r.content)

    def consultarOrden(self,orderId):
        url = self.activeEndpoint + "rest/order/byOrderId?orderId=" + orderId

        r = requestAPI(url)
        return simplejson.loads(r.content)

    def consultarOrdenesActivas(self,accountId):
        url = self.activeEndpoint + "rest/order/actives?accountId=" + accountId

        r = requestAPI(url)
        # return r.content
        return simplejson.loads(r.content)

    def consultarOrdenesOperadas(self,accountId):
        url = self.activeEndpoint + "rest/order/filleds?accountId=" + accountId

        r = requestAPI(url)
        return simplejson.loads(r.content)

    def consultarOrdenesAllClientOrder(self,accountId):
        url = self.activeEndpoint + "rest/order/all?accountId=" + accountId

        r = requestAPI(url)
        return simplejson.loads(r.content)

    def consultarOrdenExecutionId(self,execId):
        url = self.activeEndpoint + "rest/order/byExecId?execId=" + execId

        r = requestAPI(url)
        return simplejson.loads(r.content)

    def getMarketData(self,marketId, symbol, p1, p2, p3, p4, p5, p6, p7, depth):
        url = self.activeEndpoint + "rest/marketdata/get?marketId=" + marketId + "&symbol=" + symbol + "&entries=" + p1 + "," + p2 + "," + p3 + "," + p4 + "," + p5 + "," + p6 + "," + p7 + "&depth=" + depth

        r = requestAPI(url)

        return simplejson.loads(r.content)

    def getMarketDataHist(self,marketId, symbol, date):
        url = self.activeEndpoint + "rest/data/getTrades?marketId=" + marketId + "&symbol=" + symbol + "&date=" + date

        r = requestAPI(url)

        return simplejson.loads(r.content)

    def getMarketDataHistRange(self,marketId, symbol, dateFrom, dateTo):
        url = self.activeEndpoint + "rest/data/getTrades?marketId=" + marketId + "&symbol=" + symbol + "&dateFrom=" + dateFrom + "&dateTo=" + dateTo

        r = requestAPI(url)

        return simplejson.loads(r.content)


"""
class PMYAPIException(Exception):
    def __init__(self, msg):
        self.msg = msg
    def __str__(self):
        return self.msg





# Fix API Parameter
marketID='ROFX'
timeInForce='Day'






# 2
"""
