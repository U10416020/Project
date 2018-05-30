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
        #print soup
    
        title = soup.find("title").text
        #print "Title: "+title

        date = soup.find("time").text.strip()    
        date = date.replace(u"年","-")
        date = date.replace(u"月","-")
        date = date.replace(u"日","")
        date +=":00"
        date = datetime.strptime(date,"%Y-%m-%d %H:%M:%S")
        #print date
      
        kinds = soup.find(attrs={"name":"section"})['content']
        #print kinds
        kind_number = kind_dict.get(kinds,0)
        #print kind_number
        
        keywords = soup.find(attrs={"name":"news_keywords"})['content']  
        #print keywords

        content = soup.find("div","clummbox clear-fix").find_all("p")
        #print "Content: "
        text=""
        for i in content:
            text=text+i.text
        #print text
        content = text
        while keywords.endswith(","):
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
        
        try:
            db = MySQLdb.connect(host="localhost",user="", passwd="",db="", charset="utf8")
            cursor = db.cursor()
            sql = "INSERT INTO news(Link, Title, Content, Kinds, Post_time, Keywords)                VALUES (%s,%s,%s,%s,%s,%s)"
                # 插入資料
            cursor.execute(sql,(url, title, content , kind_number, date, keyword_string))
            db.commit()
            db.close()
        except MySQLdb.Error as err:
			if 1062 in err:
                writeLog('E',"[Repeat] %s url=%s"%(err,url))
            else:
                writeLog('E',"[DatabaseError] %s url=%s"%(err,url))
    except AttributeError as error:
        writeLog('E',"[AttributeError] %s  url=%s"%(error,url))
        
    except requests.ConnectionError as error:
        writeLog('E',"[ConnectError] %s url=%s"%(error,url))
   
    except requests.exceptions.ConnectionError as error:
        writeLog('E',"[Request_Connect] %s url=%s"%(error,url))
    except Exception as error:
		writeLog('E',"[Error] %s url=%s"%(error,url))
if __name__ == '__main__':   
    kind_dict = {u'社會':1,u'娛樂':2,u'娛樂新聞':2,u'生活新聞':3,u'生活':3,u'健康':3,u'體育':4,u'國際':5,u'兩岸':5,u'國際大事':5,u'政治':6,u'政治要聞':6,u'財經要聞':7,u'財經':7}
    jieba.set_dictionary('dict.txt.big')
    file_ = open('chinatime_news.log','a')
    hotNews = "http://www.chinatimes.com/hotnews/click"
    try:        
        res = requests.get(hotNews)
        soup = BeautifulSoup(res.text,"lxml")
        url_search = soup.find_all("div","content")
        url_search[10:]=()
        for i in url_search:
            url = i.find("a").get("href")
            title = i.find("a").text
            getNews(url)
    except requests.ConnectionError as error:
        writeLog('E',"[ConnectError] %s url=%s"%(error,hotNews))
	except Exception as error:
		writeLog('E',"[Error] %s url=%s"%(error,hotNews))
    writeLog("I", "Finish")
    file_.close()
