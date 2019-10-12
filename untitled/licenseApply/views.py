from django.shortcuts import HttpResponse
# from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.core import serializers
from django.http import JsonResponse
import requests,json,re
from .LicenseData import *
import os
import time
from django.http import FileResponse
from licenseApply import models

@require_http_methods(["POST"])
def login(request):
    response = {}
    url = "https://www.yunzhijia.com/space/c/rest/user/login"
    email = request.POST.get("email")
    password = request.POST.get("password")
    # password = "22"
    payload = "email="+email+"&password="+password+"&remember=false&forceToNetwork=false"
    headers = {
        'referer': "http://yunzhijia.com/home/?m=open&a=login",
        'Content-Type': "application/x-www-form-urlencoded",
        'Cache-Control': "no-cache",
        'Postman-Token': "14728954-0395-4ff0-abbd-d8926a985923"
    }
    resp = HttpResponse('success')
    try:
        response = requests.request("POST", url, data=payload, headers=headers)
        respInfo = json.loads(response.text)
        if respInfo['success'] == True:
            resp.set_cookie('at', response.cookies['at'])
            resp.set_cookie('cd', response.cookies['cd'])
            resp.set_cookie('cn', response.cookies['cn'])
            resp.set_cookie('cu', response.cookies['cu'])
            resp.set_cookie('__loginType', '')
            resp.set_cookie('uuid', response.cookies['uuid'])
            return resp
    except  Exception as e:
            return HttpResponse('failed')
    return HttpResponse('failed')


@require_http_methods(["GET"])
def testcookie(request):
    resp = HttpResponse('success')
    resp.set_cookie('cd', '11')
    resp.set_cookie('cn', '222')
    resp.set_cookie('cu', '33')
    resp.set_cookie('__loginType', '44')
    resp.set_cookie('uuid', '55')
    # request.session['uuid'] = '55'
    resp["Set-Cookie"] = "JSESSIONID=1dluwc7pzdnza1q6d22msvn6ph;Path=/sss"
    print(resp.cookies)
    return resp


@require_http_methods(["GET"])
def fetchMyInfo(request):
    cookie = {}
    if request.COOKIES:
        cookie = requests.cookies.RequestsCookieJar()
        cookie.set('at',request.COOKIES['at'])
        cookie.set('cd',request.COOKIES['cd'])
        cookie.set('cn',request.COOKIES['cn'])
        cookie.set('cu',request.COOKIES['cu'])
        cookie.set('__loginType','')
        cookie.set('uuid',request.COOKIES['uuid'])
        url = "https://www.yunzhijia.com/im/api/myinfo"
        headers = {
            "Cache-Control": "no-cache",
            "Postman-Token": "e9546ca5-c428-4de0-b62b-f7d3a823650b",
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36",
        }
        myinforesp = requests.request("GET", url, headers=headers, cookies=cookie)
        content = myinforesp.content.decode('utf-8').replace(' ','').replace('\n','')
        loginError = re.findall(re.compile(r'errorCode', re.S), content)
        if(len(loginError) == 0):
            myInfoDic = parseMyInfo(myinforesp)
            return JsonResponse({'myInfo': myInfoDic})
        myInfoDic = {
              'username':'',
              'department':'',
              'position':'',
              'photoUrl':'',
              'worknumber':'',
        }
        return JsonResponse({'myInfo':myInfoDic})

#解析个人信息响应报文
def parseMyInfo(myinforesp):
    content = myinforesp.content.decode('utf-8')
    myInfoDic = getDict(content)
    return myInfoDic

def findkey(data):
    p2 = re.compile(r'([a-z].*?)[:]')
    key = re.findall(p2, data)
    key.remove('http')
    key.remove('http')
    print(key)
    return key

# 第二步，获取key中元素对应的value
def matchvalue(key,data):
    p1 = re.compile(r'[\s]' + key + ': \'(.*?)[\',]', re.S)
    value = re.findall(p1, data)
    if len(value) == 0:
        return ''
    return value[0]

def getDict(data):
    key = findkey(data)
    d = dict()
    for k in key:
        value = matchvalue(k,data)
        d[k] = value
    return d


