
# coding: utf-8

import requests
import lxml
from bs4 import BeautifulSoup
import MySQLdb
import jieba.posseg as pseg
import jieba

def getNews(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.text,"lxml")

    title = soup.title.string
    #print "Title: "+title

    date = soup.find("time").text.strip()
    #print date
    
    kinds = soup.find(attrs={"name":"section"})['content']
    #print "Kinds: "+kinds
    
    keywords = soup.find(attrs={"name":"news_keywords"})['content']  
    
    while keywords.endswith(","):
        keywords = keywords[:-1]
    keywords = keywords.split(",")
    #print keywords
    
    f = open('Test.txt','w')
    for key in keywords:
        key = key.encode('utf-8')
        f.write(key+" 20 n\n")
    f.close() 
    
    
    description = soup.find("meta",property="og:description")
    #print "Description: "+description["content"]
    
    content = soup.find("div","story").find_all("p")    
    text=""
    for i in content:
        text=text+i.text
    #print "Content: "+text
    
    jieba.load_userdict("Test.txt")
    words = pseg.cut(text)
    keyword_string=""
    for word in words:
        if word.flag == 'n'and keyword_string.find(word.word)==-1:
            keyword_string+=word.word+","
            #print word.word, word.flag 
    keyword_string=keyword_string[:-1]
    #print keyword_string
            
    db = MySQLdb.connect(host="",user="", passwd="",db="testdb", charset="utf8")
    cursor = db.cursor()
    
    repeat = "SELECT * FROM news where link='%s';"%(url)
    cursor.execute(repeat)
    if not cursor.rowcount:        
        sql = "INSERT INTO news(Link, Title, Content, Kinds, Post_time, Keywords)                VALUES ('%s', '%s', '%s', '%s', '%s', '%s' )" %                (url, title, text , kinds, date, keyword_string)
        # 插入資料
        cursor.execute(sql)
        db.commit()

    db.close()
    
if __name__ == '__main__':     
    jieba.set_dictionary('dict.txt.big')
    ettoday_url="https://www.ettoday.net"
    res = requests.get("https://www.ettoday.net/news/hot-news.htm")
    soup = BeautifulSoup(res.text,"lxml")
    url = soup.find_all('a',"pic")
    url[50:]=()

    for i in url:
        #print "content:"+i.text
        href=i.get("href")
        #print "HREF:"ettoday_url+href
        getNews(ettoday_url+href)

