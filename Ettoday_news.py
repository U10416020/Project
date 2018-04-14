
# coding: utf-8

# In[18]:


import requests
import lxml
from bs4 import BeautifulSoup
import MySQLdb
import jieba.posseg as pseg

def getNews(url):
    res = requests.get(url)
    #print res.text
    #soup = BeautifulSoup(res.text,"html.parser")
    soup = BeautifulSoup(res.text,"lxml")

    title = soup.title.string
    print "Title: "+title

    date = soup.find("time").text
    print date
    #keywords = soup.find("meta",attrs={'name':'news_keywords'})
    #print keywords['content']
    keywords = soup.find(attrs={"name":"news_keywords"})['content']  
    print keywords
    
    description = soup.find("meta",property="og:description")
    print "Description: "+description["content"]
    
    content = soup.find("div","story").find_all("p")    
    text=""
    for i in content:
        text=text+i.text
    print "Content: "+text
    words = pseg.cut(text)
    for word in words:
        if word.flag.find('n') !=-1:
            print word.word, word.flag
    
jieba.set_dictionary('dict.txt.big')
res = requests.get("https://www.ettoday.net/news/hot-news.htm")
soup = BeautifulSoup(res.text,"lxml")
#url = soup.find_all("div","piece clearfix")
#url = soup.find_all("h3")
url = soup.find_all('a',"pic")
url[50:]=()
#print "URL!!!"
#print url
for i in url:
    print "content:"+i.text
    href=i.get("href")
    print "HREF:"+href
    getNews("https://www.ettoday.net/"+href)


# In[31]:


import requests
import lxml
import jieba
import jieba.posseg as pseg
#import jieba.analyse
from bs4 import BeautifulSoup
jieba.set_dictionary('dict.txt.big')
jieba.load_userdict("Test.txt")
#res = requests.get("https://star.ettoday.net/news/1130434")
#res = requests.get("https://www.ettoday.net/news/20180315/1130644.htm")
res = requests.get("https://www.ettoday.net/news/20180409/1147040.htm")
#res = requests.get("https://www.ettoday.net/news/20180409/1146992.htm")

soup = BeautifulSoup(res.text,"lxml")
content = soup.find("div","story").text.strip() 
#print "Content: "+content
#print soup
date = soup.find("time").text
print date
#keywords = soup.find("meta",attrs={'name':'news_keywords'})
#keywords = keywords['content']
keywords = soup.find(attrs={"name":"news_keywords"})['content']
while keywords.endswith(","):
    keywords = keywords[:-1]
keywords = keywords.split(",")
print keywords

f = open('Test.txt','a')
for key in keywords:
    key = key.encode('utf-8')
    f.write(key+" 20 n\n")
f.close()

description = soup.find("meta",property="og:description")
description = description["content"]
print "Description: "+description

content = soup.find("div","story").find_all("p")    
text=""
for i in content:
    text=text+i.text
print "Content: "+text


words = jieba.cut(description)
for word in words:
    print word
    
words = pseg.cut(text)
for word in words:
    if word.flag.find('n') !=-1:
        print word.word, word.flag

#tags = jieba.analyse.extract_tags(text, 10)
#print "Output："
#print ",".join(tags)


# In[ ]:



