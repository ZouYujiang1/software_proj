from sqlalchemy import Column, String, Integer, DateTime, Float, Boolean  # 使用的类型
from sqlalchemy.ext.declarative import declarative_base  # ORM(对象关系映射的基类）
from sqlalchemy import create_engine
from sqlalchemy import func
from sqlalchemy.orm import sessionmaker  # 会话（入口）
from sqlalchemy import or_, and_
from sqlalchemy import ForeignKey
from sqlalchemy.exc import SQLAlchemyError

import json

import datetime
from datetime import time, timedelta

import const

# 引擎
engine = create_engine("sqlite:///softwareEngineering.db", echo=False,
                       connect_args={'check_same_thread': False})  # echo是显示详细过程
# 基类，其他的类继承它
Base = declarative_base(engine)
# 会话
Session = sessionmaker(bind=engine)  # 通过对话对数据库操作，query()/add()
session = Session()


# 用于车辆排队时,对应表一
class QueuingUser(Base):
    __tablename__ = "queuingUser"

    userID = Column(Integer, ForeignKey("user.id"), comment="用户id")
    userName = Column(String(const.NAME_AND_PASSWORD_LEN), ForeignKey("user.name"), nullable=False, comment="用户姓名")
    chargingMode = Column(String(1), nullable=False, comment="充电模式")
    queueNO = Column(Integer, autoincrement=True, primary_key=True, comment="排队号码")
    requestVol = Column(Float, default=0, comment="请求充电量")
    timeOfApplyingNO = Column(DateTime, nullable=False, comment="申请排队号时间")

    # query查询的时候返回这个
    def __repr__(self):
        return '{' + f'"id":{self.userID},"name":"{self.userName}","mode":"{self.chargingMode}","No":{self.queueNO},"requestVol":{self.requestVol},"applyTime":"{self.timeOfApplyingNO}"' + '}'

    def __init__(self, userID, userName, chargingMode, requestVol, timeOfApplyingNo):
        self.userID = userID
        self.userName = userName
        self.chargingMode = chargingMode
        self.requestVol = requestVol
        self.timeOfApplyingNO = timeOfApplyingNo


# 设备信息，对应表二
class EquipmentInfo(Base):
    __tablename__ = "equipmentInfo"
    id = Column(Integer, default=1, primary_key=True)  # 方便更改
    waitingAreaCapacity = Column(Integer, default=const.WAITING_AREA_CAPACITY, comment="等候区容量")
    quickChargeNumber = Column(Integer, default=0, comment="快充桩数")
    slowChargeNumber = Column(Integer, default=0, comment="慢充桩数")
    quickChargePower = Column(Float, default=const.QUICK_CHARGE_POWER, comment="快充功率")
    slowChargePower = Column(Float, default=const.SLOW_CHARGE_POWER, comment="慢充功率")
    parkingSpaceOfChargePile = Column(Integer, default=const.NUMBER_OF_CHARGE_PILE, comment="每个充电桩车位数")

    def __repr__(self):
        return '{' + f'"waitingAreaCapacity": {self.waitingAreaCapacity}, "quickChargeNumber": {self.quickChargeNumber},"slowChargeNumber":{self.slowChargeNumber}, ' \
                     f'"quickChargePower":{self.quickChargePower}, "slowChargePower": {self.slowChargePower},"parkingSpaceOfChargePile": {self.parkingSpaceOfChargePile}' + "}"


# 记录用户信息，用于登录注册，对应表三
class User(Base):
    __tablename__ = "user"
    # 指定列的属性
    id = Column(Integer, primary_key=True, autoincrement=True, comment="用户id")
    name = Column(String(const.NAME_AND_PASSWORD_LEN), nullable=False, unique=True, comment="用户姓名")
    password = Column(String(const.NAME_AND_PASSWORD_LEN), nullable=False, comment="用户密码")
    identity = Column(String(1), default="U", comment="用户身份，U代表普通用户，M代表管理员")

    # query查询的时候回显这个
    def __repr__(self):
        return '{' + f'"id":{self.id},"name":"{self.name}","password":"{self.password}","identity":"{self.identity}"' + '}'

    def __init__(self, name, password, identity="U"):
        self.name = name
        self.password = password
        self.identity = identity


