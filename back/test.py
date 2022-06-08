# 对数据库部分的测试桩
import datetime
import json
import time

import backDB
import const

db = backDB.DB()


# 测试用户部分，对应表三
def testUser():
    id = db.addUser(name="小明", password="123456")
    if id == -1:
        print("已有同名用户")

    print(db.getUserID(name="小"))
    '''
    usrName = "小明"
    id = db.getUserInfo(usrName)["id"]
    return json.dumps({"queno":id})
    '''
    # db.getAllUserInfo()
    '''
    r = db.getUserInfo(nameOrID="小明")
    if r is None:
        print("没有该用户")
    else:
        print(type(r.get("id")))
        print(r)
    '''
    #id = db.getUserInfo(nameOrID="小明").get("id")


    '''
    id = 4
    # id = 1
    r = db.getUserInfo(nameOrID=id)
    if r is None:
        print("没有该用户")
    else:
        print(r)
    '''


# 测试排队用户，对应表一
def testQueuingUser():
    db.deleteQueuingUser(nameOrID=1)
    r = db.addQueuingUser(userID=1, userName="小明", chargingMode="T", requestVol=10,
                          timeOfApplyingNo=datetime.datetime.now())
    if r == 0:
        print("不存在该用户")
    elif r == -1:
        print('充电模式有误，只能是“T"或"F"')
    elif r == -2:
        print("这个用户已有排队信息")
    else:
        print(db.getQueuingUserInfo(nameOrID=1))

    r = db.setChargeMode(name="小明",newMode="F") # 改变充电模式会产生新的排队信息
    if r == 0:
        print("不存在该用户")
    elif r == -1:
        print('充电模式有误，只能是“T"或"F"')
    elif r == -2:
        print("这个用户已有排队信息")
    elif r == -3:
        print("模式和原来的一样")
    else:
        print(db.getQueuingUserInfo(nameOrID=1))

    # db.getAllQueuingUserInfo()



# 测试设备相关的，对应表二
def testEquipment():
    '''
    r = db.getEquipmentInfo()
    if r is None:
        print("未调用init")
    else:
        print(r)
    '''
    r = db.getParkingSpace()
    if r == 0:
        print("未调用init")
    else:
        print(r)
    db.setParkingSpace(20)
    print(db.getParkingSpace())

    '''
    r = db.getWaitingAreaCapacity()
    if r == 0:
        print("未调用init")
    else:
        print(r)
    db.setWaitingAreaCapacity(10)
    print(db.getWaitingAreaCapacity())
    '''
    '''
    r = db.setWaitingAreaCapacity(newCapacity=10)
    if r == 0:
        print("未调用init")
    else:
        print(db.getEquipmentInfo())
    '''
    '''
    r = db.setQuickChargeNumber(newNumber=11)
    if r == 0:
        print("未调用init")
    elif r ==-1:
        print("数量比原来的小，不支持修改")
    else:
        print(db.getEquipmentInfo())
    db.getAllPileInfo()
    db.getAllReportInfo()
    '''
    '''
    r = db.setSlowChargeNumber(newNumber=12)
    if r == 0:
        print("未调用init")
    elif r == -1:
        print("数量比原来的小，不支持修改")
    else:
        print(db.getEquipmentInfo())
    db.getAllPileInfo()
    db.getAllReportInfo()
    '''
    '''
    r = db.addQuickChargeNumber()
    if r == 0:
        print("未调用init")
    else:
        print(db.getEquipmentInfo())

    r = db.setSlowChargeNumber(newNumber=5)
    if r == 0:
        print("未调用init")
    else:
        print(db.getEquipmentInfo())

    r = db.addSlowChargeNumber()
    if r == 0:
        print("未调用init")
    else:
        print(db.getEquipmentInfo())

    r = db.setQuickChargePower(newPower=40)
    if r == 0:
        print("未调用init")
    else:
        print(db.getEquipmentInfo())

    r = db.setSlowChargePower(newPower=10)
    if r == 0:
        print("未调用init")
    else:
        print(db.getEquipmentInfo())

    r = db.setParkingSpace(newSpace=4)
    if r == 0:
        print("未调用init")
    else:
        print(db.getEquipmentInfo())
    '''

