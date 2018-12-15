from flask import Flask, request
import dao
import json
import mySerial
app = Flask(__name__)
cd = dao.CardOperate

false = "1"
success = "2"
# 新用户注册
@app.route('/addUser',methods = {"POST"})
def addUser():
    result = "false"
    # 获取参数
    cardId = request.form.get("cardId", type = int, default = None)
    balance = request.form.get("balance",type = int,default= 50)
    type = request.form.get("type", type = int ,default= 1)
    # 插入数据库
    res  = cd.addUser(cd,cardId,balance,type)
    # 向串口发送数据
    if(res == "success"):
        try:
            ser.Sender(data = str(success) + str(3) + str(cardId) + str(balance))
            result = res
        except Exception as ex:
            print(ex)
    return result

@app.route('/addBlackLists',methods = {"POST"})
def addBlackLists():
    result = "false"
    cardId = request.form.get("cardId",type = int)
    res = cd.addBlackList(cd,cardId)
    if res is "success":
        result = "success"
    return result

# 获取用户扣费历史
@app.route('/getHistory',methods = {"POST"})
def getHistory():
    cardId = request.form.get("cardId",type=int)
    data = cd.getHistory(cd,cardId)
    print(data)
    str = json.dumps(data)
    return str

# 获取用户列表
@app.route('/getAllUser',methods = {"GET"})
def getAllUser():
    data = cd.getAllUser(cd)
    str = json.dumps(data)
    return str

# 获取用户充值历史
@app.route('/getBalanceHistory',methods = {"POST"})
def getBalanceHistory():
    cardId = request.form.get("cardId", type=int)
    data = cd.getBalanceHistory(cd, cardId)
    print(data)
    str = json.dumps(data)
    return str

if __name__ == '__main__':
    ser = mySerial.SerThread('com3')
    ser.start()
    app.run()