# 充电详单，对应表四
class ChargingOrder(Base):
    __tablename__ = "chargingOrder"
    orderID = Column(Integer, primary_key=True, comment="订单编号", autoincrement=True)
    userID = Column(Integer, comment="用户编号")
    userName = Column(String(const.NAME_AND_PASSWORD_LEN), comment="用户姓名")
    orderGenerationTime = Column(DateTime, comment="订单生成时间")
    idOfChargePile = Column(Integer, default=-1, comment="充电桩编号")
    actualCharge = Column(Float, default=0, comment="实际充电量")
    chargingTime = Column(Float, default=0, comment="充电时长,分钟为单位")
    startUpTime = Column(DateTime, comment="启动充电的时间")
    stopTime = Column(DateTime, comment="停止充电的时间")
    chargingCost = Column(Float, default=0, comment="充电费用")
    serviceCost = Column(Float, default=0, comment="服务费用")
    totalCost = Column(Float, default=0, comment="总费用，前面二者之和")
    # requestVol = Column(Float,default=0, comment="请求充电量")
    startingVol = Column(Float, default=0, comment="开始车的电量")

    def __init__(self, userId, userName):
        self.userID = userId
        self.userName = userName

    def __repr__(self):
        return '{' + f'"orderID":{self.orderID}, "userID":{self.userID}, "userName":"{self.userName}",' \
                     f'"orderGenerationTime":"{self.orderGenerationTime}", "idOfChargePile":{self.idOfChargePile}, "actualCharge":{self.actualCharge}, ' \
                     f'"chargingTime":{self.chargingTime}, "startUpTime":"{self.startUpTime}", "stopTime":"{self.stopTime}","chargingCost":{self.chargingCost},' \
                     f'"serviceCost":{self.serviceCost}, "totalCost":{self.totalCost}, "startingVol":{self.startingVol}' + "}"

    # 创建表


# 充电桩信息，对应表五
class ChargePileInfo(Base):
    __tablename__ = "chargePileInfo"
    chargePileID = Column(Integer, primary_key=True, comment="充电桩编号", autoincrement=True)
    working = Column(Boolean, default=True, comment="表示开或关")
    broken = Column(Boolean, default=False, comment="发生故障否")
    serviceLength = Column(Integer, default=0, comment="当前充电桩的服务车辆数，在充电区的")
    kind = Column(String(1), comment="充电桩类型，F快充，T慢充")

    # 只需要告诉添加的类型
    def __init__(self, kind):
        self.kind = kind

    '''
    def __repr__(self):
        return "{" + f'"chargePileId":{self.chargePileID},"working":"{self.working}","broken":"{self.broken}","serviceLength":{self.serviceLength},"kind":"{self.kind}"' + "}"
    '''

    def __repr__(self):
        return "{" + f'"id":{self.chargePileID},"working":"{self.working}","broken":"{self.broken}","service_length":{self.serviceLength},"kind":"{self.kind}"' + "}"


# 充电桩服务的车辆信息，对应表六
# 主键为chargePileID和userID的复合主键
class ServingCarInfoOfPile(Base):
    __tablename__ = "servingCarInfoOfPile"
    chargePileId = Column(Integer, comment="充电桩编号", primary_key=True)
    userID = Column(Integer, comment="用户ID", primary_key=True)
    carVol = Column(Float, comment="车辆的电池总容量")
    requestVol = Column(Float, comment="请求充电量")

    # queueTime = Column(Float, default=0, comment="排队时长,以分钟为单位")
    # realVol = Column(Float, comment="车辆的实时电量")

    def __init__(self, pileID, userID, carVol):
        self.chargePileId = pileID
        self.userID = userID
        self.carVol = carVol
        self.requestVol = DB.getQueuingUserInfo(self, userID)["requestVol"]

    '''
    def __repr__(self):
        return '{' + f'"chargePileId":{self.chargePileId},"userID":{self.userID}, "carVol":{self.carVol}, ' \
                     f'"requestVol":{self.requestVol},"queueTime":{self.queueTime}, "realVol":{self.realVol}' + '}'
    '''

    def __repr__(self):
        return '{' + f'"id":{self.chargePileId},"client_id":{self.userID}, "car_vol":{self.carVol}, ' \
                     f'"request_vol":{self.requestVol}' + '}'


