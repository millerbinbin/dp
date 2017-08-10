# -*- coding: UTF-8 -*-

import execjs
import win32com.server.util, win32com.client

class win32Doc:
     _public_methods_ = ['write']
     def write(self, s):
             print s

doc = win32Doc()
jsengine = win32com.client.Dispatch('MSScriptControl.ScriptControl')
jsengine.language = 'JavaScript'
jsengine.allowUI = False
jsengine.addObject('document', win32com.server.util.wrap(doc))
jsengine.eval('document.write("hello, world")')

# 执行本地的js

def get_js():
    # f = open("D:/WorkSpace/MyWorkSpace/jsdemo/js/des_rsa.js",'r',encoding='UTF-8')
    f = open("./rohr.min.js", 'r')
    line = f.readline()
    htmlstr = ''
    while line:
        htmlstr = htmlstr + line
        line = f.readline()
    return htmlstr


jsstr = get_js()
ctx = execjs.compile(jsstr)
print ctx
print(ctx.call('g', '123456'))