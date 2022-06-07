import json
from tabnanny import check
from urllib import response
from flask import Flask, make_response, request, session, url_for
from sqlalchemy import true
from backDB import DB

db = DB()
app = Flask(__name__)

@app.route("/")
def printAllTestURL():
    urlDict = {
        'usrLogon':request.url + url_for('usrLogon',name='Jackie',password='114514'),
        'usrLogin':request.url + url_for('usrLogin',name='Jackie',password='114514'),
        'usrResetPWD':request.url + url_for('usrResetPWD',name='Jackie',password='114514')
        }
    return urlDict

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

    checkResult = db.resetUserPwd(name, password)
    return json.dumps({'id':checkResult})

if __name__ == '__main__':
    app.run(port='5000')