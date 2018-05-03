
# coding: utf-8

import requests
import lxml
from bs4 import BeautifulSoup
import MySQLdb
from itertools import izip
import jieba.posseg as pseg
import jieba

def getNews(url,kind):
    res = requests.get(url)
    #print res.text
    #soup = BeautifulSoup(res.text,"html.parser")
    soup = BeautifulSoup(res.text,"lxml")
    #print "URL:"+url
    #title = soup.title.string    
    if kind == u'娛樂' or kind == u'日韓' or kind == u'華流':
        title = soup.find(id="newsTitle").text.strip()
        date = soup.find("div","time").text.strip()
        content = soup.find("div","Content2").text.strip()
        keywords = soup.find(attrs={"name":"keywords"})['content'].strip()  
    else:
        title = soup.find("div","title").text.strip()
        date = soup.find("span","date").text.strip()
        content = soup.find("div",id="Content1").text.strip() 
        keywords = soup.find(attrs={"name":"Keywords"})['content'].strip()
    
    while keywords.endswith(","):
        keywords = keywords[:-1]
    keywords = keywords.split(",")
    
    f = open('Test.txt','w')
    for key in keywords:
        key = key.encode('utf-8')
        f.write(key+" 20 n\n")
    f.close() 
    
    jieba.load_userdict("Test.txt")
    words = pseg.cut(content)
    keyword_string=""
    for word in words:
        if word.flag == 'n'and keyword_string.find(word.word)==-1:
            keyword_string+=word.word+","
            #print word.word, word.flag 
    keyword_string=keyword_string[:-1]
    if content.find("'") != -1:
    	content_string = content.split("'")
    	content=""
    	for con in content_string:
        	content+=con 
    db = MySQLdb.connect(host="",user="", passwd="",db="testdb", charset="utf8")
    cursor = db.cursor()
    
    repeat = "SELECT * FROM news where link='%s';"%(url)
    cursor.execute(repeat)
    if not cursor.rowcount:        
        sql = "INSERT INTO news(Link, Title, Content, Kinds, Post_time, Keywords)                VALUES ('%s', '%s', '%s', '%s', '%s', '%s' )" %                (url, title, content , kind, date, keyword_string)
        # 插入資料
        cursor.execute(sql)
        db.commit()

    db.close()

def getUrl(page):    
    res = requests.get(page)
    soup = BeautifulSoup(res.text,"lxml")
    url = soup.find_all("a","gt")
    kind_all = soup.find_all("div","tab_list_type")
    nextPage = soup.find("div","pager")
    nextPage = nextPage.find_all("a")
    changePage = nextPage[len(nextPage)-1].get("href")
    lastPage = "http://www.setn.com"+nextPage[len(nextPage)-2].get("href")
    url[30:]=()
    for i,j in izip(url,kind_all):
        title = i.text
        #print "Title:"+title
        kind = j.text
        #print "Kind: "+kind       
        href=i.get("href")
        #print "HREF:"+href
        getNews("http://www.setn.com"+href,kind) 
       
    if page!= lastPage:
        getUrl("http://www.setn.com"+changePage)

if __name__ == '__main__':  
    jieba.set_dictionary('dict.txt.big')
    hotNews = "http://www.setn.com/ViewAll.aspx?PageGroupID=0"
    getUrl(hotNews)

