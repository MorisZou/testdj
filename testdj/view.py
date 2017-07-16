
from connect import Connect
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
import time
import re


def search(request):
   return render_to_response('search.html')

def result(request):
   key=request.POST['m1']
   p=re.compile(r'select')
   if key=='':
       return render_to_response('search.html',{'error':True})
   if not (p.search(key)):
       return render_to_response('search.html',{'error1':True})
   result_conn1=Connect()
   result_cur=result_conn1.connectdb()
   result_cur01=result_cur.cursor()
   result_cur01.execute(key)
   resultall=result_cur01.fetchall()
   result_count=[]
   for row in resultall:
      result_count.append(row.values())
      columnname=row.keys()
   return render_to_response('result.html',{'columnname':columnname,'message':result_count})


def hello(request):
   conn1=Connect()
   cur=conn1.connectdb()
   cur01=cur.cursor()
   cur01.execute("update db1.t2 set a=a+1")
   cur01.execute("commit")
   cur01.execute("select a from db1.t2")
   return HttpResponse(cur01.fetchall())

def currenttime(request,offset):
   try:
    offset=int(offset)
   except ValueError:
    raise Http404()
   
 
   return HttpResponse(time.strftime("%b %d %Y %H:%M:%S"))












