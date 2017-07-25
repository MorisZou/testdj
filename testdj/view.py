
from django.contrib import auth
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
           return render_to_response('search.html',{'dberrormsg':result_desc})  
   else:
     open('/tmp/1.txt','w+').write(key)
     return render_to_response('result.html',{'key':base64.encodestring(key),'messages':messages,'page_counts':page_counts,'result_descs':result_desc,'result_conn':dbchoice1})
   #return HttpResponse(key)
   
def query_page(request):
   #sql=request.GET.get('sql')
   page_id=request.GET.get('page_id')
    
   sqltext=open('/tmp/1.txt','r').read()
   
   db_connect=Connect(host='172.30.16.136',sqltext1=sqltext)
   (result_desc,messages,page_counts)=db_connect.connectexec(page_id=int(page_id))
   return render_to_response('result.html',{'key':base64.encodestring(sqltext),'messages':messages,'page_counts':page_counts,'result_descs':result_desc})
  


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
