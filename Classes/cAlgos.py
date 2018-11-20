import threading

class cRobot():
    def __init__(self, s1,s2):

        self.s1=s1
        self.s2=s2

        self.goRobot()

    def goRobot(self):
        print (self.s1.md[-1])
        print (self.s2.md[-1])
        return



