import threading
import serial
import database

false = "1"
success = "2"
cd = database.CardOperate()

class SerThread:
    def __init__(self, Port=0):
        self.my_serial = serial.Serial()
        self.my_serial.port = Port
        self.my_serial.baudrate = 115200
        self.my_serial.timeout = 1
        self.alive = False
        self.waitEnd = None
        self.thread_read = None

    def waiting(self):
        # 等待event停止标志
        if not self.waitEnd is None:
            self.waitEnd.wait()

    def start(self):
        self.my_serial.open()

        if self.my_serial.isOpen():
            self.waitEnd = threading.Event()
            self.alive = True

            self.thread_read = threading.Thread(target=self.Reader)
            self.thread_read.setDaemon(True)

            self.thread_read.start()
            return True
        else:
            return False

    def Reader(self):
        while self.alive:
            try:
                n = self.my_serial.inWaiting()
                data = ''
                if n:
                    data = self.my_serial.read(n).decode('utf-8')
                    print("收到的数据为：",data)
                    self.Sender(self.getData(data))
                    if len(data) == 1 and ord(data[len(data) - 1]) == 113:  # 收到字母q，程序退出
                        break
            except Exception as ex:
                print(ex)
        self.waitEnd.set()
        self.alive = False
    def stop(self):
        self.alive = False
        if self.my_serial.isOpen():
            self.my_serial.close()

    def Sender(self,data):
        self.my_serial.write(data.encode('utf-8'))

    def getData(self,data):
        result = false
        type = data[0]
        featuresId = data[1]
        cardId = data[2:5]
        cost = data[5:7]
        print(cost)
        # print(type)
        # print(featuresId)
        # print(cardId)
        # print(cost)
        isVaild = cd.isVaild(cardId)
        # 判断是否为非法卡
        if isVaild is "false":
            type = "3"
            return result + featuresId + cardId + cost

        # 扣费功能
        if featuresId == "1":
            if type == "2":
                re = cd.deduceMoney(cardId,1)
            else:
                re = cd.deduceMoney(cardId,2)
            if re == "success":
                cost = cd .getBalance(cardId)
                print(cost)
                result = success
            return result + featuresId + cardId + str(cost)

        # 充值
        if featuresId =="2":
            res = cd.rechargeMoney(cardId,cost)
            if res == "success":
                cost = cd.getBalance(cardId)
                result = success
            return result + featuresId + cardId + str(cost)