# 测试充电桩，对应表五
def testPile():
    print(db.getEquipmentInfo())
    '''
    r = db.addPile("M")
    if r == -1:
        print("只能是T或F")
    '''
    r = db.addPile("T")
    if r == -1:
        print("只能是T或F")
    else:
        print(db.getPileInfo(chargePileID=r))
    db.getAllPileInfo()
    print(db.getEquipmentInfo())
    print(db.getReportForm(pileID=r))
    '''
    db.setPileBroken(chargePileID=r)
    print(db.getPileInfo(chargePileID=r))
    db.turnOffPile(chargePileID=r)
    print(db.getPileInfo(chargePileID=r))

    db.setPileWork(chargePileID=r)
    print(db.getPileInfo(chargePileID=r))
    db.turnOnPile(chargePileID=r)
    print(db.getPileInfo(chargePileID=r))
    '''
    '''
    r = db.addPile("F")
    if r == -1:
        print("只能是T或F")
    print(db.getEquipmentInfo())

    r = db.getPileInfo(chargePileID=1)
    if r is None:
        print("不存在该充电桩")
    else:
        print(r)


    r = db.turnOffPile(chargePileID=1)
    if r == 0:
        print("不存在该充电桩")
    else:
        print(db.getPileInfo(chargePileID=1))

    r = db.turnOnPile(chargePileID=1)
    if r == 0:
        print("不存在该充电桩")
    else:
        print(db.getPileInfo(chargePileID=1))


    r = db.setPileBroken(chargePileID=1)
    if r == 0:
        print("不存在该充电桩")
    else:
        print(db.getPileInfo(chargePileID=1))

    r = db.setPileWork(chargePileID=1)
    if r == 0:
        print("不存在该充电桩")
    else:
        print(db.getPileInfo(chargePileID=1))
        



    r = db.setServicelenOfPile(chargePileID=1,newLen=1)
    if r == 0:
        print("不存在该充电桩")
    elif r == -1:
        print("超过最大长度")
    else:
        print(db.getPileInfo(chargePileID=1))

    print(db.getPileInfo(chargePileID=1))
    r = db.addServiceLengthOfPile(chargePileID=1)
    if r == 0:
        print("不存在该充电桩")
    elif r==-1:
        print("超过最大长度")
    else:
        print(db.getPileInfo(chargePileID=1))
    '''


# 测试报表，对应表七
def testReport():

    r = db.addReportForm(pileID=1)
    if r == 0:
        print("不存在该充电桩")
    elif r ==-1:
        print("该充电桩已存在报表")
    else:
        print(db.getReportForm(pileID=1))
    db.getAllReportInfo()
    '''
    r =db.getReportForm(pileID=1)
    if r is None:
        print("不存在报表")
    else:
        print(r)

    r = db.setReportTime(pileID=1,reportTime=datetime.datetime.now())
    if r == 0:
        print("不存在报表")
    else:
        print(db.getReportForm(pileID=1))
    '''
    '''
    print(db.getReportForm(pileID=1))
    r = db.addTotalUsedTimes(pileID=1)
    if r == 0:
        print("不存在报表")
    else:
        print(db.getReportForm(pileID=1))
    '''
    '''
    print(db.getReportForm(pileID=1))
    r = db.addTotalUsedMinutes(pileID=1,timeToAdd=10)
    if r == 0:
        print("不存在报表")
    else:
        print(db.getReportForm(pileID=1))
    '''
    '''
    print(db.getReportForm(pileID=1))
    r = db.addTotalUsedVol(pileID=1, volToAdd=123)
    if r == 0:
        print("不存在报表")
    else:
        print(db.getReportForm(pileID=1))
    '''
    '''
    print(db.getReportForm(pileID=1))
    r = db.addTotalChargeCost(pileID=1, costToAdd=10)
    if r == 0:
        print("不存在报表")
    else:
        print(db.getReportForm(pileID=1))
    '''
    '''
    print(db.getReportForm(pileID=1))
    r = db.addTotalServiceCost(pileID=1, costToAdd=20)
    if r == 0:
        print("不存在报表")
    else:
        print(db.getReportForm(pileID=1))
    '''

