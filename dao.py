import pymysql

def singleton(cls):
    instance = cls()
    instance.__call__ = lambda: instance
    return instance

@singleton
class Mysql():
    def __init__(self):
        self.connection = pymysql.connect("localhost", "root", "", "card")
    def getConnect(self):
        return self.connection

class CardOperate():
    # 新卡注册
    def addUser(self,cardId,balance,type):
        result = "false"
        try:
            db = Mysql.getConnect()
            cursor = db.cursor()
            cursor.execute("insert into userinfo(cardId,balance,type) value (%s,%s,%s)",(cardId,balance,type))
            cursor.close()
            db.commit()
            result = "success"
        except Exception as ex:
            print(ex)
        return result

    # 将用户加入黑名单
    def addBlackList(self,cardId):
        result = "false"
        try:
            db = Mysql.getConnect()
            cursor = db.cursor()
            re = cursor.execute("update userinfo set type = '3' where cardId = (%s) ", cardId)
            cursor.close()
            if re is 1:
                result = "success"
        except Exception as ex:
            print(ex)
        return result


    # 扣费
    def deduceMoney(self,cardId,cost):
        result = "false"
        db = Mysql.getConnect()
        cursor = db.cursor()
        res = CardOperate.isEnough(self,cardId,cost)
        if res == "success":
            try:
                cursor.execute("update userinfo set balance = (balance - %s) where cardId = %s ", (cost, cardId))
                cursor.execute("insert into history(cardId,cost) value (%s,%s)", (cardId, cost))
                cursor.close()
                db.commit()
                result = "success"
            except:
                import traceback
                traceback.print_exc()
                # 发生错误时会滚
                db.rollback()
            finally:
                # 关闭游标连接
                cursor.close()
                return result
        else:
            return result

    # 充值
    def rechargeMoney(self,cardId,amount):
        result = "false"
        db = Mysql.getConnect()
        cursor = db.cursor()
        try:
            cursor.execute("update userinfo set balance = (balance + %s) where cardId = %s ", (amount, cardId))
            cursor.execute("insert into balance_history(cardId,cost) value (%s,%s)", (cardId, amount))
            cursor.close()
            db.commit()
            result = "success"
        except:
            import traceback
            traceback.print_exc()
            # 发生错误时会滚
            db.rollback()
        finally:
            # 关闭游标连接
            cursor.close()
            return result

    # 所有用户查询
    def getAllUser(self):
        db = Mysql.getConnect()
        cursor = db.cursor(cursor=pymysql.cursors.DictCursor)
        cursor.execute("select cardId,balance,type from userinfo")
        data = cursor.fetchall()
        cursor.close()
        return data

    # 获取扣费历史
    def getHistory(self,cardId):
        db = Mysql.getConnect()
        cursor = db.cursor(cursor= pymysql.cursors.DictCursor)

        cursor.execute("select cardId,cost,CAST(time AS CHAR) AS time from history where cardId = %s ",cardId)
        data = cursor.fetchall()
        cursor.close()
        return data

    # 余额是否充足
    def isEnough(self,cardId,cost):
        db = Mysql.getConnect()
        result = "false"
        cursor = db.cursor()
        cursor.execute("select * from userinfo where balance >= %s and cardId = %s ",(cost,cardId))
        data = cursor.fetchall()
        cursor.close()
        if len(data):
            result = "success"
        return result

    # 用户是否合法
    def isVaild(self,cardId):
        db = Mysql.getConnect()
        result = "false"
        cursor = db.cursor()
        cursor.execute("select * from userinfo where cardId = %s and type <> '3' ", cardId)
        data = cursor.fetchall()
        cursor.close()
        if len(data):
            result = "success"
        return result

    # 获得余额
    def getBalance(self,cardId):
        db = Mysql.getConnect()
        cursor = db.cursor()
        cursor.execute("select balance from userinfo where cardId = %s",cardId)
        data = cursor.fetchone()
        cursor.close()
        return data[0]

    def getBalanceHistory(self,cardId):
        db = Mysql.getConnect()
        cursor = db.cursor(cursor=pymysql.cursors.DictCursor)

        cursor.execute("select cardId,cost,CAST(time AS CHAR) AS time from balance_history where cardId = %s ", cardId)
        data = cursor.fetchall()
        cursor.close()
        return data


