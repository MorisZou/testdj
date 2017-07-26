
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from connect import Connect
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
import time
import re
import csv
from  reportlab.pdfgen import canvas
import base64
import os
import sys


from testdj.models import user

import logging

sqlgtext=''

def search(request):
   if request.user.is_authenticated():     
     return render_to_response('search.html')
   else:
     return HttpResponse("no login")


def result(request):
 
   logger=logging.getLogger('testdj')
   
   key=request.POST.get('m1')
   dbchoice1=request.POST.get('dbchoice')
   p=re.compile(r'^select')
   if key=='':
       return render_to_response('search.html',{'error':'NULL'})
   if not (p.search(key)):
       return render_to_response('search.html',{'error':'notValidSelect'})

   if re.compile(r'for update').search(key):
       return render_to_response('search.html',{'error':'forUpdate'})

   logger.warning('SQL: '+key+' DB EXEUTION:'+dbchoice1+' USER: '+request.user.username+request.META['REMOTE_ADDR'])
   db_connect=Connect(host=dbchoice1,sqltext1=key)
   
   (result_desc,messages,page_counts)=db_connect.connectexec()
  
   p2=re.compile(r'ORA-')
   if  (p2.search(str(messages))):
           return render_to_response('search.html',{'dberrormsg':messages})  
   else:
      open('/tmp/1.txt','w+').write(key)
      if  re.compile(r'v\$').search(key) or re.compile(r'V\$').search(key) or re.compile(r'dba_\$').search(key) or re.compile(r'DBA_\$').search(key):
       cols=[]
       rows=[]
       for row in messages:
        for col in row:
         cols.append(str(col).decode('utf-8', 'ignore'))
        rows.append(cols)
       messages=rows 
       return render_to_response('result.html',{'dbchoice1':base64.encodestring(dbchoice1),'messages':messages,'page_counts':page_counts,'result_descs':result_desc})
      else:
        return render_to_response('result.html',{'dbchoice1':base64.encodestring(dbchoice1),'messages':messages,'page_counts':page_counts,'result_descs':result_desc}) 



@login_required(login_url='/loging/')   
def query_page(request):
   dbchoice1=base64.decodestring(request.GET.get('dbchoice1'))
   page_id=request.GET.get('page_id')
    
   sqltext=open('/tmp/1.txt','r').read()
   
   db_connect=Connect(host=dbchoice1,sqltext1=sqltext)
   (result_desc,messages,page_counts)=db_connect.connectexec(page_id=int(page_id))

   if  re.compile(r'v\$').search(sqltext) or re.compile(r'V\$').search(sqltext) or re.compile(r'dba_\$').search(sqltext) or re.compile(r'DBA_\$').search(sqltext):
       cols=[]
       rows=[]
       for row in messages:
        for col in row:
         cols.append(str(col).decode('utf-8', 'ignore'))
        rows.append(cols)
       messages=rows
       return render_to_response('result.html',{'dbchoice1':base64.encodestring(dbchoice1),'messages':messages,'page_counts':page_counts,'result_descs':result_desc})
   else: 
     return render_to_response('result.html',{'dbchoice1':base64.encodestring(dbchoice1),'messages':messages,'page_counts':page_counts,'result_descs':result_desc})
  

@login_required(login_url='/loging/')
def changepwd(request):
       return render_to_response('changepwd.html')

@login_required(login_url='/loging/')
def changepwdok(request):

      username=request.POST.get('username','')
      password=request.POST.get('oldpassword','')
      newpassword=request.POST.get('newpassword','')
      if len(newpassword)==0 or len(newpassword)<=8:
          return render_to_response('changepwd.html',{'pwdnullorshor':True})
      user = auth.authenticate(username=username, password=password)
      if user is not None and user.is_active:
        auth.login(request,user)
        user.set_password(newpassword)  
        user.save()  
        return render_to_response('login.html',{'changepwdok':True})
      else:
        return render_to_response('changepwd.html',{'changepwdokerror':True}) 

def loging(request):
    
    return render_to_response('login.html')

def logout(request):
    auth.logout(request)
    return render_to_response('login.html',{'logout':True})


def login_view(request):
       
      username=request.POST.get('username','')
      password=request.POST.get('password','')
      user = auth.authenticate(username=username, password=password)    
      if user is not None and user.is_active:
          auth.login(request,user)
          return HttpResponseRedirect("/search/")
      else:
          return render_to_response('login.html',{'error':True})

def help(request):
  
    return render_to_response('help.html')