#申请license
@require_http_methods(["POST"])
def applyLicense(request):
    response = {}
    #获取username
    try:
        username = request.POST.get("email").replace('@.*','')
        username = re.sub(r'@.*','',username)
        url = "https://www.yunzhijia.com/space/c/rest/app/getlightappurl?appId=10284&originType=web&_=1569346655442"
        cookie = requests.cookies.RequestsCookieJar()
        cookie.set('at', request.COOKIES['at'])
        cookie.set('cd', request.COOKIES['cd'])
        cookie.set('cn', request.COOKIES['cn'])
        cookie.set('cu', request.COOKIES['cu'])
        cookie.set('__loginType', '')
        cookie.set('uuid', request.COOKIES['uuid'])
        headers = {
            'Cache-Control': "no-cache",
            'Postman-Token': "b57a8222-8123-4d76-adab-303ff5884208"
        }
        lightAppUrl = requests.request("GET", url, headers=headers, cookies=cookie)
        p1 = re.compile(r'ticket=[0-9a-zA-Z]*&', re.S)
        ticketStr = re.findall(p1, lightAppUrl.text)
        ticket = ticketStr[0].replace('ticket=','').replace('&','')

        #登录mykingdee门户拿到cookie中的jsessionid,uuid
        url = "https://login.mykingdee.com/login"
        headers = {
            'Cache-Control': "no-cache",
            'Postman-Token': "b57a8222-8123-4d76-adab-303ff5884208"
        }
        myKingdeeLoginResponse = requests.request("GET", url, headers=headers, cookies=cookie, timeout=1000)

        # 拿到CASTGC
        #1.请求登录
        url = "https://login.mykingdee.com/yzj/current-user!get.action?yzjTicket=" + ticket
        headers = {
            'Cache-Control': "no-cache",
            'Postman-Token': "b57a8222-8123-4d76-adab-303ff5884208"
        }
        requests.request("GET", url, headers=headers, cookies=cookie)
        url = "https://login.mykingdee.com/yzj/current-user!get.action?yzjTicket=https://login.mykingdee.com/login"
        headers = {
            'Cache-Control': "no-cache",
            'Postman-Token': "b57a8222-8123-4d76-adab-303ff5884208"
        }
        t = requests.request("GET", url, headers=headers, cookies=cookie)
        #2.拿到CASTGC
        url = "https://login.mykingdee.com/login?username="+username+"&ticket="+ticket+"&password=123456&lt=e1s1&_eventId=submit"
        cookie = {
            'JSESSIONID': myKingdeeLoginResponse.cookies['JSESSIONID'],
            'uid': myKingdeeLoginResponse.cookies['uid'],
        }
        headers = {
            'Cache-Control': "no-cache",
            'Postman-Token': "b57a8222-8123-4d76-adab-303ff5884208",
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36"
        }
        myKingdeeCASTGCResponse = requests.request("GET", url, headers=headers, cookies=cookie)

        #请求新增license
        url = 'http://icrm.kingdee.com:81/icrm/workflowCenter!add.action?workflowType=limLic'
        workflowCenterResp = requests.request("GET", url, headers=headers,allow_redirects=False)
        workflowCenterSession = workflowCenterResp.cookies['JSESSIONID']

        url = workflowCenterResp.headers['location']
        cookie = {
            'JSESSIONID': myKingdeeLoginResponse.cookies['JSESSIONID'],
            'uid': myKingdeeLoginResponse.cookies['uid'],
            'CASTGC': myKingdeeCASTGCResponse.cookies['CASTGC'],
            'username': username
        }
        ssoMyKingdeeResp = requests.request("GET", url, headers=headers,cookies=cookie,allow_redirects=False)

        url = ssoMyKingdeeResp.headers['location']
        loginMyKingdeeResp = requests.request("GET", url, headers=headers,cookies=cookie,allow_redirects=False)

        url = loginMyKingdeeResp.headers['location']
        cookie = {
            'JSESSIONID': workflowCenterSession
        }
        loginMyKingdeeResp = requests.request("GET", url, headers=headers,cookies=cookie,allow_redirects=False)

        url = loginMyKingdeeResp.headers['location']
        loginMyKingdeeResp = requests.request("GET", url, headers=headers,cookies=cookie,allow_redirects=False)

        url = 'http://icrm.kingdee.com:81' + loginMyKingdeeResp.headers['location']
        loginMyKingdeeResp = requests.request("GET", url, headers=headers, cookies=cookie, allow_redirects=False)

        url = 'http://icrm.kingdee.com:81' + loginMyKingdeeResp.headers['location']
        loginMyKingdeeResp = requests.request("GET", url, headers=headers, cookies=cookie, allow_redirects=False)

        url = 'http://icrm.kingdee.com:81/icrm/requestBill/limLic!add.action'
        licensePageResp = requests.request("GET", url, headers=headers,cookies=cookie,allow_redirects=False)


        #2打开页面解析响应报文获取提交个性化数据
        url = 'http://icrm.kingdee.com:81/icrm/requestBill/limLic!add.action;jsessionid=' + myKingdeeLoginResponse.cookies['JSESSIONID']
        cookie = {
            'JSESSIONID': myKingdeeLoginResponse.cookies['JSESSIONID']
        }
        licensePageResponse = requests.request("GET", url, headers=headers, cookies=cookie)
        #解析响应报文并获取提交POSTDATA
        featureCode = request.POST.get("serverSpecialCode")
        stationNumber = request.POST.get("stationNumber")
        productVersion = request.POST.get("version")
        content = licensePageResp._content.decode('utf-8')
        licensePageDefaultInfoDic = genLicensePostData(content,featureCode,productVersion,stationNumber)
        limLicNumber = licensePageDefaultInfoDic['limLic.number']
        #license申请提交
        url = 'http://icrm.kingdee.com:81/icrm/requestBill/limLic!submitBill.action?workflowId='
        cookie = {
            'JSESSIONID': workflowCenterSession
        }
        licensePostResponse = requests.request("POST", url, data=licensePageDefaultInfoDic, headers=headers, cookies=cookie, timeout=2000)
        content = licensePostResponse._content.decode('utf-8')
        status = checkIsApplySuccess(content)
        resp = JsonResponse(data={"status":status})
        resp.set_cookie('workflowCenterSession',workflowCenterSession)
        resp.set_cookie('limLicNumber',limLicNumber)
        return resp
    except  Exception as e:
            resp = JsonResponse(data={"status": "failed"})
            return resp


