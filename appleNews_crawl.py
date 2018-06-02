# coding: utf-8

import requests
import lxml
from datetime import datetime, date, time
import re
from bs4 import BeautifulSoup
import MySQLdb
import json
import jieba.posseg as pseg
import jieba
def writeLog(level, message):
	global file_
	message = "Log %s %s %s" % (level, datetime.now(), message)
	file_.write("%s\n"%message)
def writeFile(kind_number):
    if kind_number==0:
        return 'keyword/Other.txt'
    elif kind_number ==1:
        return 'keyword/Society.txt'
    elif kind_number == 2:
        return 'keyword/Entertainment.txt'
    elif kind_number == 3:
        return 'keyword/Life.txt'
    elif kind_number == 4:
        return 'keyword/Sport.txt'
    elif kind_number==5:
        return 'keyword/International.txt'
    elif kind_number==6:
        return 'keyword/Politic.txt'
    elif kind_number ==7:
        return 'keyword/Finance.txt'
    elif kind_number == 8:
        return 'keyword/Technology.txt'
    else :
        return 'Test.txt'

def getNews(url):
    try:
        res = requests.get(url)
        soup = BeautifulSoup(res.text,"lxml")
		title = soup.title.string
		title = title.encode('utf-8')
		#print "Title: "+title
    
    	content = soup.find("div","ndArticle_margin").text.strip()
    	byte_string = '報導\)|報導\）'
    	unicode_string = byte_string.decode('utf-8')
    	result = re.findall(unicode_string,content)
    	if result!=[]:
        	content = content[:content.find(result[0])+len(result[0])]
    	date = soup.find("div","ndArticle_creat").text
		date = date[5:]
		date = date.replace("/","-")
		date +=":00"
        date = datetime.strptime(date,"%Y-%m-%d %H:%M:%S")
        #print date
        
        kind = json.loads(soup.find('script', type='application/ld+json').text)
        kind = kind['keywords'][0]
        #print kind
        kind_number = kind_dict.get(kind,0)
        #print kind_number

		f = writeFile(kind_number)
		jieba.load_userdict(f)
        words = pseg.cut(content)
        keyword_string=""
        for word in words:
            if word.flag == 'n'and keyword_string.find(word.word)==-1:
                keyword_string+=word.word+","            
        keyword_string=keyword_string[:-1]       
        #print keyword_string
        
        try:            
            db = MySQLdb.connect(host="localhost",user="", passwd="",db="", charset="utf8")
            cursor = db.cursor()
            sql = "INSERT INTO news(Link, Title, Content, Kinds, Post_time, Keywords)                VALUES (%s,%s,%s,%s,%s,%s)"
            cursor.execute(sql,(url, title, content , kind_number, date, keyword_string))
            db.commit()
            db.close()
        except MySQLdb.Error as err:
			if 1062 in err:
                writeLog('E',"[Repeat] %s url=%s"%(err,url))
            else:
                writeLog('E',"[DatabaseError] %s url=%s"%(err,url))
    except AttributeError as error:
        writeLog('E',"[AttributeError] %s url=%s"%(error,url))
    
    except ValueError as error:
        writeLog('E',"[ValueError] %s url=%s"%(error, url))
    
    except requests.ConnectionError as error:
        writeLog('E',"[ConnectError] %s url=%s"%(error,url))
    #print content
    except requests.exceptions.ConnectionError as error:
	writeLog('E',"[Request_Connect] %s url=%s"%(error,url))
    except Exception as error:
	writeLog('E',"[Error] %s url=%s"%(error,url))
	
def getUrl(url,bool_page,shift):
    global file_
    res = requests.get(url)
    soup = BeautifulSoup(res.text,"lxml")
    div = soup.find("div","abdominis rlby clearmen")
    div = div.find_all('a')
    if shift:
        get_url = div[:-12]
    else:
        get_url = div[:-11]
    #print getpage

    for con in get_url:
        con = con.get('href')
        next_url = "https://tw.appledaily.com"+con        
        getNews(next_url)
           
    if bool_page:
        getpage = div[32:]
        for page in getpage:
            page_url = page.get('href')
            next_page = "https://tw.appledaily.com"+page_url
            title = page.get('title')
            #print title
            if title==u"下10頁":
                bool_page=True
                shift = True
            else:
                bool_page=False
            title = title.encode('utf-8')
			writeLog("I","[Page] %s"%title)
            getUrl(next_page,bool_page,shift)
            
if __name__ == '__main__': 
    kind_dict = {u'社會':1,u'娛樂':2,u'生活':3,u'體育':4,u'國際':5,u'政治':6,u'財經':7,u'3C':8}
    jieba.set_dictionary('dict.txt.big')
    file_ = open('apple_news.log','a')
    url = "https://tw.appledaily.com/hot/realtime/"
    bool_page = True
    shift = False
    getUrl(url,bool_page,shift)
    writeLog("I", "Finish")
    file_.close()
    
