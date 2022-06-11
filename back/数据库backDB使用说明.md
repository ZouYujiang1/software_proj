# 数据库backDB使用说明

在添加新的充电桩时，自动增加对应类型的充电桩的数量，同时生成对应充电桩id的报表

## 一.进行初始化

1. 方法：调用init()
2. 目的：初始化和设备有关的数据，包括，等候区容量，快充桩数，慢充桩数，快充功率，慢充功率，每个充电桩车位数(即充电区每个充电桩可排队的车位数)，添加初始的充电桩，即const中定义的快充和慢充桩

## 二.用户相关，对应表三

1. 添加新用户（主要用于注册时)

   方法:addUser(name, password，identity="U"),添加成功返回新用户的id，失败返回-1，表示已有同名用户，默认为普通用户（普通用户不用写identity也行），U表示普通用户，M为管理员

2. 查看用户信息

   方法：getUserInfo(nameOrID)，根据用户名或用户id，查看用户信息，成功以json格式（字典）返回用户的id，name，password，identity，失败返回None(无该用户)
   
3. 获取所有用户信息，主要用来调试

   方法：getAllUserInfo()，打印所有用户信息
   
4. 根据用户名返回用户id

   方法：getUserID(name),成功返回对应的id，失败返回-1（不存在该用户）

## 三.设备相关，对应表二

1. 获取设备信息

   方法:getEquipmentInfo(),失败（没有调用init），返回None；成功则以字典（json)的形式返回以下字段

   - waitingAreaCapacity ：等候区容量
   - quickChargeNumber：快充桩数
   - slowChargeNumber：慢充桩数
   - quickChargePower：快充功率
   - slowChargePower：慢充功率
   - parkingSpaceOfChargePile： 每个充电桩车位数

2. 设置等候区大小

   方法：setWaitingAreaCapacity(newCapacity)，成功返回1，失败返回0（没有调用init)

3. 获得等候区大小

   方法：getWaitingAreaCapacity()，成功返回等候区大小，失败返回0

4. 设置快充桩数，只支持数量比原来的大

   方法：setQuickChargeNumber(newNumber)，成功返回1，失败返回0或-1，0表示没有调用init，-1表示新的number比原来的小

5. 获得快充桩数

   方法：getQuickChargeNumber（），成功返回快充桩数，失败返回0

4. 快充桩数加一（在加入新的快充桩的时候，数据库自己处理这个）

   方法：addQuickChargeNumber()，成功返回1，失败返回0（没用调用init)

7. 设置慢充桩数，只支持数量比原来的大

   方法：setSlowChargeNumber(newNumber)，成功返回1，失败返回0或-1,0表示没用调用init，-1表示新的number比原来的小

8. 获得慢充桩数

   方法：getSlowChargeNumber()，失败返回0，成功返回快充桩数

6. 慢充桩数加一（在加入新的慢充桩的时候，数据库自己处理这个）

   方法：addSlowChargeNumber()，成功返回1，失败返回0（没用调用init)

10. 设置快充功率

   方法：setQuickChargePower(newPower)，成功返回1，失败返回0（没用调用init)

11. 获得快充功率

    方法：getQuickChargePower()，成功返回快充功率，失败返回0

12. 设置慢充功率

    方法：setSlowChargePower(newPower)，成功返回1，失败返回0（没用调用init)

13. 获得慢充功率

    方法：getSlowChargePower()，成功否返回慢充哦功率，失败返回0

9. 设置每个充电桩车位数（充电区的）

   方法：setParkingSpace(newSpace)，成功返回1，失败返回0（没用调用init)
   
15. 获取每个充电桩的车位数

    方法：getParkingSpace()，成功返回车位数，失败返回0

## 四.排队用户相关，对应表一

1. 添加新的排队用户信息

   方法：addQueuingUser(userID, userName, chargingMode, requestVol, timeOfApplyingNo)，成功返回新的排队号，失败返回-1或0或-2，-1表示充电模式有误（不是‘T’和‘F'),0表示不存在该用户（用户id或名字出错），-2表示重复插入同一个用户的排队信息

