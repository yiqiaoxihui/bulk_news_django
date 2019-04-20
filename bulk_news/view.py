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


def log(content,request):
	fp=open('visit.log','a')
	if request.META.has_key('HTTP_X_FORWARDED_FOR'):
	    ip =  request.META['HTTP_X_FORWARDED_FOR']
	else:
	    ip = request.META['REMOTE_ADDR']
	if content and len(content)<1024:
		fp.write(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())+"\nsource:"+ip+", "+content+"\n")
	fp.close()

def del_file(path):
    ls = os.listdir(path)
    for i in ls:
        c_path = os.path.join(path, i)
        if os.path.isdir(c_path):
            del_file(c_path)
        else:
            os.remove(c_path)

def index(request):
	#clear cache download file
	del_file("./download/")
	context          = {}
	context['hello'] = 'Hello World!'
	log("visit index.",request)
	return render(request, 'index.html', context)
def swarm_npr(begin_news,count):
	headers = {}
	headers["User-Agent"] = "Mozilla/5.0 (Windows NT 5.2) AppleWebKit/534.30 (KHTML, like Gecko) Chrome/12.0.742.122 Safari/534.30"
	headers["Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
	headers["Accept-Language"] = "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3"
	headers["Accept-Encoding"] = "gzip, deflate"
	headers["Upgrade-Insecure-Requests"] = "1"
	current=0
	if str(begin_news).isdigit() == False or str(count).isdigit() ==False:
		print "input error: illege input"
		dic['msg']="input error: illege input"
		dic['status']=0
		return dic
	begin_news=int(begin_news)
	count=int(count)
	file_name='npr_from_'+str(begin_news)+"_count_"+str(count)+"_"+str(int(time.time()))+".txt"
	fw=open("download/"+file_name,'w')
	dic={}
	dic['status']=1
	dic['msg']="download success"
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
			print "error:",e
			dic['msg']="request error: "+str(e)
			dic['status']=0
			break
	fw.close()
	dic['file_name']=file_name
	return dic
def npr_download(request):
	data ={}
	data['status']=0
	if request.POST:
		npr_begin = request.POST['npr_begin']
		npr_count = request.POST['npr_count']
		# baseDir = os.path.dirname(os.path.abspath(__name__))
		# data['baseDir']=baseDir
		dic=swarm_npr(npr_begin,npr_count)
		if dic['status'] ==0:
			data['msg']=dic['msg']
			log("visit npr fail:"+data['msg']+","+npr_begin+"~"+npr_count,request)
			return HttpResponse(json.dumps(data), content_type='application/json')
		log("visit npr success,"+npr_begin+"~"+npr_count,request)
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
	count=0
	dic={}
	if str(begin_page).isdigit() == False or str(end_page).isdigit() ==False:
		print "input error: illege input"
		dic['msg']="input error: illege input"
		dic['status']=0
		return dic
	dic['status']=1
	dic['msg']="download success"
	begin_page=int(begin_page)
	end_page=int(end_page)
	fw=open("download/"+file_name,'w')
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
			print "request error:",e
			dic['msg']="request error: "+str(e)
			dic['status']=0
	fw.close()
	dic['file_name']=file_name
	return dic
def interestingengineering_industry_download(request):
	data ={}
	data['status']=0
	if request.POST:
		page_begin = request.POST['interestingengineering_industry_begin']
		page_end = request.POST['interestingengineering_industry_end']
		dic=swarm_interestingengineering_industry(page_begin,page_end)
		if dic['status'] ==0:
			data['msg']=dic['msg']
			log("visit interestingengineering fail:"+data['msg']+","+page_begin+"~"+page_end,request)
			return HttpResponse(json.dumps(data), content_type='application/json')
		log("visit interestingengineering success,"+page_begin+"~"+page_end,request)
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
	count=0
	dic={}
	dic['status']=1
	dic['msg']="download success"
	if str(begin_page).isdigit() == False or str(end_page).isdigit() ==False:
		print "input error: illege input"
		dic['msg']="input error: illege input"
		dic['status']=0
		return dic
	begin_page=int(begin_page)
	end_page=int(end_page)
	fw=open("download/"+file_name,'w')
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
			print "error:",e
			dic['msg']="request error: "+str(e)
			dic['status']=0
	fw.close()
	dic['file_name']=file_name
	return dic
def theatlantic_download(request):
	data ={}
	data['status']=0
	if request.POST:
		page_begin = request.POST['theatlantic_begin']
		page_end = request.POST['theatlantic_end']
		# data['baseDir']=baseDir
		dic=theatlantic(page_begin,page_end)
		if dic['status'] ==0:
			data['msg']=dic['msg']
			log("visit theatlantic fail:"+data['msg']+","+page_begin+"~"+page_end,request)
			return HttpResponse(json.dumps(data), content_type='application/json')
		log("visit theatlantic success,"+page_begin+"~"+page_end,request)
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


#usnews

def download_usnews_national_news(offset,count,type_name):
	headers = {}
	headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36"
	headers["Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
	headers["Accept-Language"] = "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3"
	headers["Accept-Encoding"] = "gzip, deflate, br"
	headers["Upgrade-Insecure-Requests"] = "1"
	headers['dnt']="1"
	headers['host']="www.usnews.com"
	#网站检查cookie,防止非浏览器访问
	headers['cookie']='akacd_www=2177452799~rv=27~id=b90d566f2e7ef60c84d7afe2c32fda4d; ak_bmsc=1E2BFD5AEEE3C9149DCDF134A206ACAC686D342D7F0C00000C7DB85C1480245A~plCikRpGmRDKH1ozmsZeuUCYSnFi8wVCEhIDo4rYvLZpZY1w9PAYpizSLA8om27TRfm6iEGAxB72sIfopMiXBWLBkOhcLMMXa/Hp6gBLO0mx2OlfGyUVoKmNX/prl0fuS7A1haCk5ztR5+j3IHeJIO96B2gaAyp+YTDyziGbtjlmXXloYOqTtxuG9Iis4u4Ssn/KCvpXvvNw18qJN+abQn3FyDhqV31Pvc5Y+PQqB65+g=; usn_session_id=5559450840561891; usn_visitor_id=55594508406661476; s_cc=true; s_fid=53CCD88B114578CF-200090CE5C0032A9; _ga=GA1.2.172632290.1555594541; _gid=GA1.2.1541948908.1555594541; __gads=ID=da114bdcf42f75c7:T=1555594553:S=ALNI_MbL49gbkLN_pY4bKleHPrz0PfSDqA; s_sq=%5B%5BB%5D%5D; _parsely_session={%22sid%22:2%2C%22surl%22:%22https://www.usnews.com/news/healthiest-communities/articles/2019-04-18/trump-plan-to-fight-hiv-aids-meets-skepticism-in-atlanta%22%2C%22sref%22:%22https://www.usnews.com/news/national-news%22%2C%22sts%22:1555601489555%2C%22slts%22:1555598003078}; _parsely_visitor={%22id%22:%22d7a0efb0-5ebb-45c7-8e08-77aabc11db9d%22%2C%22session_count%22:2%2C%22last_session_ts%22:1555601489555}; JSESSIONID=F364AFAB60B3A841AA0F95A9733664BB; _gat_tealium_0=1; sailthru_pageviews=4; sailthru_content=c16a6b9b4b4bbe14ad0ef03c8e01ede4bcbf4479891123bf36c55e9aa65e803d; sailthru_visitor=1b034867-4a84-4899-b61a-9ba6ba414784; RT="sl=1&ss=1555597972950&tt=11224&obo=0&bcn=%2F%2F173e2514.akstat.io%2F&sh=1555601505894%3D1%3A0%3A11224%2C1555600335720%3D1%3A0%3A23720&dm=usnews.com&si=193a2b6f-edb4-4980-9398-13f91a1b5a17&ld=1555601505895"; utag_main=v_id:016a30a8852f005003d15b03d48003073002906b00ac2$_sn:3$_ss:0$_st:1555603306014$_prevpage:www.usnews.com%2Fnews%2Fnational-news%3Bexp-1555605106005$_pn:3%3Bexp-session$ses_id:1555600306881%3Bexp-session; bm_sv=21AED741DF7DF3D6BA61E9774F199B2A~/hhbceHPENisDdNFWytQ/0pRJrcwuxQieE7D7bxMI+4D3hAfwVSE2WagUYkVI622I65S2jlrarC8eC87jLLLe15KyWIw/+ozKHM2fJ5Q1r+HIUGK0iRefGkwhVGyu74A+owNM+WTIEvycXq9a+elhl0idDVFVEAokHO+IoaaiIU='
	# headers['cookie']='akacd_www=2177452799~rv=27~id=b90d566f2e7ef60c84d7afe2c32fda4d; ak_bmsc=1E2BFD5AEEE3C9149DCDF134A206ACAC686D342D7F0C00000C7DB85C1480245A~plCikRpGmRDKH1ozmsZeuUCYSnFi8wVCEhIDo4rYvLZpZY1w9PAYpizSLA8om27TRfm6iEGAxB72sIfopMiXBWLBkOhcLMMXa/Hp6gBLO0mx2OlfGyUVoKmNX/prl0fuS7A1haCk5ztR5+j3IHeJIO96B2gaAyp+YTDyziGbtjlmXXloYOqTtxuG9Iis4u4Ssn/KCvpXvvNw18qJN+abQn3FyDhqV31Pvc5Y+PQqB65+g=; usn_session_id=5559450840561891; usn_visitor_id=55594508406661476; s_cc=true; s_fid=53CCD88B114578CF-200090CE5C0032A9; _ga=GA1.2.172632290.1555594541; _gid=GA1.2.1541948908.1555594541; __gads=ID=da114bdcf42f75c7:T=1555594553:S=ALNI_MbL49gbkLN_pY4bKleHPrz0PfSDqA; s_sq=%5B%5BB%5D%5D; _parsely_session={%22sid%22:1%2C%22surl%22:%22https://www.usnews.com/news/healthiest-communities/articles/2019-04-18/trump-plan-to-fight-hiv-aids-meets-skepticism-in-atlanta%22%2C%22sref%22:%22https://www.usnews.com/news/national-news%22%2C%22sts%22:1555598003078%2C%22slts%22:0}; _parsely_visitor={%22id%22:%22d7a0efb0-5ebb-45c7-8e08-77aabc11db9d%22%2C%22session_count%22:1%2C%22last_session_ts%22:1555598003078}; utag_main=v_id:016a30a8852f005003d15b03d48003073002906b00ac2$_sn:2$_ss:0$_st:1555599998039$_prevpage:www.usnews.com%2Fnews%2Fnational-news%3Bexp-1555601798413$_pn:4%3Bexp-session$ses_id:1555597960952%3Bexp-session; sailthru_pageviews=8; sailthru_content=c16a6b9b4b4bbe14ad0ef03c8e01ede4bcbf4479891123bf36c55e9aa65e803d; sailthru_visitor=1b034867-4a84-4899-b61a-9ba6ba414784; RT="sl=3&ss=1555597956403&tt=71532&obo=1&bcn=%2F%2F173e2513.akstat.io%2F&sh=1555598211875%3D3%3A1%3A71532%2C1555598196063%3D2%3A1%3A55773%2C1555598012183%3D1%3A0%3A55773&dm=usnews.com&si=193a2b6f-edb4-4980-9398-13f91a1b5a17&ld=1555598211875"; JSESSIONID=369BC083F3B1E9B851A50B26953A8026; bm_sv=21AED741DF7DF3D6BA61E9774F199B2A~/hhbceHPENisDdNFWytQ/0pRJrcwuxQieE7D7bxMI+4D3hAfwVSE2WagUYkVI622I65S2jlrarC8eC87jLLLe15KyWIw/+ozKHM2fJ5Q1r+FpFQumH4Twrjebwmof8e6k5SNSXyZOoNvBLuAf2VqlzMQHLtpZAKCbXVZThCKt+Q='
	dic={}
	dic['status']=1
	dic['msg']="download success"
	if str(offset).isdigit() == False or str(count).isdigit() ==False:
		print "input error: illege input"
		dic['msg']="input error: illege input"
		dic['status']=0
		return dic
	offset=int(offset)
	count=int(count)
	if offset==1:
		offset=0
	current=0
	file_name='usnews_'+type_name+'_offset_'+str(offset)+"_count_"+str(count)+"_"+str(int(time.time()))+".txt"
	fw=open("download/"+file_name,'w')
	while current<count:
		# print current
		try:
			url = 'https://www.usnews.com/news/'+type_name+'?offset='+str(offset+current)+'&renderer=json'
			# print url
			req = requests.get(url, headers=headers, timeout=60)
			req.encoding="utf-8"
			# print req.text
			try:
				json_text=json.loads(req.text)
				if json_text.get('stories'):
					for item in json_text['stories']:
						try:
							s="start: "+str(offset+current)+" title: "+item['short_headline'].encode("utf-8")+" ,"+item['pubdate'].encode("utf-8")
							print s
							fw.write(s+"\n")
							current+=1
						except Exception as e:
							print "line error:" ,e
			except Exception as e:
				print "loads error:", e
				dic['msg']="loads error: "+str(e)
				dic['status']=0
				break
		except Exception as e:
			print "request error:", e
			dic['msg']="request error: "+str(e)
			dic['status']=0
			break
	fw.close()
	dic['file_name']=file_name
	return dic
def usnews_national_news_download(request):
	data ={}
	data['status']=0
	if request.POST:
		# baseDir = os.path.dirname(os.path.abspath(__name__))
		# print(request.POST['usnews_select'][0])
		data['usnews_select']=request.POST['usnews_select']
		# return HttpResponse(json.dumps(data), content_type='application/json')
		usnew_begin=request.POST['usnews_national_news_begin']
		usnew_count=request.POST['usnews_national_news_count']
		dic=download_usnews_national_news(usnew_begin,usnew_count,request.POST['usnews_select'])
		if dic['status'] ==0:
			data['msg']=dic['msg']
			log("visit usnews fail:"+data['msg']+","+usnew_begin+"~"+usnew_count,request)
			return HttpResponse(json.dumps(data), content_type='application/json')
		log("visit usnews success,"+usnew_begin+"~"+usnew_count,request)
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
#wsj 
def wsj_opinion(begin_page,end_page,type_name):
	headers = {}
	headers["user-agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36"
	headers["accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3"
	headers["accept-language"] = "zh-CN,zh;q=0.9"
	headers["accept-encoding"] = "gzip, deflate, br"
	headers["upgrade-insecure-requests"] = "1"
	headers['dnt']="1"
	headers['cookie']='MicrosoftApplicationsTelemetryDeviceId=f368b9cc-f957-c4b6-8eed-f4cf78b9be47; MicrosoftApplicationsTelemetryFirstLaunchTime=1555646377649; _scid=c56e45c5-8aa8-4dea-a5e8-967ccb9b7e50; wsjregion=na%2Cus; usr_bkt=2qgQ1WCa3A; ab_uuid=aea8240b-0366-4126-954b-b682b3e3518e; test_key=0.7220783668882076; optimizelyEndUserId=oeu1555646101426r0.1287645573626417; AMCVS_CB68E4BA55144CAA0A4C98A5%40AdobeOrg=1; s_cc=true; __gads=ID=8b5722181bfee765:T=1555646107:S=ALNI_MbMFEM4gdOTaEUOp9v2CgxLrFeRkA; _ncg_sp_ses.5378=*; _ncg_id_=760f8154-5e60-4ba4-b583-fbb8dc19c673; NaN_hash=af3f02e7HKEKCGNE1555646111871; _mibhv=anon-1555646113976-3777492670_4171; _fbp=fb.1.1555646118325.1982338707; _parsely_session={%22sid%22:1%2C%22surl%22:%22https://www.wsj.com/news/opinion%22%2C%22sref%22:%22%22%2C%22sts%22:1555646119786%2C%22slts%22:0}; _parsely_visitor={%22id%22:%220285a2cc-91ea-4a41-a628-344c1065181c%22%2C%22session_count%22:1%2C%22last_session_ts%22:1555646119786}; cX_P=jqk9lj5bxylsgx94; cX_S=junjjf1oqs102wdu; _sctr=1|1555603200000; cX_G=cx%3A4gp59eg9a2vx3uo93ast7s9j5%3Afocaobt6urb2; usr_prof_v2=eyJpYyI6Mn0%3D; hok_seg=8m5oogcu3a7n; __qca=P0-603558645-1555646218054; vidoraUserId=eb0rcr800c4gdhd4tib17ksb9lqp6g; AMCV_CB68E4BA55144CAA0A4C98A5%40AdobeOrg=-1891778711%7CMCIDTS%7C18006%7CMCMID%7C91866129217042738901410584778414687528%7CMCAAMLH-1556253665%7C9%7CMCAAMB-1556261647%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1555664047s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C2.4.0; s_vnum=1558251406684%26vn%3D1; s_invisit=true; gpv_pn=WSJ_infogrfx_interactive_virtual-reality_How%20to%20Watch%20WSJ%20Virtual%20Reality%20%7C%20360%26deg%3B%20Video; s_sq=%5B%5BB%5D%5D; utag_main=v_id:016a33bbb1fc0017d7f6be0b6e7e03073002006b00ac2$_sn:1$_ss:0$_st:1555662280023$ses_id:1555646099966%3Bexp-session$_pn:48%3Bexp-session$_prevpage:WSJ_Summaries_Opinion%3Bexp-1555664080033$vapi_domain:wsj.com; _ncg_sp_id.5378=760f8154-5e60-4ba4-b583-fbb8dc19c673.1555646111.1.1555660532.1555646111.7c5f234d-2c83-48ed-90a0-70e96bb4d7da; GED_PLAYLIST_ACTIVITY=W3sidSI6IlVlV28iLCJ0c2wiOjE1NTU2NjA5OTEsIm52IjowLCJ1cHQiOjE1NTU2NjA0NzQsImx0IjoxNTU1NjYwNTYwfV0'
	type_name_dic={}
	type_name_dic['review-outlook-u-s']='Review%20%26%20Outlook%20U.S.'
	type_name_dic['commentary-u-s']='Commentary%20U.S.'
	type_name_dic['Letters-to-the-Editor']='Letters'
	type_name_dic['Bookshelf']='Bookshelf'
	type_name_dic['film-review']='Film%20Review'
	type_name_dic['television-review']='Television%20Review'
	type_name_dic['theater-review']='Theater%20Review'
	type_name_dic['art-review']='Art%20Review'
	type_name_dic['masterpiece']='Masterpiece'
	type_name_dic['music-review']='Music%20Review'
	type_name_dic['dance-review']='Dance%20Review'
	type_name_dic['opera-review']='Opera%20Review'
	type_name_dic['exhibition-review']='Exhibition%20Review'
	type_name_dic['cultural-commentary']='Cultural%20Commentary'
	file_name='wsj_opinion_'+type_name+'_page_'+str(begin_page)+"_to_"+str(end_page)+"_"+str(int(time.time()))+".txt"
	count=0
	dic={}
	dic['status']=1
	dic['msg']="download success"
	if type_name_dic.get(type_name) ==False:
		print("input error: illege input type_name")
		dic['msg']="input error: illege input type_name"
		dic['status']=0
		return dic
	if str(begin_page).isdigit() == False or str(end_page).isdigit() ==False:
		print("input error: illege input")
		dic['msg']="input error: illege input"
		dic['status']=0
		return dic
	begin_page=int(begin_page)
	end_page=int(end_page)
	fw=open("download/"+file_name,'w')
	# fw=open("q_format.html",'r')
	for i in range(begin_page,end_page+1):
		try:
			url = 'https://www.wsj.com/search/term.html?isAdvanced=true&articleType='+type_name_dic[type_name]+'&daysback=4y&min-date=2015/04/19&max-date=2019/04/19&source=wsjarticle,wsjblogs,sitesearch&page='+str(i)
			req = requests.get(url, headers=headers, timeout=60)
			soup = BeautifulSoup(req.text.encode('utf-8'), 'lxml')	#html5lib:最好的容错性;以浏览器的方式解析文档;生成HTML5格式的文档
			# print soup
			list = []
			# print req.text.encode('utf-8')
			soup=soup.find('body')
			# print soup
			try:
				for item in soup.find_all(name='div',attrs={"class":"headline-container"}):
					# print("*************************")
					# print item.string.encode('utf-8')
					h3=item.find('h3',attrs={"class":"headline"})
					time_lable=item.find('time',attrs={"class":"date-stamp-container"})
					# date=time_lable.find(attrs={"class":"time-container"})
					# print h3.string.encode('utf-8')
					a=h3.find('a')
					count+=1
					s="page:"+str(i)+" count: "+str(count)+" title: "+a.text.encode('utf-8').strip()+", "+time_lable.text.encode('utf-8').strip()
					print s
					fw.write(s+"\n")
					#print(a['href'])
					#print(a.string)
			except Exception as e:
				print "find error:",e

		except Exception as e:
			print "request error:",e
			dic['msg']="request error: "+str(e)
			dic['status']=0
	dic['file_name']=file_name
	return dic

def wsj_opinion_download(request):
	data ={}
	data['status']=0
	page_begin=request.POST['wsj_opinion_begin']
	page_end=request.POST['wsj_opinion_end']
	if request.POST:
		dic=wsj_opinion(page_begin,page_end,request.POST['wsj_select'])
		if dic['status'] ==0:
			data['msg']=dic['msg']
			log("visit wsj_opinion "+request.POST['wsj_select']+" fail:"+data['msg']+","+page_begin+"~"+page_end,request)
			return HttpResponse(json.dumps(data), content_type='application/json')
		log("visit wsj_opinion "+request.POST['wsj_select']+" success,"+page_begin+"~"+page_end,request)
		data['status']=1
		file_name=dic['file_name']
		data['file_name']=file_name
		file=open("download/"+file_name,'rb')
		response = FileResponse(file)
		response['Content-Type'] = 'application/octet-stream'
		response['Content-Disposition'] = 'attachment;filename="'+file_name+'"'
		return response
	else:
		return HttpResponse(json.dumps(data), content_type='application/json')


#washingtonpost
def swarm_washingtonpost(page_begin,page_end,type_name):
	headers = {}
	headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36"
	headers["Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
	headers["Accept-Language"] = "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3"
	headers["Accept-Encoding"] = "gzip, deflate, br"
	headers["Upgrade-Insecure-Requests"] = "1"
	headers['dnt']="1"
	#网站检查cookie,防止非浏览器访问
	# headers['cookie']='akacd_www=2177452799~rv=27~id=b90d566f2e7ef60c84d7afe2c32fda4d; ak_bmsc=1E2BFD5AEEE3C9149DCDF134A206ACAC686D342D7F0C00000C7DB85C1480245A~plCikRpGmRDKH1ozmsZeuUCYSnFi8wVCEhIDo4rYvLZpZY1w9PAYpizSLA8om27TRfm6iEGAxB72sIfopMiXBWLBkOhcLMMXa/Hp6gBLO0mx2OlfGyUVoKmNX/prl0fuS7A1haCk5ztR5+j3IHeJIO96B2gaAyp+YTDyziGbtjlmXXloYOqTtxuG9Iis4u4Ssn/KCvpXvvNw18qJN+abQn3FyDhqV31Pvc5Y+PQqB65+g=; usn_session_id=5559450840561891; usn_visitor_id=55594508406661476; s_cc=true; s_fid=53CCD88B114578CF-200090CE5C0032A9; _ga=GA1.2.172632290.1555594541; _gid=GA1.2.1541948908.1555594541; __gads=ID=da114bdcf42f75c7:T=1555594553:S=ALNI_MbL49gbkLN_pY4bKleHPrz0PfSDqA; s_sq=%5B%5BB%5D%5D; _parsely_session={%22sid%22:2%2C%22surl%22:%22https://www.usnews.com/news/healthiest-communities/articles/2019-04-18/trump-plan-to-fight-hiv-aids-meets-skepticism-in-atlanta%22%2C%22sref%22:%22https://www.usnews.com/news/national-news%22%2C%22sts%22:1555601489555%2C%22slts%22:1555598003078}; _parsely_visitor={%22id%22:%22d7a0efb0-5ebb-45c7-8e08-77aabc11db9d%22%2C%22session_count%22:2%2C%22last_session_ts%22:1555601489555}; JSESSIONID=F364AFAB60B3A841AA0F95A9733664BB; _gat_tealium_0=1; sailthru_pageviews=4; sailthru_content=c16a6b9b4b4bbe14ad0ef03c8e01ede4bcbf4479891123bf36c55e9aa65e803d; sailthru_visitor=1b034867-4a84-4899-b61a-9ba6ba414784; RT="sl=1&ss=1555597972950&tt=11224&obo=0&bcn=%2F%2F173e2514.akstat.io%2F&sh=1555601505894%3D1%3A0%3A11224%2C1555600335720%3D1%3A0%3A23720&dm=usnews.com&si=193a2b6f-edb4-4980-9398-13f91a1b5a17&ld=1555601505895"; utag_main=v_id:016a30a8852f005003d15b03d48003073002906b00ac2$_sn:3$_ss:0$_st:1555603306014$_prevpage:www.usnews.com%2Fnews%2Fnational-news%3Bexp-1555605106005$_pn:3%3Bexp-session$ses_id:1555600306881%3Bexp-session; bm_sv=21AED741DF7DF3D6BA61E9774F199B2A~/hhbceHPENisDdNFWytQ/0pRJrcwuxQieE7D7bxMI+4D3hAfwVSE2WagUYkVI622I65S2jlrarC8eC87jLLLe15KyWIw/+ozKHM2fJ5Q1r+HIUGK0iRefGkwhVGyu74A+owNM+WTIEvycXq9a+elhl0idDVFVEAokHO+IoaaiIU='
	# headers['cookie']='akacd_www=2177452799~rv=27~id=b90d566f2e7ef60c84d7afe2c32fda4d; ak_bmsc=1E2BFD5AEEE3C9149DCDF134A206ACAC686D342D7F0C00000C7DB85C1480245A~plCikRpGmRDKH1ozmsZeuUCYSnFi8wVCEhIDo4rYvLZpZY1w9PAYpizSLA8om27TRfm6iEGAxB72sIfopMiXBWLBkOhcLMMXa/Hp6gBLO0mx2OlfGyUVoKmNX/prl0fuS7A1haCk5ztR5+j3IHeJIO96B2gaAyp+YTDyziGbtjlmXXloYOqTtxuG9Iis4u4Ssn/KCvpXvvNw18qJN+abQn3FyDhqV31Pvc5Y+PQqB65+g=; usn_session_id=5559450840561891; usn_visitor_id=55594508406661476; s_cc=true; s_fid=53CCD88B114578CF-200090CE5C0032A9; _ga=GA1.2.172632290.1555594541; _gid=GA1.2.1541948908.1555594541; __gads=ID=da114bdcf42f75c7:T=1555594553:S=ALNI_MbL49gbkLN_pY4bKleHPrz0PfSDqA; s_sq=%5B%5BB%5D%5D; _parsely_session={%22sid%22:1%2C%22surl%22:%22https://www.usnews.com/news/healthiest-communities/articles/2019-04-18/trump-plan-to-fight-hiv-aids-meets-skepticism-in-atlanta%22%2C%22sref%22:%22https://www.usnews.com/news/national-news%22%2C%22sts%22:1555598003078%2C%22slts%22:0}; _parsely_visitor={%22id%22:%22d7a0efb0-5ebb-45c7-8e08-77aabc11db9d%22%2C%22session_count%22:1%2C%22last_session_ts%22:1555598003078}; utag_main=v_id:016a30a8852f005003d15b03d48003073002906b00ac2$_sn:2$_ss:0$_st:1555599998039$_prevpage:www.usnews.com%2Fnews%2Fnational-news%3Bexp-1555601798413$_pn:4%3Bexp-session$ses_id:1555597960952%3Bexp-session; sailthru_pageviews=8; sailthru_content=c16a6b9b4b4bbe14ad0ef03c8e01ede4bcbf4479891123bf36c55e9aa65e803d; sailthru_visitor=1b034867-4a84-4899-b61a-9ba6ba414784; RT="sl=3&ss=1555597956403&tt=71532&obo=1&bcn=%2F%2F173e2513.akstat.io%2F&sh=1555598211875%3D3%3A1%3A71532%2C1555598196063%3D2%3A1%3A55773%2C1555598012183%3D1%3A0%3A55773&dm=usnews.com&si=193a2b6f-edb4-4980-9398-13f91a1b5a17&ld=1555598211875"; JSESSIONID=369BC083F3B1E9B851A50B26953A8026; bm_sv=21AED741DF7DF3D6BA61E9774F199B2A~/hhbceHPENisDdNFWytQ/0pRJrcwuxQieE7D7bxMI+4D3hAfwVSE2WagUYkVI622I65S2jlrarC8eC87jLLLe15KyWIw/+ozKHM2fJ5Q1r+FpFQumH4Twrjebwmof8e6k5SNSXyZOoNvBLuAf2VqlzMQHLtpZAKCbXVZThCKt+Q='
	type_name_dic={}
	type_name_dic['outlook']='outlook'
	type_name_dic['the-posts-view']='opinions/the-posts-view'
	type_name_dic['letters-to-the-editor']='opinions/letters-to-the-editor'
	dic={}
	dic['status']=1
	if str(page_begin).isdigit() == False or str(page_end).isdigit() ==False:
		print "input error: illege input"
		dic['status']=1
		return dic
	page_begin=int(page_begin)
	page_end=int(page_end)
	if page_begin<=0:
		page_begin=1
	if page_end<=0:
		page_end=1
	file_name='washingtonpost_opinion_page_from_'+str(page_begin)+"_to_"+str(page_end)+"_"+str(int(time.time()))+".txt"
	fw=open("download/"+file_name,'w')
	limit=60
	count=0
	for i in range(page_begin,page_end+1):
		offset=(page_begin-1)*limit
		try:
			if type_name=="local-opinions":
				url='https://www.washingtonpost.com/pb/api/v2/render/feature?id=fL05x91im8Wwar&contentConfig=%7B%22path%22%3A%22%2Fopinions%2F%3Fquery%3D%2FWashingtonPost%2FProduction%2FDigital%2FQueries%2Fsite-service%2Fopinions%2Fcth-localops%26limit%3D'+str(limit)+'%26offset%3D'+str(offset)+'%22%7D&uri=/pb/opinions/local-opinions/&service=com.washingtonpost.webapps.pagebuilder.services.StoryAdapterService'
			elif type_name =='global-opinions':
				url='https://www.washingtonpost.com/pb/api/v2/render/feature?id=f0Aac2b2PCZvhr&contentConfig=%7B%22path%22%3A%22%2Fopinions%2F%3Fquery%3D%2FWashingtonPost%2FProduction%2FDigital%2FPages-Web%2Fopinions%2F_module-content%2Fglobal-opinions%26limit%3D'+str(limit)+'%26offset%3D'+str(offset)+'%22%7D&uri=/pb/global-opinions/&service=com.washingtonpost.webapps.pagebuilder.services.StoryAdapterService'
			else:
				url='https://www.washingtonpost.com/pb/api/v2/render/feature?id=fRRAZV1tyeKUar&contentConfig=%7B%22path%22%3A%22%2F'+type_name_dic[type_name]+'%2F%3Flimit%3D'+str(limit)+'%26offset%3D'+str(offset)+'%22%7D&uri=/pb/'+type_name_dic[type_name]+'/&service=com.washingtonpost.webapps.pagebuilder.services.StoryAdapterService'
			# print url
			req = requests.get(url, headers=headers, timeout=60)
			req.encoding="utf-8"
			# print req.text
			try:
				json_text=json.loads(req.text)
				if json_text.get('rendering'):
					soup = BeautifulSoup(json_text['rendering'].encode('utf-8'), 'lxml')
					try:
						for a in soup.find_all(name='a',attrs={"data-pb-local-content-field":"web_headline"}):
							count+=1
							s="page:"+str(i)+" count: "+str(count)+" title: "+a.text.encode('utf-8').strip()
							print s
							fw.write(s+"\n")
					except Exception as e:
						print "find error:",e
						dic['msg']="line error: "+str(e)
						dic['status']=0

			except Exception as e:
				print "loads error:", e
				print req.text
				break
		except Exception as e:
			print "request error:", e
			dic['status']=0
			break
	fw.close()
	dic['file_name']=file_name
	return dic
def washingtonpost_download(request):
	data ={}
	data['status']=0
	page_begin=request.POST['washingtonpost_begin']
	page_end=request.POST['washingtonpost_end']
	if request.POST:
		dic=swarm_washingtonpost(page_begin,page_end,request.POST['washingtonpost_select'])
		if dic['status'] ==0:
			data['msg']=dic['msg']
			log("visit washingtonpost "+request.POST['washingtonpost_select']+" fail:"+data['msg']+","+page_begin+"~"+page_end,request)
			return HttpResponse(json.dumps(data), content_type='application/json')
		log("visit washingtonpost "+request.POST['washingtonpost_select']+" success,"+page_begin+"~"+page_end,request)
		data['status']=1
		file_name=dic['file_name']
		data['file_name']=file_name
		file=open("download/"+file_name,'rb')
		response = FileResponse(file)
		response['Content-Type'] = 'application/octet-stream'
		response['Content-Disposition'] = 'attachment;filename="'+file_name+'"'
		return response
	else:
		return HttpResponse(json.dumps(data), content_type='application/json')