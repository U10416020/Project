# coding=utf-8
import requests
import lxml
from bs4 import BeautifulSoup
from datetime import datetime, date
import MySQLdb
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
        if key!=u'':
            key = key.encode('utf-8')    
            f.write(key+" 20 n\n")
    f.close() 
    return f.name 

def getNews(url):
    try:
        res = requests.get(url)
        soup = BeautifulSoup(res.text,"lxml")
    
        title = soup.title.string
        #print "Title: "+title
		kinds = soup.find(attrs={"name":"section"})['content']
		#print "Kinds: "+kinds

        date = soup.find("time").text.strip()    
        date = date.replace(u"年","-")
        date = date.replace(u"月","-")
        date = date.replace(u"日","")
		if kinds != u"寵物動物":
			if date.find(':')!=-1:
					 date+=":00"
				else:
					 date+=" 00:00:00"
			date = date.encode('utf-8')
		date = datetime.strptime(date,"%Y-%m-%d %H:%M:%S")
        #print date

        kind_number = kind_dict.get(kinds,0)
        #print kind_number
        keywords = soup.find(attrs={"name":"news_keywords"})['content']  
    
        while keywords.endswith(","):
            keywords = keywords[:-1]
        keywords = keywords.split(",")
        #print keywords
        
        content = soup.find("div","story").find_all("p") 
        text=""
        for i in content:
            text=text+i.text
        #print "Content: "+text
        
        f = writeFile(kind_number,keywords) 

        text = text.encode('utf-8')
        title = title.encode('utf-8')
        jieba.load_userdict(f)
        words = pseg.cut(text)
        keyword_string=""
        for word in words:
            if word.flag == 'n'and keyword_string.find(word.word)==-1:
                keyword_string+=word.word+","
                #print word.word, word.flag 
        keyword_string=keyword_string[:-1]
        #print keyword_string
        try:
            db = MySQLdb.connect(host="localhost",user="", passwd="",db="", charset="utf8")
            cursor = db.cursor()

            repeat = "SELECT * FROM news where link='%s';"%(url)
            cursor.execute(repeat)
            if not cursor.rowcount:        
                sql = "INSERT INTO news(Link, Title, Content, Kinds, Post_time, Keywords) \
                       VALUES (%s,%s,%s,%s,%s,%s)" 

                # 插入資料
                cursor.execute(sql,(url, title, text , kind_number, date, keyword_string))
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
    except ValueError as error:
		writeLog('E',"[ValueError] %s url=%s"%(error, url))
    except requests.exceptions.ConnectionError as error:
        writeLog('E',"[Request_Connect] %s url=%s"%(error,url))
    except Exception as error:
		writeLog('E',"[ERROR] %s url=%s"%(error,url))
if __name__ == '__main__':     
    kind_dict = {u'社會':1,u'影劇':2,u'電影':2,u'生活':3,u'消費':3,u'健康':3,u'體育':4,u'國際':5,u'大陸':5,u'政治':6,u'財經':7,u'3C家電':8}
    jieba.set_dictionary('dict.txt.big')
    file_ = open('ettoday_news.log','a')
    ettoday_url="https://www.ettoday.net"
    hotNews="https://www.ettoday.net/news/hot-news.htm"
    try:
        res = requests.get(hotNews)
        soup = BeautifulSoup(res.text,"lxml")
        url = soup.find_all('a',"pic")
        url[50:]=()

        for i in url:
            #print "content:"+i.text
            href=i.get("href")
            #print "HREF:"ettoday_url+href
            getNews(ettoday_url+href)

        writeLog("I", "Finish")
    except AttributeError as error:
        writeLog('E',"[AttributeError] %s url=%s"%(error,hotNews))
    except requests.ConnectionError as error:
        writeLog('E',"[ConnectError] %s url=%s"%(error,hotNews))
    except Exception as error:
		writeLog('E',"[ERROR] %s url=%s"%(error,hotNews))
    file_.close()