#生成License附件并且返回License附件名称
@require_http_methods(["GET"])
def genLicenseAttach(request):
    cookie = {}
    if request.COOKIES:
        cookie = requests.cookies.RequestsCookieJar()
        workflowCenterSession =  request.COOKIES['workflowCenterSession']
        limLicNumber =  request.COOKIES['limLicNumber']
        #获取workflow id
        url = 'http://icrm.kingdee.com:81/icrm/workflowCenter!listWorkflow.action?workflowType=limLic'
        cookie = {
            'JSESSIONID': workflowCenterSession
        }
        licenseViewId = ""
        while licenseViewId == "":
            listWorkflowResp = requests.request("GET", url, cookies=cookie,timeout=2000)
            listWorkflowRespContent = listWorkflowResp._content.decode('utf-8')
            licenseViewId = getLimicViewId(listWorkflowRespContent,limLicNumber)
        #获取license查看页面的upId
        url = 'http://icrm.kingdee.com:81/icrm/workflowCenter!viewWorkflow.action?id='+licenseViewId+'&type=limLic'
        licenseViewPageResp = requests.request("GET", url, cookies=cookie,timeout=2000,allow_redirects=False)
        url = 'http://icrm.kingdee.com:81'+licenseViewPageResp.headers['location']
        licenseViewPageResp = requests.request("GET", url, cookies=cookie,timeout=2000)
        content = licenseViewPageResp._content.decode('utf-8')
        upId = getUpId(content)
        #获取附件id
        url = 'http://icrm.kingdee.com:81/accessory!list.action'
        cookie = {
            'JSESSIONID': workflowCenterSession
        }
        postdata = {
            "objID": upId,
            "objType": "限时License申请"
        }
        licenseAttachResponse = requests.request("POST", url, data=postdata, cookies=cookie,timeout=2000)
        licenseListArray = json.loads(licenseAttachResponse._content)['list']
        while len(licenseListArray) == 0:
            licenseAttachResponse = requests.request("POST", url, data=postdata, cookies=cookie,timeout=2000)
            licenseListArray = json.loads(licenseAttachResponse._content)['list']
        licenseId = licenseListArray[0]['id']
        url = "http://icrm.kingdee.com:81/accessory!download.action;jsessionid=null?id=" + licenseId + ""
        licenseFileResp = requests.request("GET", url, cookies=cookie,timeout=2000,allow_redirects=False)
        filename = genLicenseFile(licenseFileResp._content)
        resp = JsonResponse(data={'status':'success'})
        resp.set_cookie('licenseFileName',filename)
        return resp

def genLicenseFile(content):
    licenseFileFolderPath = './licenseFolder'
    if not os.path.isdir(licenseFileFolderPath):
        os.makedirs(licenseFileFolderPath)
    localTime = time.strftime("%Y%m%d%H%M%S", time.localtime())
    filename = licenseFileFolderPath+"/license" + localTime + ".dat"
    # a:以追加模式打开（必要时可以创建）append;b:表示二进制
    f = open(filename, 'ab')
    f.write(content)
    f.close()
    return filename

#下载license
@require_http_methods(["GET"])
def getLicenseFile(request):
    filename = request.COOKIES['licenseFileName']
    file = open(filename, 'rb')
    response = FileResponse(file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="License.dat"'.format(filename)
    return response