2. 获取排队用户的信息

   方法:getQueuingUserImfo(nameOrID)，失败返回None,成功以json格式返回以下字段

   - id，用户id
   - name，用户名字
   - mode，充电模式
   - No，充电号
   - requestVol，请求充电量
   - applyTime，申请号码的时间（字符串型）

3. 删除排队用户信息（开始充电时即可删除）

   方法：deleteQueuingUser(nameOrID)，成功返回1，失败返回0（不存在用户的信息）
   
4. 改变充电模式

   方法：setChargeMode(name,newMode)，成功返回新的排队号（更改模式会重新生成新的排队信息，见详细设计），失败返回-1或0或-3，-1表示充电模式有误，0表示无对应的排队信息，-3表示新的模式和原来的一样

5. 修改请求充电量

   方法：setRequestVol(nameOrID,newVol)，成功返回1，失败返回0

5. 获取所有的排队用户的信息，主要用来调试

   方法：getAllQueuingUserInfo()，简单打印

   

## 五.充电桩相关，对应表五

1. 增加新的充电桩

   方法：addPile(kind)，成功返回新插入的充电桩的id，失败返回-1（kind有误，只能是F或T，F快充，T慢充）

2. 获取充电桩信息

   方法：getPileInfo(chargePileID)，失败返回None,成功以json的格式返回以下字段

   - chargePileId 充电桩编号
   - working，开或关（True表示打开）
   -  broken，故障否（True表示故障）
   - serviceLength，当前充电桩的充电区的车辆数
   -  kind，类型，快充或慢充

3. 关闭充电桩

   方法：turnOffPile(chargePileID)，成功返回1，失败返回0（不存在该充电桩）

4. 打开充电桩

   方法：turnOnPile(chargePileID)，成功返回1，失败返回0

5. 设置充电桩故障

   方法：setPileBroken(chargePileID)，成功返回1，失败返回0

6. 修复充电桩的故障（充电桩恢复工作）

   方法：setPileWork(chargePileID)，成功返回1，失败返回0

7. 对充电桩服务车辆数加一

   方法：addServiceLengthOfPile(chargePileID),成功返回1，失败返回0或-1,0表示不存在该充电桩，-1表示设置的长度大于最大长度（车位数）

8. 设置充电桩服务车辆数（在充电区排队的），应该主要使用上一个方法

   方法：setServicelenOfPile( chargePileID, newLen)，成功返回1，失败返回0或-1,0表示不存在该充电桩，-1表示设置的长度大于最大长度（车位数）
   
9. 获取所有的充电桩信息

   方法：getAllPileInfo()，简单打印

## 六.报表相关，对应表七

1. 添加新的报表（每一个充电桩对应一个报表，在添加充电桩时添加对应报表，数据库自动添加报表）

   方法：addReportForm(pileID)，成功返回pileID，失败返回0或-1，0表示不存在这个充电桩，-1表示同一个充电桩加入多次报表

2. 获取报表信息

   方法：getReportForm(pileID)，失败返回None，表示不存在对应的报表，成功以json格式返回以下字段：

   - chargePileId 充电桩编号
   - reportTime 报表生成的时间
   - totalUsedTimes 总的使用次数
   - totalUsedMinutes 总的使用时间（分钟为单位）
   - totalUsedVol 总的充电量
   - totalChargeCost 总的充电费用
   - totalServieceCost 总的服务费用
   - totalCost 总的费用

3. 设置报表的生成时间

   方法：setReportTime(pileID, reportTime)，成功返回1，失败返回0（不存在报表）

4. 添加一次总的充电次数

   方法：addTotalUsedTimes(pileID)，成功返回1，失败返回0

5. 添加充电时长

   方法：addTotalUsedMinutes(pileID, timeToAdd)，成功返回1，失败返回0

6. 添加充电量

   方法：addTotalUsedVol(pileID, volToAdd)，成功返回1，失败返回0

