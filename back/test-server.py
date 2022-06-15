from cgi import test
from datetime import datetime, timedelta
import requests
import string
import json as js

from sqlalchemy import JSON

def testUsrLogon(usrName = '小红'):
    url = 'http://127.0.0.1:5000/usr/logon'
    json = { "name" : usrName , "password":'114514'}
    res = requests.post(url=url, json=json)
    print(res.json())

def testUsrLogin(usrName = '小红'):
    url = 'http://127.0.0.1:5000/usr/login'
    json = { "name" : usrName , "password":'114514'}
    res = requests.post(url=url, json=json)
    print(res.json())

def testUsrUnsubscrib(usrName = '小红'):
    url = 'http://127.0.0.1:5000/usr/unsubscrib'
    json = { "name" : usrName , "password":'114514'}
    res = requests.post(url=url, json=json)
    print(res.json())

def testGetQueueNo(usrName = '小红'):
    url = 'http://127.0.0.1:5000/usr/getqueueno'
    json = { "name" : usrName , "chargingMode" : 'F', "requestVol" : '11.4514'}
    res = requests.post(url=url, json=json)
    print(res.json())

def testGetHistoryOrders(usrName = '小红'):
    url = 'http://127.0.0.1:5000/usr/history-orders'
    json = { "name" : usrName }
    res = requests.post(url=url, json=json)
    for each in res.json()['data']:
        print(each)

def testUsrInfo():
    url = 'http://127.0.0.1:5000/admin/usr-info'
    json = { "chargerID" : 1 }
    res = requests.post(url=url, json=json)
    for each in res.json()['data']:
        print(each)

def testQueuingUsrInfo():
    url = 'http://127.0.0.1:5000/admin/queue-info'
    json = { "chargerID" : 1 }
    res = requests.post(url=url, json=json)
    for each in res.json()['data']:
        print(each)

def testChargersStatus():
    url = 'http://127.0.0.1:5000/admin/charger/status'
    json = { "chargerID" : 1 }
    res = requests.post(url=url, json=json)
    print(res.json())

def testChargersService():
    url = 'http://127.0.0.1:5000/admin/charger/service'
    json = { "chargerID" : 1 }
    res = requests.post(url=url, json=json)
    for each in res.json()['data']:
        print(each)

def testChargersStatistic():
    url = 'http://127.0.0.1:5000/admin/charger/statistic'
    json = { "chargerID" : 1 }
    res = requests.post(url=url, json=json)
    for each in res.json()['data']:
        print(each)

def testChargerTurnOn():
    url = 'http://127.0.0.1:5000/admin/charger/open'
    json = { "chargerID" : 1 }
    res = requests.post(url=url, json=json)
    print(res.json())

def testChargerTurnOff():
    url = 'http://127.0.0.1:5000/admin/charger/close'
    json = { "chargerID" : 1 }
    res = requests.post(url=url, json=json)
    print(res.json())

def testChargeBreak():
    url = 'http://127.0.0.1:5000/admin/charger/break'
    json = { "chargerID" : 1 }
    res = requests.post(url=url, json=json)
    print(res.json())

def testChargeFix():
    url = 'http://127.0.0.1:5000/admin/charger/fix'
    json = { "chargerID" : 1 }
    res = requests.post(url=url, json=json)
    print(res.json())

# print((datetime(2021,3,21,3,56,56,3432) - datetime(2021,3,21,3,50,56,3432))/timedelta(minutes=1))



# for name in string.ascii_lowercase:
#     testUsrLogon(name)
#     testUsrLogin(name)
#     testGetQueueNo(name)
# testQueuingUsrInfo()
# testUsrInfo()
# for name in string.ascii_lowercase:
#     testUsrUnsubscrib(name)
# testQueuingUsrInfo()
# testUsrInfo()
testGetHistoryOrders('e')
# testChargersStatus()
testChargersService()
# testChargersStatistic()
# testChargerTurnOn()
# testChargerTurnOff()
# testChargeBreak()
# testChargeFix()
