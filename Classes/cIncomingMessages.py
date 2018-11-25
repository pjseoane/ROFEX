from Classes import cSetUp
import simplejson


class cIncomingMessages(cSetUp.cROFEXSuscription):
    def __init__ (self,message):
        self.message=message

        self.messages = []
        self.processMessage()


    def processMessage(self):

        try:
            # Valido Mensaje entrante
            self.msg = simplejson.loads(self.message)
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

