
# coding: utf-8

import requests
import lxml
from bs4 import BeautifulSoup
from datetime import datetime, date
import MySQLdb
from itertools import izip
import jieba.posseg as pseg
import jieba

def writeLog(level, message):
    global file_
    message = "Log %s %s %s" % (level, datetime.now(), message)
    file_.write("%s\n"%message)

def writeFile(kind_number,keywords):
    if kind_number==0:
        f=open('keyword/Other.txt','a')
    elif kind_number ==1:
        f=open('keyword/Society.txt','a')
    elif kind_number == 2:
        f=open('keyword/Entertainment.txt','a')
    elif kind_number == 3:
        f=open('keyword/Life.txt','a')
    elif kind_number == 4:
        f=open('keyword/Sport.txt','a')
    elif kind_number==5:
        f=open('keyword/International.txt','a')
    elif kind_number==6:
        f=open('keyword/Politic.txt','a')
    elif kind_number ==7:
        f=open('keyword/Finance.txt','a')
    elif kind_number == 8:
        f=open('keyword/Technology.txt','a')
    else :
        f=open('Test.txt','a')    
        
    for key in keywords:
        if key!=u' ':
            key = key.encode('utf-8')    
            f.write(key+" 20 n\n")
    f.close() 
    return f.name 
def getNews(url,kind):
    try:
        res = requests.get(url)
        soup = BeautifulSoup(res.text,"lxml")
        #print "URL:"+url
        #title = soup.title.string 
    
        if kind == u'娛樂' or kind == u'日韓' or kind == u'華流':
            title = soup.find(id="newsTitle").text.strip()
            date = soup.find("div","time").text.strip()
            content = soup.find("div","Content2").text.strip()
            keywords = soup.find(attrs={"name":"keywords"})['content'].strip()  
        else:
            title = soup.find("h1","news-title-3").text.strip()
            date = soup.find("time","page-date").text.strip()
            content = soup.find("div",id="Content1").text.strip() 
            keywords = soup.find(attrs={"name":"Keywords"})['content'].strip()
        date=date.replace("/","-")
        date = datetime.strptime(date,"%Y-%m-%d %H:%M:%S")
        #print date

        kind_number = kind_dict.get(kind,0)
        #print kind_number
        while keywords.endswith(",") or keywords.endswith(" "):
            keywords = keywords[:-1]
        keywords = keywords.split(",")
        
        f = writeFile(kind_number,keywords)
        jieba.load_userdict(f)
        words = pseg.cut(content)
        keyword_string=""
        for word in words:
            if word.flag == 'n'and keyword_string.find(word.word)==-1:
                keyword_string+=word.word+","
                #print word.word, word.flag 
        keyword_string=keyword_string[:-1]
        source = u"三立"
        try:
            db = MySQLdb.connect(host="localhost",user="wkps1015", passwd="wkps1015",db="Crawl", charset="utf8")
            cursor = db.cursor()
        
            sql = "INSERT INTO news(Link, Title, Content, Kinds, Post_time, Keywords, Source)                VALUES (%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sql,(url, title, content , kind_number, date, keyword_string, source))
            db.commit()
            db.close()
        except MySQLdb.Error as err:
	    if 1062 in err:
            	writeLog('E',"[Repeat] %s url=%s"%(err,url))
            else:
		writeLog('E',"[DatabaseError] %s url=%s"%(err,url))
    except AttributeError as error:
        writeLog('E',"[AttributeError] %s url=%s"%(error,url))
        
    except requests.ConnectionError as error:
        writeLog('E',"[ConnectError] %s url=%s"%(error,url))     

    except requests.exceptions.ConnectionError as error:
        writeLog('E',"[Request_Connect] %s url=%s"%(error,url))
    except Exception as error:
	writeLog('E',"[ERROR] %s url=%s"%(error,url))
def getUrl(page):  
    try:
        res = requests.get(page)
        soup = BeautifulSoup(res.text,"lxml")
	news = soup.find("div","row NewsList")
        url = news.find_all("a","gt")
        kind_all = news.find_all("div","newslabel-tab")
        
        for href, kind in izip(url,kind_all):
            href = href.get("href")
            kind = kind.text
            getNews("http://www.setn.com"+href,kind)
        
        if page=="http://www.setn.com/ViewAll.aspx?PageGroupID=0":            
            nextPage = soup.find("div","pagination-area")
            nextPage = nextPage.find_all("a")
            changePage = nextPage[3:-2]            
            for change in changePage:          
                change = change.get("href")
                getUrl("http://www.setn.com"+change)

    except AttributeError as error:
        writeLog('E',"[AttributeError] %s  url=%s"%(error,page))
    except requests.ConnectionError as error:
        writeLog('E',"[ConnectError] %s url=%s"%(error,page)) 
    except Exception as error:
	writeLog('E',"[ERROR] %s url=%s"%(error,page))
if __name__ == '__main__':  
    kind_dict = {u'社會':1,u'日韓':2,u'娛樂':2,u'華流':2,u'生活':3,u'運動':4,u'國際':5,u'大陸':5,u'政治':6,u'財經':7,u'科技':8}
    jieba.set_dictionary('dict.txt.big')
    file_ = open('set_news.log','a')
    hotNews = "http://www.setn.com/ViewAll.aspx?PageGroupID=0"
    getUrl(hotNews)
    writeLog("I", "Finish")
    file_.close()
