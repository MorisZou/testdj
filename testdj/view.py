
from django.contrib import auth
from connect import Connect
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
import time
import re
import csv
from  reportlab.pdfgen import canvas

from testdj.models import user

import logging

def search(request):
   if request.user.is_authenticated():     
     return render_to_response('search.html')
   else:
     return HttpResponse("no login")


def result(request):
 
   logger=logging.getLogger('testdj')
   key=request.POST.get('m1')
   dbchoice1=request.POST.get('dbchoice')
   p=re.compile(r'select')
   if key=='':
       return render_to_response('search.html',{'error':True})
   if not (p.search(key)):
       return render_to_response('search.html',{'error1':True})
   logger.warning('SQL: '+key+' DB EXEUTION:'+dbchoice1+' USER: '+request.user.username+request.META['REMOTE_ADDR'])
   db_connect=Connect(host=dbchoice1,sqltext1=key)   
   result_count=db_connect.connectexec()
   p2=re.compile(r'ORA-')
   if  (p2.search(str(result_count))):
           return render_to_response('search.html',{'dberrormsg':result_count})
   else: 
     return render_to_response('result.html',{'messages':result_count,'result_conn':dbchoice1})
 



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



