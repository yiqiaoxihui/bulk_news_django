# -*- coding: UTF-8 -*-
from django.http import HttpResponse
from django.shortcuts import render
import json
import time
import sys
import requests
import os
from bs4 import BeautifulSoup
from django.http import FileResponse
def index(request):
	context          = {}
	context['hello'] = 'Hello World!'
	return render(request, 'index.html', context)
def swarm_npr(begin_news,count):
	headers = {}
	headers["User-Agent"] = "Mozilla/5.0 (Windows NT 5.2) AppleWebKit/534.30 (KHTML, like Gecko) Chrome/12.0.742.122 Safari/534.30"
	headers["Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
	headers["Accept-Language"] = "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3"
	headers["Accept-Encoding"] = "gzip, deflate"
	headers["Upgrade-Insecure-Requests"] = "1"
	current=0
	file_name='npr_from_'+str(begin_news)+"_count_"+str(count)+"_"+str(int(time.time()))+".txt"
	fw=open("download/"+file_name,'w')
	dic={}
	dic['status']=1
	while current<count:
		# print current
		try:
			url = 'https://www.npr.org/sections/health/archive?start='+str(begin_news+current)
			req = requests.get(url, headers=headers, timeout=60)
			req.encoding="utf-8"
			soup = BeautifulSoup(req.text, 'html.parser')
			list = []
			for h2 in soup.find_all(name='h2',attrs={"class":"title"}):
				a=h2.find_all('a')[0]
				s="start: "+str(begin_news+current)+" title: "+a.string.encode("utf-8")
				# print s
				fw.write(s+"\n")
				current+=1
		except Exception as e:
			print "error:",
			print(e)
			dic['status']=0
	fw.close()
	dic['file_name']=file_name
	return dic
def npr_download(request):
	data ={}
	data['status']=0
	if request.POST:
		data['npr_begin'] = request.POST['npr_begin']
		data['npr_count'] = request.POST['npr_count']
		baseDir = os.path.dirname(os.path.abspath(__name__))
		data['status']=1
		data['baseDir']=baseDir
		dic=swarm_npr(int(data['npr_begin']),int(data['npr_count']))
		file_name=dic['file_name']
		data['file_name']=file_name
		file=open("download/"+file_name,'rb')
		response = FileResponse(file)
		response['Content-Type'] = 'application/octet-stream'
		response['Content-Disposition'] = 'attachment;filename="'+file_name+'"'
		return response
		# return HttpResponse(json.dumps(data), content_type='application/json')
	else:
		return HttpResponse(json.dumps(data), content_type='application/json')

def swarm_interestingengineering_industry(begin_page,end_page):
	headers = {}
	headers["User-Agent"] = "Mozilla/5.0 (Windows NT 5.2) AppleWebKit/534.30 (KHTML, like Gecko) Chrome/12.0.742.122 Safari/534.30"
	headers["Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
	headers["Accept-Language"] = "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3"
	headers["Accept-Encoding"] = "gzip, deflate"
	headers["Upgrade-Insecure-Requests"] = "1"
	file_name='interestingengineering_industry_page_'+str(begin_page)+"_to_"+str(end_page)+"_"+str(int(time.time()))+".txt"
	fw=open("download/"+file_name,'w')
	count=0
	dic={}
	dic['status']=1
	for i in range(begin_page,end_page+1):
		try:
			url = 'https://interestingengineering.com/industry?page='+str(i)
			res = requests.get(url, headers=headers, timeout=60)
			# CVEList_html = getMiddleStr(res.text, 'New entries:', 'Graduations')
			soup = BeautifulSoup((res.text).encode('utf-8'), 'html.parser')
			list = []
			for h2 in soup.find_all(name='h2',attrs={"class":"clearfix"}):
				count+=1
				a=h2.find_all('a')[0]
				# print "page:",i,"title: ",a.string.encode("utf-8")	#
				fw.write("page:"+str(i)+" count: "+str(count)+" title: "+a.string.encode("utf-8")+"\n")
				#print(a['href'])
				#print(a.string)
		except Exception as e:
			print "error:",
			print(e)
			dic['status']=0
	dic['file_name']=file_name
	return dic
def interestingengineering_industry_download(request):
	data ={}
	data['status']=0
	if request.POST:
		data['interestingengineering_industry_begin'] = request.POST['interestingengineering_industry_begin']
		data['interestingengineering_industry_end'] = request.POST['interestingengineering_industry_end']
		baseDir = os.path.dirname(os.path.abspath(__name__))
		data['baseDir']=baseDir
		dic=swarm_interestingengineering_industry(int(data['interestingengineering_industry_begin']),int(data['interestingengineering_industry_end']))
		if dic['status']==1:
			data['status']=1
			file_name=dic['file_name']
			data['file_name']=file_name
			file=open("download/"+file_name,'rb')
			response = FileResponse(file)
			response['Content-Type'] = 'application/octet-stream'
			response['Content-Disposition'] = 'attachment;filename="'+file_name+'"'
			return response
		# return HttpResponse(json.dumps(data), content_type='application/json')
	else:
		return HttpResponse(json.dumps(data), content_type='application/json')

def theatlantic(begin_page,end_page):
	headers = {}
	headers["User-Agent"] = "Mozilla/5.0 (Windows NT 5.2) AppleWebKit/534.30 (KHTML, like Gecko) Chrome/12.0.742.122 Safari/534.30"
	headers["Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
	headers["Accept-Language"] = "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3"
	headers["Accept-Encoding"] = "gzip, deflate"
	headers["Upgrade-Insecure-Requests"] = "1"
	file_name='theatlantic_page_'+str(begin_page)+"_to_"+str(end_page)+"_"+str(int(time.time()))+".txt"
	fw=open("download/"+file_name,'w')
	count=0
	dic={}
	dic['status']=1
	count=0
	for i in range(begin_page,end_page+1):
		# time.sleep(1)
		try:
			url = 'https://www.theatlantic.com/latest/?page='+str(i)
			req = requests.get(url, headers=headers, timeout=60)
			# req.encoding="utf-8"
			soup = BeautifulSoup((req.text).encode('utf-8'), 'html.parser')
			list = []
			for h2 in soup.find_all(name='h2',attrs={"class":"hed"}):
				# a=h2.find_all('a')[0]
				# for em in h2.find_all("em"):
				# 	em_str=str(em.string).encode('utf-8').strip()

				# 	title=title+" " +em_str
				count+=1
				s="page:"+str(i)+" count: "+str(count)+" title: "+h2.text.encode('utf-8').strip()
				# print s
				fw.write(s+"\n")
				#print(a['href'])
				#print(a.string)
		except Exception as e:
			print "error:",
			print(e)
			dic['status']=0
	dic['file_name']=file_name
	return dic
def theatlantic_download(request):
	data ={}
	data['status']=0
	if request.POST:
		data['theatlantic_begin'] = request.POST['theatlantic_begin']
		data['theatlantic_end'] = request.POST['theatlantic_end']
		baseDir = os.path.dirname(os.path.abspath(__name__))
		# data['baseDir']=baseDir
		dic=theatlantic(int(data['theatlantic_begin']),int(data['theatlantic_end']))
		if dic['status']==1:
			data['status']=1
			file_name=dic['file_name']
			data['file_name']=file_name
			file=open("download/"+file_name,'rb')
			response = FileResponse(file)
			response['Content-Type'] = 'application/octet-stream'
			response['Content-Disposition'] = 'attachment;filename="'+file_name+'"'
			return response
		# return HttpResponse(json.dumps(data), content_type='application/json')
	else:
		return HttpResponse(json.dumps(data), content_type='application/json')