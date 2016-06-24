#!/usr/bin/python
#-*- coding:utf-8 -*-

    
import json
import requests
import warnings
import sys
import time

def gettoken(corpid,corpsecret,tokenpath):
    Url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=%s&corpsecret=%s' % (corpid,corpsecret)
    UrlContext = requests.get(Url).text
    Content = eval(UrlContext)
    Token = Content['access_token']
    with open(tokenpath,'w') as f:
        f.write(Token)
    return Token
	
def sendmessage(Userid,Text,token):
    submiturl = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={0}'.format(token)
    data = {"touser":Userid,"msgtype":"text","agentid":"0","text":{"content":Text},"safe":"0"}
    data = json.dumps(data,ensure_ascii=False)
    submitdata = requests.post(submiturl,data)
    content=submitdata.text
    if eval(content)['errcode'] == 42001 or eval(content)['errcode'] == 40014:
        print eval(content)['errcode']
        token=gettoken(CorpID,Corpsecret,'/tmp/token.txt')     
        sendmessage(Userid,Text,token)

def readtoken(corpid,corpsecre,tokenpath):
    try:
        with open(tokenpath,'r') as f:
            token=f.read()
        return token
    except IOError:
        token=gettoken(corpid,corpsecre,tokenpath)
	return token

def date():
    date = time.strftime('%m-%d %H:%M:%S',time.localtime())
    return date

if __name__ == '__main__':
    CorpID = 'CorpID 可在企业号设置页面账号信息处查看'
    Corpsecret = 'corpsecret 可在 设置->功能设置->权限管理 中查看'

    warnings.filterwarnings('ignore')
    token=readtoken(CorpID,Corpsecret,'/tmp/token.txt')
    userid = sys.argv[1]
    text = sys.argv[2]+'\nCall Time:'+date()
    sendmessage(userid,text,token)