# 测试详单，对应表四
def testOrder():
    r = db.addOrder(userID=1, userName="小明")
    id = r
    if r == 0:
        print("用户不存在，或信息有误")
    db.getAllOrderInfo()
    '''
    r = db.getOrder(orderID=id)
    if r is None:
        print("不存在该订单")
    else:
        print(r)
    
    r = db.setOrderWhenStartCharging(orderID=id, idOfChargePile=1, startUpTime=datetime.datetime.now(), startingVol=90)
    if r == 0:
        print("订单不存在")
    elif r == -1:
        print("充电桩不存在")
    else:
        print(db.getOrder(orderID=id))

    time.sleep(5)

    r = db.setOrderWhenStopCharging(orderID=id, orderGenerationTime=datetime.datetime.now(), actualCharge=10,
                                    chargingTime=1.2, stopTime=datetime.datetime.now(), chargingCost=1, serviceCost=2)
    if r == 0:
        print("不存在订单")
    else:
        print(db.getOrder(orderID=id))

    db.deleteOrder(userNameOrID=1)
    r = db.getOrder(orderID=id)
    if r is None:
        print("不存在该订单")
    else:
        print(r)
    '''

# 测试充电桩服务车辆信息，对应表六
def testServingCar():
    # db.deleteServingCarInfo(pileID=1,userID=1)

    r = db.getServingCarInfoOfPile(pileID=1)
    if r == None:
        print("该充电桩无服务信息或不存在这个充电桩")
    else:
        print(r)

    r = db.addServingCarInfo(pileID=1, userID=1, carVol=100)
    if r == 0:
        print("不存在对应的充电桩")
    elif r == -1:
        print("不存在该用户")
    elif r == -2:
        print("已有服务信息")
    else:
        print(db.getServingCarInfoOfPile(pileID=1))
    db.getAllServingCarInfo()

    '''
    print(db.getServingCarInfoOfPile(pileID=1))
    r = db.addQueueTime(pileID=1,userID=1,timeToAdd=10)
    if r ==0:
        print("不存在服务信息")

    print(db.getServingCarInfoOfPile(pileID=1))
    '''
    '''
    print(db.getServingCarInfoOfPile(pileID=1))
    r = db.setRequestVol(pileID=1, userID=1, newRequestVol=100)
    if r == 0:
        print("不存在服务信息")

    print(db.getServingCarInfoOfPile(pileID=1))
    '''
    '''
    
    print(db.getServingCarInfoOfPile(pileID=1))
    r = db.setQueueTime(pileID=1, userID=1, newQueueTime=123)
    if r == 0:
        print("不存在服务信息")

    print(db.getServingCarInfoOfPile(pileID=1))
    
    
    print(db.getServingCarInfoOfPile(pileID=1))
    r = db.addRealVol(pileID=1, userID=1, volToAdd=12)
    if r == 0:
        print("不存在服务信息")

    print(db.getServingCarInfoOfPile(pileID=1))
    
    
    print(db.getServingCarInfoOfPile(pileID=1))
    r = db.setRealVol(pileID=1, userID=2, newRealVol=100)
    if r == 0:
        print("不存在服务信息")

    print(db.getServingCarInfoOfPile(pileID=1))
    '''
    '''
    print(db.getServingCarInfoOfPile(pileID=1))
    r = db.deleteServingCarInfo(pileID=1, userID=2)
    if r == 0:
        print("不存在服务信息")

    print(db.getServingCarInfoOfPile(pileID=1))
    '''

# 测试初始化
def testInit():
    print(db.getEquipmentInfo())
    # 打印初始化的快充
    for i in range(const.QUICK_CHARGE_NUMBER):
        print(db.getPileInfo(chargePileID=i+1))
        print(db.getReportForm(pileID=i+1))
    # 打印初始化的慢充
    for i in range(const.SLOW_CHARGE_NUMBER):
        print(db.getPileInfo(chargePileID=i + 1+const.QUICK_CHARGE_NUMBER))
        print(db.getReportForm(pileID=i + 1 + const.QUICK_CHARGE_NUMBER))


if __name__ == "__main__":
    db.init()
    # testInit()

    # testOrder()
    # testServingCar()
    # testPile()
    # testReport()
    # testPile()
    # testUser()
    testQueuingUser()
    # testEquipment()

    # testjson()


# 键值必须用双引号，数字等不用，字符串必须用双引号

def testjson():
    t = {"broken": True}
    s = json.dumps(t)
    print(s)
    '''
    t = '{"broken":"True"}'
    s = json.loads(t)
    print(s)
    '''
    '''
    if s.get("broken") == "True":
        s["broken"] = True
    print(type(s.get("broken")))
    '''
    '''
    d = '{"id":123,"name":"xiaoming"}' # 最外层用单引号

    r = json.loads(d)
    print(type(r))
    print(type(r.get("name")))
    '''


