
# coding: utf-8

import requests
import lxml
from bs4 import BeautifulSoup
import MySQLdb
import jieba.posseg as pseg
import jieba

def getNews(url,db):
    res = requests.get(url)
    soup = BeautifulSoup(res.text,"lxml")
    title = soup.find("title").text
       
    date = soup.find("time").text.strip() 
    date = date.replace(u"年","-")
    date = date.replace(u"月","-")
    date = date.replace(u"日","")
    date +=":00"
    
    kinds = soup.find(attrs={"name":"section"})['content']
       
    keywords = soup.find(attrs={"name":"news_keywords"})['content']  
        
    content = soup.find("div","clummbox clear-fix").find_all("p")
    text=""
    for i in content:
        text=text+i.text
        content = text

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
    
    #insert data into database      
    sql = "INSERT INTO news(Link, Title, Content, Kinds, Post_time, Keywords)                VALUES (%s,%s,%s,%s,%s,%s)"
	cursor = db.cursor()
    cursor.execute(sql,(url, title, content , kinds, date, keyword_string))
    db.commit()
    db.close()
    
if __name__ == '__main__':   
    jieba.set_dictionary('dict.txt.big')
    hotNews = "http://www.chinatimes.com/hotnews/click"
    res = requests.get(hotNews)
    soup = BeautifulSoup(res.text,"lxml")
    url_search = soup.find_all("div","content")
    url_search[10:]=()
    for i in url_search:
        url = i.find("a").get("href")
        title = i.find("a").text
		db = MySQLdb.connect(host="",user="", passwd="",db="", charset="utf8")
    	cursor = db.cursor()

    	repeat = "SELECT * FROM news where link='%s';"%url
    	cursor.execute(repeat)
		if not cursor.rowcount:
			print "enter"  
			getNews(url,db)
		else:
			print "Error"
			db.close()