# 报表，对应表七
# 只要有一个充电桩，就有一个对应的报表，所以在添加充电桩时生成
class ReportOfPile(Base):
    __tablename__ = "reportOfPile"
    chargePileId = Column(Integer, ForeignKey("chargePileInfo.chargePileID"), primary_key=True, comment="充电桩编号")
    reportTime = Column(DateTime, comment="生成报表的时间")
    totalUsedTimes = Column(Integer, default=0, comment="累计充电次数")
    totalUsedMinutes = Column(Float, default=0, comment="累计充电时长,分钟做单位")
    totalUsedVol = Column(Float, default=0, comment="累计充电量 ")
    totalChargeCost = Column(Float, default=0, comment="累计充电费用")
    totalServiceCost = Column(Float, default=0, comment="累计服务费用")
    totalCost = Column(Float, default=0, comment="累计总费用，前面二者之和")

    '''
    def __repr__(self):
        return '{' + f'"chargePileId":{self.chargePileId},"reportTime":"{self.reportTime}", "totalUsedTimes":{self.totalUsedTimes},"totalUsedMinutes":{self.totalUsedMinutes},' \
                     f'"totalUsedVol":{self.totalUsedVol},"totalChargeCost":{self.totalChargeCost},"totalServieceCost":{self.totalServiceCost},"totalCost":{self.totalCost}' + '}'
    '''

    def __repr__(self):
        return '{' + f'"id":{self.chargePileId},"date":"{self.reportTime}", "used_times":{self.totalUsedTimes},"used_minutes":{self.totalUsedMinutes},' \
                     f'"used_vol":{self.totalUsedVol},"charge_cost":{self.totalChargeCost},"service_cost":{self.totalServiceCost},"total_cost":{self.totalCost}' + '}'

    def __init__(self, pileID):
        self.chargePileId = pileID


Base.metadata.create_all()