7. 添加充电费用

   方法：addTotalChargeCost(pileID, costToAdd)，成功返回1，失败返回0

8. 添加服务费用

   方法：addTotalServiceCost(pileID, costToAdd)，成功返回1，失败返回0
   
9. 获取所有的报表信息

   方法：getAllReportInfo()，简单打印



## 七.充电桩服务车辆信息，对应表六

1. 添加等候服务车辆信息

   方法：addServingCarInfo(pileID, userID, carVol)，carVol车辆总的电池容量，成功返回1，失败返回0或-1或-2,0表示不存在对应的充电桩，-1表示不存在对应的用户，-2表示重复插入（同一个充电桩，同一个用户）

2. 获取某个充电桩等候服务的车辆信息

   方法：getServingCarInfoOfPile(pileID)，返回None表示充电桩还没有服务信息，或者充电桩不存在,成功以列表的形式返回结果，列表的元素包含以下信息（以下信息存为json格式）

   - chargePileId 充电桩编号
   - userID 用户id
   - carVol 车辆总电量
   - requestVol 请求电量

8. 删除充电桩服务车辆信息（应该在充电结束时，适时删除，不需要这个信息的时候）

   方法：deleteServingCarInfo(pileID, userID)，成功返回1，失败返回0(不存在服务信息)
   
9. 获取所有等候服务的车辆信息

   方法：getAllServingCarInfo（），简单打印



## 八.充电详单，对应表四

1. 添加充电详单

   方法：addOrder(userID, userName)，失败返回0（用户信息不存在，或其中之一有误），成功返回新添加的充电详单的id（上层应避免重复添加同一个用户的订单，应保存最新对应用户的详单编号，便于之后的操作）

2. 获取订单信息

   方法：getOrder(orderID)，失败返回None(没有该订单),成功以接送格式返回以下信息：

   - orderID 订单编号
   - userID 用户id
   - userName 用户姓名
   - orderGenerationTime 订单生成时间
   - idOfChargePile 充电桩编号
   - actualCharge 实际充电量
   - chargingTime 充电时长
   - startUpTime 开始充电时间
   - stopTime 停止充电时间
   - chargingCost 充电费用
   - serviceCost 服务费用
   - totalCost 总费用
   - startingVol 初始的电量

3. 开始充电时设置的信息

   方法：setOrderWhenStartCharging(orderID,idOfChargePile, startUpTime,  startingVol)，成功返回1，失败返回0或-1,0表示不存在订单，-1表示不存在对应的充电桩

4. 停止充电时设置的信息

   方法：setOrderWhenStopCharging(self, orderID, orderGenerationTime, actualCharge, chargingTime, stopTime,chargingCost, serviceCost)，成功返回1，失败返回0（不存在订单）

5. 删除订单，结束充电时，打印订单之后

   方法：deleteOrder(userNameOrID)，删除对应的所有订单

6. 获取所有订单信息

   方法：getAllOrderInfo（），简单打印

   

## 九.一些说明

1. 由于删除充电桩比较麻烦，所以只支持添加新的充电桩，故设置快充和慢充的数量时，新的数量应比原来的大
2. 上层应尽量做正确的操作，不清楚返回值的时候打印看一下，对应说明文档
3. 充电桩报表在添加充电桩时自动添加，不用上层调用，同时自动添加对应的快充或慢充桩的数量（加一），也不用上层调用
4. 部分初始值是没有意义的

## 十.一些信息的添加和删除的时刻

1. 添加用户信息在注册的时候
2. 添加服务车辆信息在开始充电时（或进入充电区）
3. 删除排队信息在添加新的服务车辆信息之后（或修改充电模式时，这个数据库自己处理）
4. 添加排队信息在进入等候区时
5. 添加充电详单在开始充电时，结束时更新
6. 删除订单在打印订单之后
7. 删除服务车辆信息在结束充电时



 

 

 

 

 

 

 

 

 

 

 

 

 

 

 

 

 

 

 

 

 

 

 

 

 

 

 

 

 

 

 

 













