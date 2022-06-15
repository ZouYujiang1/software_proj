from cmath import inf
import backDB
from typing import Tuple


class UserStatus(object):
    def __init__(self, waiting_number: int, request_vol: int, charging_mode: str, status: int = -1) -> None:
        self.waiting_number = waiting_number
        self.request_vol = request_vol
        self.charging_mode = charging_mode
        self.status = status # -1：等待区 -2：优先等待区 >=0：充电区


class Dispatcher(object):
    def __init__(self, db: backDB.DB) -> None:
        self.db = db
        self.fast_queue = []  # 快充队列，保存用户名
        self.slow_queue = []  # 慢充队列，保存用户名
        self.fast_pri_queue = []  # 快充优先队列，保存用户名
        self.slow_pri_queue = []  # 慢充优先队列，保存用户名
        self.user_status: dict[str, UserStatus] = dict()  # 用户名到 UserStatus 的映射
        self.charger_queue: dict[int, list[str]
                                 ] = dict()  # 充电桩ID->充电桩队列，队列中保存用户名
        self.charger_mode: dict[int, str] = dict()  # 充电桩ID->充电模式（'T'/'F'）
        self.charger_vol = dict()  # 充电桩ID->请求电量
        self.waiting_fast_car = 0
        self.waiting_slow_car = 0
        self.avai_slow_charger = 0
        self.avai_fast_charger = 0
        self.charger_down_dispatch_mode = 0

    def carStatus(self, username: str) -> Tuple[int, int]:
        """获取车辆状态

        Args:
            username (str): 用户名

        Returns:
            tuple[int, int]: 车辆状态 第一位：0：充电中 1：充电区等待中 2：等待队列中 3：优先等待队列中；第二位：充电桩ID
        """
        status = self.user_status[username].status
        if status == -1:
            return 2, 0
        elif status == -2:
            return 3, 0
        else:
            if self.charger_queue[status][0] == username:
                return 0, status
            else:
                return 1, status

    def available(self) -> bool:
        """判断等候区是否有空位

        Returns:
            bool: 有/无空位
        """
        return self.waiting_fast_car + self.waiting_slow_car < self.db.getWaitingAreaCapacity()

    def addCar(self, waiting_number: int, username: str, charging_mode: str, request_vol: int) -> None:
        """向等待区添加车

        Args:
            waiting_number (int): 排队号
            username (str): 用户名 
            charging_mode (str): 充电模式
            request_vol (int): 充电量
        """
        if charging_mode == 'T':
            self.user_status[username] = UserStatus(
                waiting_number,  request_vol, charging_mode)
            self.slow_queue.append(username)
            self.waiting_slow_car += 1
        elif charging_mode == 'F':
            self.user_status[username] = UserStatus(
                waiting_number, request_vol, charging_mode)
            self.fast_queue.append(username)
            self.waiting_fast_car += 1
        else:
            return
        self.__dispatch(charging_mode)

    def exitCar(self, username: str) -> None:
        """有车离开

        Args:
            username (str): 用户名
        """
        status = self.user_status.get(username)
        if status is None:
            return
        if status.status == -1:
            if status.charging_mode == 'T':
                self.slow_queue.remove(username)
                self.waiting_slow_car -= 1
            else:
                self.fast_queue.remove(username)
                self.waiting_fast_car -= 1
        elif status.status == -2:
            if status.charging_mode == 'T':
                self.slow_pri_queue.remove(username)
                self.waiting_slow_car -= 1
            else:
                self.fast_pri_queue.remove(username)
                self.waiting_fast_car -= 1
        else:
            if not self.__chargerQueueFull(status.status):
                if status.charging_mode == 'T':
                    self.avai_slow_charger += 1
                else:
                    self.avai_fast_charger += 1
            self.charger_queue[status.status].remove(username)
            self.charger_vol[status.status] -= status.request_vol
        del self.user_status[username]

    def changeChargePower(self, username: str, request_vol: int) -> None:
        """改变充电量

        Args:
            username (str): 用户名
            request_vol (int): 新的充电量
        """
        self.user_status[username].request_vol = request_vol

    def newCharger(self, charger_ID: int, charging_mode: str) -> None:
        """新的充电桩开启

        Args:
            charger_ID (int): 新的充电桩ID
            charging_mode (str): 充电桩的充电模式
        """
        if self.charger_mode.get(charger_ID) is not None:
            return
        self.charger_mode[charger_ID] = charging_mode
        self.charger_vol[charger_ID] = 0
        self.charger_queue[charger_ID] = []
        if charging_mode == 'T':
            self.avai_slow_charger += 1
        else:
            self.avai_fast_charger += 1
        self.__batchDispatch(charging_mode)

    def onCharger(self, charger_ID: int) -> None:
        """充电桩恢复

        Args:
            charger_ID (int): 恢复充电桩ID
        """
        charging_mode = self.charger_mode.get(charger_ID)
        if charging_mode is None:
            return
        self.charger_vol[charger_ID] = 0
        self.charger_queue[charger_ID] = []
        if charging_mode == 'T':
            self.avai_slow_charger += 1
        else:
            self.avai_fast_charger += 1
        if charging_mode == 'T':
            new_queue: list[tuple[int, str]] = []
            for username in self.slow_queue:
                new_queue.append(
                    (self.user_status[username].waiting_number, username))
            for k, v in self.charger_queue.items():
                if k == charger_ID or self.charger_mode[k] != charging_mode:
                    continue
                while len(v) > 1:
                    username = v.pop()
                    self.user_status[username].status = -1
                    self.waiting_slow_car += 1
                    self.charger_vol[k] -= self.user_status[username].request_vol
                    new_queue.append(
                        (self.user_status[username].waiting_number, username))
            new_queue.sort()
            self.slow_queue = [i[1] for i in new_queue]
        else:
            new_queue: list[tuple[int, str]] = []
            for username in self.fast_queue:
                new_queue.append(
                    (self.user_status[username].waiting_number, username))
            for k, v in self.charger_queue.items():
                if k == charger_ID or self.charger_mode[k] != charging_mode:
                    continue
                while len(v) > 1:
                    username = v.pop()
                    self.user_status[username].status = -1
                    self.waiting_fast_car += 1
                    self.charger_vol[k] -= self.user_status[username].request_vol
                    new_queue.append(
                        (self.user_status[username].waiting_number, username))
            new_queue.sort()
            self.fast_queue = [i[1] for i in new_queue]
        self.__batchDispatch(charging_mode)

    def offCharger(self, charger_ID: int)->None:
        """充电桩故障

        Args:
            charger_ID (int): 故障充电桩ID
        """
        del self.charger_vol[charger_ID]
        charging_mode = self.charger_mode[charger_ID]
        if charging_mode == 'T':
            if self.charger_down_dispatch_mode == 0:
                for username in self.charger_queue[charger_ID]:
                    self.user_status[username].status = -2
                    self.waiting_slow_car += 1
                    self.slow_pri_queue.append(username)
            else:
                new_queue: list[tuple[int, str]] = []
                for username in self.slow_queue:
                    new_queue.append(
                        (self.user_status[username].waiting_number, username))
                for k, v in self.charger_queue.items():
                    if k == charger_ID or self.charger_mode[k] != charging_mode:
                        continue
                    while len(v) > 1:
                        username = v.pop()
                        self.user_status[username].status = -1
                        self.waiting_slow_car += 1
                        self.charger_vol[k] -= self.user_status[username].request_vol
                        new_queue.append(
                            (self.user_status[username].waiting_number, username))
                new_queue.sort()
                self.slow_queue = [i[1] for i in new_queue]
            if not self.__chargerQueueFull(charger_ID):
                self.avai_slow_charger -= 1
        else:
            if self.charger_down_dispatch_mode == 0:
                for username in self.charger_queue[charger_ID]:
                    self.user_status[username].status = -2
                    self.waiting_fast_car += 1
                    self.fast_pri_queue.append(username)
            else:
                new_queue: list[tuple[int, str]] = []
                for username in self.fast_queue:
                    new_queue.append(
                        (self.user_status[username].waiting_number, username))
                for k, v in self.charger_queue.items():
                    if k == charger_ID or self.charger_mode[k] != charging_mode:
                        continue
                    while len(v) > 1:
                        username = v.pop()
                        self.user_status[username].status = -1
                        self.waiting_fast_car += 1
                        self.charger_vol[k] -= self.user_status[username].request_vol
                        new_queue.append(
                            (self.user_status[username].waiting_number, username))
                new_queue.sort()
                self.fast_queue = [i[1] for i in new_queue]
            if not self.__chargerQueueFull(charger_ID):
                self.avai_fast_charger -= 1
        del self.charger_queue[charger_ID]
        self.__batchDispatch(charging_mode)

    def carsAhead(self, username: str) -> int:
        """获取前序车辆数

        Args:
            username (str): 用户名

        Returns:
            int: 前序车辆数
        """
        status = self.user_status[username]
        if status.charging_mode == 'T':
            if status.status == -1:
                return len(self.slow_pri_queue) + self.slow_queue.index(username)
            elif status.status == -2:
                return self.slow_pri_queue.index(username)
            else:
                return 0
        else:
            if status.status == -1:
                return len(self.fast_pri_queue) + self.fast_queue.index(username)
            elif status.status == -2:
                return self.fast_pri_queue.index(username)
            else:
                return 0

    def __getQueueFront(self, mode: str) -> int:
        if mode == 'T':
            if len(self.slow_pri_queue) != 0:
                ret = self.slow_pri_queue[0]
                self.slow_pri_queue.remove(ret)
                return ret
            else:
                ret = self.slow_queue[0]
                self.slow_queue.remove(ret)
                return ret
        else:
            if len(self.fast_pri_queue) != 0:
                ret = self.fast_pri_queue[0]
                self.fast_pri_queue.remove(ret)
                return ret
            else:
                ret = self.fast_queue[0]
                self.fast_queue.remove(ret)
                return ret

    def __getCharger(self, charging_mode: str) -> int:
        min_vol = inf
        for k, v in self.charger_vol.items():
            if self.charger_mode[k] != charging_mode or self.__chargerQueueFull(k):
                continue
            if v < min_vol:
                min_vol = v
                charger_ID = k
        return charger_ID

    def __addToCharger(self, username: str, charging_mode: str, charger_ID: int) -> None:
        self.user_status[username].status = charger_ID
        self.charger_queue[charger_ID].append(username)
        self.charger_vol[charger_ID] += self.user_status[username].request_vol
        if charging_mode == 'T':
            self.waiting_slow_car -= 1
            if self.__chargerQueueFull(charger_ID):
                self.avai_slow_charger -= 1
        else:
            self.waiting_fast_car -= 1
            if self.__chargerQueueFull(charger_ID):
                self.avai_fast_charger -= 1

    def __chargerQueueFull(self, charger_ID: int) -> bool:
        return len(self.charger_queue[charger_ID]) == self.db.getParkingSpace()

    def __batchDispatch(self, charging_mode: str) -> None:
        if charging_mode == 'T':
            charging_list = []
            for username in self.slow_queue:
                charging_list.append(
                    (self.user_status[username].request_vol, username))
            charging_list.sort()
            while self.waiting_slow_car != 0 and self.avai_slow_charger != 0:
                charger_ID = self.__getCharger(charging_mode)
                while not self.__chargerQueueFull(charger_ID) and len(self.slow_pri_queue) != 0:
                    username = self.slow_pri_queue[0]
                    self.slow_pri_queue.remove(username)
                    self.__addToCharger(username, charging_mode, charger_ID)
                while not self.__chargerQueueFull(charger_ID):
                    username = charging_list[0]
                    charging_list.remove(username)
                    self.slow_queue.remove(username)
                    self.__addToCharger(username, charging_mode, charger_ID)
        else:
            charging_list = []
            for username in self.fast_queue:
                charging_list.append(
                    (self.user_status[username].request_vol, username))
            charging_list.sort()
            while self.waiting_fast_car != 0 and self.avai_fast_charger != 0:
                charger_ID = self.__getCharger(charging_mode)
                while not self.__chargerQueueFull(charger_ID) and len(self.fast_pri_queue) != 0:
                    username = self.fast_pri_queue[0]
                    self.fast_pri_queue.remove(username)
                    self.__addToCharger(username, charging_mode, charger_ID)
                while not self.__chargerQueueFull(charger_ID):
                    username = charging_list[0]
                    charging_list.remove(username)
                    self.fast_queue.remove(username)
                    self.__addToCharger(username, charging_mode, charger_ID)

    def __dispatch(self, charging_mode: str) -> None:
        # 判断调度策略，进行调度
        if charging_mode == 'T':
            while self.waiting_slow_car != 0 and self.avai_slow_charger != 0:
                charger_ID = self.__getCharger(charging_mode)
                username = self.__getQueueFront('T')
                self.__addToCharger(username, charging_mode, charger_ID)
        else:
            while self.waiting_fast_car != 0 and self.avai_fast_charger != 0:
                charger_ID = self.__getCharger(charging_mode)
                username = self.__getQueueFront('T')
                self.__addToCharger(username, charging_mode, charger_ID)

if __name__ == '__main__':
    dispatcher = Dispatcher(backDB.DB())
    dispatcher.db.init()
    dispatcher.db.setParkingSpace(2)
    dispatcher.db.setWaitingAreaCapacity(6)
    dispatcher.newCharger(1, 'T')
    dispatcher.addCar(1, '233', 'T', 3)
    dispatcher.addCar(2, '455', 'T', 3)
    print(dispatcher.carStatus('233'))
    print(dispatcher.carStatus('455'))