class DB(object):
    # 获取电价
    # TODO:根据输入时间获取当时电价
    def getVolPrice(self, timeNow: datetime.datetime):
        timeNowHour = timeNow.hour
        if (timeNowHour >= 10 and timeNowHour < 15) or (timeNowHour >= 18 and timeNowHour < 21):
            return const.HIGH_TIME_PRICE
        elif (timeNowHour >= 7 and timeNowHour < 10)  or (timeNowHour >= 15 and timeNowHour < 18) or (timeNowHour >= 21 and timeNowHour < 23):
            return const.MID_TIME_PRICE
        elif (timeNowHour >= 0 and timeNowHour < 7) or (timeNowHour >= 23 and timeNowHour < 24):
            return const.LOW_TIME_PRICE

    # 表三相关
    # 添加用户信息，成功则返回刚插入用户的id，失败返回-1
    def addUser(self, name, password):
        global Session
        session = Session()
        if session.query(User).filter(User.name == name).first() is not None:
            return -1  # -1表示加入失败，有相同的用户名
        newUser = User(name=name, password=password)
        session.add(newUser)
        session.commit()
        return newUser.id  # 返回新加入的用户的id

    # 删除用户信息
    def deleteUser(self, userNameOrID):
        global Session
        session = Session()
        queryResult = session.query(User).filter(
            or_(User.id == userNameOrID, User.name == userNameOrID))
        for r in queryResult:
            session.delete(r)
        session.commit()
        return userNameOrID

    # 获取用户信息
    def getUserInfo(self, nameOrID):
        global Session
        session = Session()
        queryResult = session.query(User).filter(or_(User.id == nameOrID, User.name == nameOrID)).first()
        if queryResult is not None:
            return json.loads(queryResult.__repr__())
        return queryResult

    # 匹配用户密码
    def checkUserPwd(self, nameOrID, password):
        global Session
        session = Session()
        queryResult = session.query(User).filter(or_(User.id == nameOrID, User.name == nameOrID)).first()
        if queryResult is not None:
            if password == queryResult.password:
                return queryResult.id
            else:
                return 0
        else:
            return -1

    # 修改密码
    def resetUserPwd(self, nameOrID, password):
        global Session
        session = Session()
        queryResult = session.query(User).filter(or_(User.id == nameOrID, User.name == nameOrID)).first()
        if queryResult is not None:
            queryResult.password = password
            session.add(queryResult)
            session.commit()
            return queryResult.id
        else:
            return -1

    # 根据用户名求得对应id,失败返回-1
    def getUserID(self, name):
        global Session
        session = Session()
        queryResult = session.query(User).filter(User.name == name).first()
        if queryResult is not None:
            return queryResult.id
        else:
            return -1

    # 获取所有的用户信息，主要用来调试
    def getAllUserInfo(self):
        # print("所有用户信息如下：")
        query_result = session.query(User).all()
        # for result in query_result:
            # print(result)
        return query_result

    # 表一相关
    # 添加排队的用户,成功返回userid,失败返回-1
    def addQueuingUser(self, userID, userName, chargingMode, requestVol, timeOfApplyingNo):
        # 模式有误
        if chargingMode != 'F' and chargingMode != 'T':
            return -1
        # 不存在该用户
        if DB.getUserInfo(self, nameOrID=userID) is None or DB.getUserInfo(self, nameOrID=userName) is None:
            return 0
        # 重复插入
        if DB.getQueuingUserInfo(self, nameOrID=userID) is not None:
            return -2

        # carsAhead = session.query(func.max(QueuingUser.carsAhead)).scalar() + 1
        newQueuingUser = QueuingUser(userID, userName, chargingMode, requestVol, timeOfApplyingNo)
        session.add(newQueuingUser)
        session.commit()
        return newQueuingUser.queueNO  # 成功

    # 获得排队用户的信息
    def getQueuingUserInfo(self, nameOrID):
        global Session
        session = Session()
        queryResult = session.query(QueuingUser).filter(
            or_(QueuingUser.userName == nameOrID, QueuingUser.userID == nameOrID)).first()

        if queryResult is not None:
            return json.loads(queryResult.__repr__())

        return queryResult

    # 删除排队用户信息（充电结束时）
    def deleteQueuingUser(self, nameOrID):
        queryResult = session.query(QueuingUser).filter(
            or_(QueuingUser.userName == nameOrID, QueuingUser.userID == nameOrID)).first()

        if queryResult is not None:
            session.delete(queryResult)
            session.commit()
            return 1
        else:
            return 0  # 不存在这个信息

    # 修改充电模式
    def setChargeMode(self, name, newMode):
        if newMode != "T" and newMode != "F":
            return -1

        queryResult = session.query(QueuingUser).filter(QueuingUser.userName == name).first()
        if queryResult is None:
            return 0
        else:
            # 模式一样
            if newMode == queryResult.chargingMode:
                return -3
            requestVol = queryResult.requestVol
            # 删除旧的排队信息
            DB.deleteQueuingUser(self, nameOrID=name)
            # 修改充电模式要重新排队
            return DB.addQueuingUser(self, userID=DB.getUserID(self, name), userName=name,
                                     chargingMode=newMode, requestVol=requestVol,
                                     timeOfApplyingNo=datetime.datetime.now())

    # 修改请求充电量
    def setRequestVol(self, nameOrID, newVol):
        queryResult = session.query(QueuingUser).filter(
            or_(QueuingUser.userName == nameOrID, QueuingUser.userID == nameOrID)).first()
        if queryResult is None:
            return 0
        else:
            queryResult.requestVol = newVol
            session.add(queryResult)
            session.commit()
            return 1

    '''
    # 修改前面排队车辆数
    def setCarsAhead(self, nameOrID, newCars):
        queryResult = session.query(QueuingUser).filter(
            or_(QueuingUser.userName == nameOrID, QueuingUser.userID == nameOrID)).first()
        if queryResult is None:
            return 0
        else:
            queryResult.carsAhead = newCars
            session.add(queryResult)
            session.commit()
            return 1
    '''

    # 获取有所有排队用户的信息，主要用来调试
    def getAllQueuingUserInfo(self):
        # print("所有排队用户信息如下：")
        query_result = session.query(QueuingUser).all()
        # for result in query_result:
        #     print(result)
        return query_result

    # 表二相关
    # 获取设备信息
    def getEquipmentInfo(self):
        queryResult = session.query(EquipmentInfo).filter(EquipmentInfo.id == 1).first()
        if queryResult is not None:
            return json.loads(queryResult.__repr__())
        return queryResult

    # 设置等候区大小
    def setWaitingAreaCapacity(self, newCapacity):
        queryResult = session.query(EquipmentInfo).filter(EquipmentInfo.id == 1).first()

        if queryResult is None:
            return 0
        else:
            queryResult.waitingAreaCapacity = newCapacity
            session.add(queryResult)
            session.commit()
            return 1

    # 获得等候区大小
    def getWaitingAreaCapacity(self):
        queryResult = session.query(EquipmentInfo).filter(EquipmentInfo.id == 1).first()

        if queryResult is None:
            return 0
        else:
            return queryResult.waitingAreaCapacity

    # 设置快充桩数
    def setQuickChargeNumber(self, newNumber):
        queryResult = session.query(EquipmentInfo).filter(EquipmentInfo.id == 1).first()
        if queryResult is None:
            return 0
        else:
            if newNumber < queryResult.quickChargeNumber:
                return -1
            # 添加新增的充电桩
            for i in range(newNumber - queryResult.quickChargeNumber):
                DB.addPile(self, kind="F")
            return 1

    # 获得快充桩数
    def getQuickChargeNumber(self):
        queryResult = session.query(EquipmentInfo).filter(EquipmentInfo.id == 1).first()
        if queryResult is None:
            return 0
        else:
            return queryResult.quickChargeNumber

    # 快充数加一
    def addQuickChargeNumber(self):
        queryRessult = session.query(EquipmentInfo).filter(EquipmentInfo.id == 1).first()
        if queryRessult is None:
            return 0
        else:
            queryRessult.quickChargeNumber = queryRessult.quickChargeNumber + 1
            session.add(queryRessult)
            session.commit()
            return 1

    # 设置慢充桩数
    def setSlowChargeNumber(self, newNumber):
        queryResult = session.query(EquipmentInfo).filter(EquipmentInfo.id == 1).first()
        if queryResult is None:
            return 0
        else:
            if newNumber < queryResult.slowChargeNumber:
                return -1
            # 添加新增的充电桩
            for i in range(newNumber - queryResult.slowChargeNumber):
                DB.addPile(self, kind="T")
            return 1

    # 获得慢充桩数
    def getSlowChargeNumber(self):
        queryResult = session.query(EquipmentInfo).filter(EquipmentInfo.id == 1).first()
        if queryResult is None:
            return 0
        else:
            return queryResult.slowChargeNumber

    # 慢充数加一
    def addSlowChargeNumber(self):
        queryRessult = session.query(EquipmentInfo).filter(EquipmentInfo.id == 1).first()
        if queryRessult is None:
            return 0
        else:
            queryRessult.slowChargeNumber = queryRessult.slowChargeNumber + 1
            session.add(queryRessult)
            session.commit()
            return 1

    # 设置快充功率
    def setQuickChargePower(self, newPower):
        queryResult = session.query(EquipmentInfo).filter(EquipmentInfo.id == 1).first()
        if queryResult is None:
            return 0
        else:
            queryResult.quickChargePower = newPower
            session.add(queryResult)
            session.commit()
            return 1

    # 获得快充功率
    def getQuickChargePower(self):
        queryResult = session.query(EquipmentInfo).filter(EquipmentInfo.id == 1).first()
        if queryResult is None:
            return 0
        else:
            return queryResult.quickChargePower

    # 设置慢充功率
    def setSlowChargePower(self, newPower):
        queryResult = session.query(EquipmentInfo).filter(EquipmentInfo.id == 1).first()
        if queryResult is None:
            return 0
        else:
            queryResult.slowChargePower = newPower
            session.add(queryResult)
            session.commit()
            return 1

    # 获得慢充功率
    def getSlowChargePower(self):
        queryResult = session.query(EquipmentInfo).filter(EquipmentInfo.id == 1).first()
        if queryResult is None:
            return 0
        else:
            return queryResult.slowChargePower

    # 设置每个充电桩的车位数
    def setParkingSpace(self, newSpace):
        global Session
        session = Session()
        queryResult = session.query(EquipmentInfo).filter(EquipmentInfo.id == 1).first()
        if queryResult is None:
            return 0
        else:
            queryResult.parkingSpaceOfChargePile = newSpace
            session.add(queryResult)
            session.commit()
            return 1

    # 获得每个充电桩的车位数
    def getParkingSpace(self):
        queryResult = session.query(EquipmentInfo).filter(EquipmentInfo.id == 1).first()
        if queryResult is None:
            return 0
        else:
            return queryResult.parkingSpaceOfChargePile

    # 表四相关
    # 添加新的详单
    def addOrder(self, userID, userName):
        if DB.getUserInfo(self, nameOrID=userID) is None or DB.getUserInfo(self, nameOrID=userName) is None:
            return 0
        newOrder = ChargingOrder(userID, userName)
        session.add(newOrder)
        session.commit()
        return newOrder.orderID

    # 获取详单
    def getOrder(self, orderID):
        queryResult = session.query(ChargingOrder).filter(ChargingOrder.orderID == orderID).first()
        if queryResult is not None:
            return json.loads(queryResult.__repr__())
        return queryResult

    def getUsrHistoryOrders(self, nameOrID):
        queryResult = session.query(ChargingOrder).filter(
                or_(QueuingUser.userName == nameOrID, QueuingUser.userID == nameOrID)).all()
        if queryResult is not None:
            return json.loads(queryResult.__repr__())
        return queryResult

    # 停止充电时设置以下信息
    def setOrderWhenStopCharging(self, orderID, orderGenerationTime, actualCharge, chargingTime, stopTime,
                                 chargingCost, serviceCost):
        queryResult = session.query(ChargingOrder).filter(ChargingOrder.orderID == orderID).first()

        if queryResult is None:
            return 0
        queryResult.orderGenerationTime = orderGenerationTime
        queryResult.actualCharge = actualCharge
        queryResult.chargingTime = chargingTime
        queryResult.stopTime = stopTime
        queryResult.chargingCost = chargingCost
        queryResult.serviceCost = serviceCost
        queryResult.totalCost = chargingCost + serviceCost
        session.add(queryResult)
        session.commit()
        return 1

    # 开始充电时设置以下信息
    def setOrderWhenStartCharging(self, orderID, idOfChargePile, startUpTime, startingVol):
        # 检查充电桩存在否
        if DB.getPileInfo(self, chargePileID=idOfChargePile) is None:
            return -1

        queryResult = session.query(ChargingOrder).filter(ChargingOrder.orderID == orderID).first()
        if queryResult is None:
            return 0
        queryResult.idOfChargePile = idOfChargePile
        queryResult.startUpTime = startUpTime
        # queryResult.requestVol = requestVol
        queryResult.startingVol = startingVol
        session.add(queryResult)
        session.commit()
        return 1

    # 删除订单，用户看完订单后可删除
    def deleteOrder(self, userNameOrID):
        queryResult = session.query(ChargingOrder).filter(
            or_(ChargingOrder.userID == userNameOrID, ChargingOrder.userName == userNameOrID))
        for r in queryResult:
            session.delete(r)
            session.commit()

    # 获取所有订单信息，主要用来调试
    def getAllOrderInfo(self):
        # print("所有订单信息如下：")
        query_result = session.query(ChargingOrder).all()
        # for result in query_result:
        #     print(result)
        return query_result


    # 表五相关
    # 添加新的充电桩
    def addPile(self, kind):
        if kind != 'T' and kind != 'F':
            return -1

        newPile = ChargePileInfo(kind=kind)
        session.add(newPile)
        session.commit()
        # 修改对应的快充或慢充的数量
        if kind == 'F':
            DB.addQuickChargeNumber(self)
        else:
            DB.addSlowChargeNumber(self)

        # 生成相应的报表,一个充电桩一个报表
        DB.addReportForm(self, pileID=newPile.chargePileID)

        return newPile.chargePileID  # 返回新添加的id

    # 获取充电桩信息
    def getPileInfo(self, chargePileID):
        queryResult = session.query(ChargePileInfo).filter(ChargePileInfo.chargePileID == chargePileID).first()

        if queryResult is not None:
            t = json.loads(queryResult.__repr__())
            # 转换bool值
            if t.get("working") == "True":
                t["working"] = True
            else:
                t["working"] = False
            if t.get("broken") == "True":
                t["broken"] = True
            else:
                t["broken"] = False
            return t
        return queryResult

    # 关闭充电桩
    def turnOffPile(self, chargePileID):
        queryResult = session.query(ChargePileInfo).filter(ChargePileInfo.chargePileID == chargePileID).first()
        if queryResult is not None:
            queryResult.working = False
            session.add(queryResult)
            session.commit()
            return 1
        else:
            return 0

    # 打开充电桩
    def turnOnPile(self, chargePileID):
        queryResult = session.query(ChargePileInfo).filter(ChargePileInfo.chargePileID == chargePileID).first()
        if queryResult is not None:
            queryResult.working = True
            session.add(queryResult)
            session.commit()
            return 1
        else:
            return 0

    # 充电桩故障
    def setPileBroken(self, chargePileID):
        queryResult = session.query(ChargePileInfo).filter(ChargePileInfo.chargePileID == chargePileID).first()
        if queryResult is not None:
            queryResult.broken = True
            session.add(queryResult)
            session.commit()
            return 1
        else:
            return 0

    # 修复充电脏
    def setPileWork(self, chargePileID):
        queryResult = session.query(ChargePileInfo).filter(ChargePileInfo.chargePileID == chargePileID).first()
        if queryResult is not None:
            queryResult.broken = False
            session.add(queryResult)
            session.commit()
            return 1
        else:
            return 0

    # 设置服务长度
    def setServicelenOfPile(self, chargePileID, newLen):
        queryResult = session.query(ChargePileInfo).filter(ChargePileInfo.chargePileID == chargePileID).first()
        if queryResult is None:
            return 0
        else:
            # 这里需要判断是否超过最长的长度
            if newLen > DB.getEquipmentInfo(self).get("parkingSpaceOfChargePile"):
                return -1
            else:
                queryResult.serviceLength = newLen
                session.add(queryResult)
                session.commit()
                return 1

    # 服务长度加1
    def addServiceLengthOfPile(self, chargePileID):
        queryResult = session.query(ChargePileInfo).filter(ChargePileInfo.chargePileID == chargePileID).first()
        if queryResult is None:
            return 0
        else:
            if queryResult.serviceLength + 1 > DB.getEquipmentInfo(self).get("parkingSpaceOfChargePile"):
                return -1

            queryResult.serviceLength = queryResult.serviceLength + 1
            session.add(queryResult)
            session.commit()
            return 1

    # 获取所有充电桩信息
    def getAllPileInfo(self):
        # print("所有充电桩信息如下：")
        query_result = session.query(ChargePileInfo).all()
        # for result in query_result:
        #     print(result)
        return query_result

    # 表六相关
    # 最开始的实时电量为车辆的初始电量
    def addServingCarInfo(self, pileID, userID, carVol):
        if DB.getPileInfo(self, chargePileID=pileID) is None:
            return 0
        if DB.getUserInfo(self, nameOrID=userID) is None:
            return -1

        newServingCar = ServingCarInfoOfPile(pileID=pileID, userID=userID, carVol=carVol)
        try:
            session.add(newServingCar)
            session.commit()
            return 1
        except SQLAlchemyError as e:
            session.rollback()
            return -2

    # 获取服务车辆信息
    def getServingCarInfoOfPile(self, pileID):
        requestResult = session.query(ServingCarInfoOfPile).filter(ServingCarInfoOfPile.chargePileId == pileID).all()
        if len(requestResult) == 0:
            return None

        return json.loads(requestResult.__repr__())

    '''
    # 添加排队时长
    def addQueueTime(self, pileID, userID, timeToAdd):
        requestResult = session.query(ServingCarInfoOfPile).filter(
            and_(ServingCarInfoOfPile.chargePileId == pileID, ServingCarInfoOfPile.userID == userID)).first()
        if requestResult is None:
            return 0
        else:
            requestResult.queueTime = requestResult.queueTime + timeToAdd
            session.add(requestResult)
            session.commit()
            return 1

    # 设置排队时长
    def setQueueTime(self, pileID, userID, newQueueTime):
        requestResult = session.query(ServingCarInfoOfPile).filter(
            and_(ServingCarInfoOfPile.chargePileId == pileID, ServingCarInfoOfPile.userID == userID)).first()
        if requestResult is None:
            return 0
        else:
            requestResult.queueTime = newQueueTime
            session.add(requestResult)
            session.commit()
            return 1

    # 添加实时电量
    def addRealVol(self, pileID, userID, volToAdd):
        requestResult = session.query(ServingCarInfoOfPile).filter(
            and_(ServingCarInfoOfPile.chargePileId == pileID, ServingCarInfoOfPile.userID == userID)).first()
        if requestResult is None:
            return 0
        else:
            requestResult.realVol = requestResult.realVol + volToAdd
            session.add(requestResult)
            session.commit()
            return 1

    # 设置实时电量
    def setRealVol(self, pileID, userID, newRealVol):
        requestResult = session.query(ServingCarInfoOfPile).filter(
            and_(ServingCarInfoOfPile.chargePileId == pileID, ServingCarInfoOfPile.userID == userID)).first()
        if requestResult is None:
            return 0
        else:
            requestResult.realVol = newRealVol
            session.add(requestResult)
            session.commit()
            return 1
    '''
    '''
    # 修改请求充电量
    def setRequestVolInServingCar(self, pileID, userID, newRequestVol):
        requestResult = session.query(ServingCarInfoOfPile).filter(
            and_(ServingCarInfoOfPile.chargePileId == pileID, ServingCarInfoOfPile.userID == userID)).first()
        if requestResult is None:
            return 0
        else:
            requestResult.requestVol = newRequestVol
            session.add(requestResult)
            session.commit()
            return 1
    '''

    # 删除服务车辆信息
    def deleteServingCarInfo(self, pileID, userID):
        queryResult = session.query(ServingCarInfoOfPile).filter(
            and_(ServingCarInfoOfPile.chargePileId == pileID, ServingCarInfoOfPile.userID == userID)).first()
        if queryResult is None:
            return 0
        else:
            session.delete(queryResult)
            session.commit()
            return 1

    # 获取所有服务车辆信息
    def getAllServingCarInfo(self):
        # print("所有等候服务车辆信息如下：")
        query_result = session.query(ServingCarInfoOfPile).all()
        # for result in query_result:
        #     print(result)
        return query_result

    # 表七相关
    # 添加报表
    def addReportForm(self, pileID):
        # 不存在对应的充电桩
        if DB.getPileInfo(self, chargePileID=pileID) is None:
            return 0

        newReport = ReportOfPile(pileID=pileID)
        try:
            session.add(newReport)
            session.commit()
            return pileID  # 加入成功
        except SQLAlchemyError as e:
            session.rollback()
            return -1  # 已有报表

    # 获得报表信息
    def getReportForm(self, pileID):
        queryResult = session.query(ReportOfPile).filter(ReportOfPile.chargePileId == pileID).first()
        if queryResult is not None:
            return json.loads(queryResult.__repr__())
        return queryResult

    # 设置生成报表的时间
    def setReportTime(self, pileID, reportTime):
        queryResult = session.query(ReportOfPile).filter(ReportOfPile.chargePileId == pileID).first()
        if queryResult is None:
            return 0
        else:
            queryResult.reportTime = reportTime
            session.add(queryResult)
            session.commit()
            return 1

    # 添加一次充电次数
    def addTotalUsedTimes(self, pileID):
        queryResult = session.query(ReportOfPile).filter(ReportOfPile.chargePileId == pileID).first()
        if queryResult is None:
            return 0
        else:
            queryResult.totalUsedTimes = queryResult.totalUsedTimes + 1
            session.add(queryResult)
            session.commit()
            return 1

    # 添加充电时长
    def addTotalUsedMinutes(self, pileID, timeToAdd):
        queryResult = session.query(ReportOfPile).filter(ReportOfPile.chargePileId == pileID).first()
        if queryResult is None:
            return 0
        else:
            queryResult.totalUsedMinutes = queryResult.totalUsedMinutes + timeToAdd
            session.add(queryResult)
            session.commit()
            return 1

    # 添加充电量
    def addTotalUsedVol(self, pileID, volToAdd):
        queryResult = session.query(ReportOfPile).filter(ReportOfPile.chargePileId == pileID).first()
        if queryResult is None:
            return 0
        else:
            queryResult.totalUsedVol = queryResult.totalUsedVol + volToAdd
            session.add(queryResult)
            session.commit()
            return 1

    # 添加充电费用
    def addTotalChargeCost(self, pileID, costToAdd):
        queryResult = session.query(ReportOfPile).filter(ReportOfPile.chargePileId == pileID).first()
        if queryResult is None:
            return 0
        else:
            queryResult.totalChargeCost = queryResult.totalChargeCost + costToAdd
            queryResult.totalCost = queryResult.totalCost + costToAdd
            session.add(queryResult)
            session.commit()
            return 1

    # 添加服务费用
    def addTotalServiceCost(self, pileID, costToAdd):
        queryResult = session.query(ReportOfPile).filter(ReportOfPile.chargePileId == pileID).first()
        if queryResult is None:
            return 0
        else:
            queryResult.totalServiceCost = queryResult.totalServiceCost + costToAdd
            queryResult.totalCost = queryResult.totalCost + costToAdd
            session.add(queryResult)
            session.commit()
            return 1

    # 获取所有报表信息
    def getAllReportInfo(self):
        # print("所有报表信息如下：")
        query_result = session.query(ReportOfPile).all()
        # for result in query_result:
        #     print(result)
        return query_result

    # 初始化一些设备的常量
    def init(self):
        queryResult = session.query(EquipmentInfo).filter(EquipmentInfo.id == 1).first()
        # 第一次打开
        if queryResult is not None:
            session.delete(queryResult)
            # print(str(queryResult))
            session.commit()

        # 初始化设备信息
        equipmentInfo = EquipmentInfo()
        session.add(equipmentInfo)
        session.commit()
        # 添加const里声明的快充和慢充数
        # 添加快充
        for i in range(const.QUICK_CHARGE_NUMBER):
            DB.addPile(self, "F")
        # 添加慢充
        for i in range(const.SLOW_CHARGE_NUMBER):
            DB.addPile(self, "T")

        # 初始化管理员信息
        Manager1 = User(name=const.NAME1, password=const.PWD1, identity="M")
        session.add(Manager1)
        session.commit()

        Manager2 = User(name=const.NAME2, password=const.PWD2, identity="M")
        session.add(Manager2)
        session.commit()

        for i in range(30):
            User1 = User(name=str(i + 3), password="1", identity="U")
            session.add(User1)
            session.commit()

if __name__ == "__main__":
    db = DB()
    db.init()
