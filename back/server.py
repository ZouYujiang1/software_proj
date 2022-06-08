from cgitb import text
from datetime import datetime
import json
from tabnanny import check
from unittest import result
from urllib import response
from xmlrpc.client import DateTime
from flask import Flask, make_response, request, session, url_for
from sqlalchemy import func, true
from backDB import DB, QueuingUser

db = DB()
db.init()
app = Flask(__name__)

@app.route("/")
def printAllTestURL():
    urlTestList = '{'
    urlTestList += '\nusrLogon: ' + request.url + url_for('usrLogon',name='Jackie',password='114514')
    urlTestList += '\nusrLogin: ' + request.url + url_for('usrLogin',name='Jackie',password='114514')
    urlTestList += '\nusrResetPWD: ' + request.url + url_for('usrResetPWD',name='Jackie',password='114514')
    urlTestList += '\nusrPersonal: ' + request.url + url_for('usrPersonal',name='Jackie',password='114514')
    urlTestList += '\nusrGetQueueNo: ' + request.url + url_for('usrGetQueueNo',name='Jackie',chargingMode='F')
    urlTestList += '\nadminUsrInfo: ' + request.url + url_for('adminUsrInfo')
    urlTestList += '\n}'
    print(urlTestList)
    return urlTestList

@app.route("/usr/logon")
def usrLogon():
    name = request.args['name']
    password = request.args['password']

    id = db.addUser(name,password)
    return json.dumps({'id':id})

@app.route("/usr/login")
def usrLogin():
    name = request.args['name']
    password = request.args['password']

    # checkResult成功时返回id，失败时返回0或-1
    checkResult = db.checkUserPwd(name, password)
    if checkResult > 0:
        return json.dumps({'status':'UsrId OnLine Now', 'id':checkResult})
    elif checkResult == 0:
        return json.dumps({'status':'Password Error', 'id':0})
    else:
        return json.dumps({'status':'UsrId Not Found','id':-1})

@app.route("/usr/resetpwd")
def usrResetPWD():
    name = request.args['name']
    password = request.args['password']

    # checkResult成功时返回id，失败时返回-1
    checkResult = db.resetUserPwd(name, password)
    return json.dumps({'id':checkResult})

@app.route("/usr/personal")
def usrPersonal():
    name = request.args['name']
    password = request.args['password']

    # checkResult成功时返回id，失败时返回-1
    checkResult = db.checkUserPwd(name, password)
    if checkResult > 0:
        return db.getUserInfo(name)
    else:
        return json.dumps({'id':-1,'status':'UsrId or UsrName Not Found'})

@app.route("/usr/getQueueNo")
def usrGetQueueNo():
    usrName = request.args['name']
    chargingMode = request.args['chargingMode']

    timeOfApplyingNo = datetime.now()
    carsAhead = 0;
    # print(db.getUserInfo(usrName))
    usrID = db.getUserInfo(usrName).get('id')
    queueNo = db.addQueuingUser(usrID, chargingMode, carsAhead, timeOfApplyingNo)
    return json.dumps({'queueNo' : queueNo})


@app.route("/admin/usr-info")
def adminUsrInfo():
    return str(db.getAllUserInfo())

if __name__ == '__main__':
    app.run(port='5000')
    print('HelloWorld')