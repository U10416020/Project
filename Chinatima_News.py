
# coding: utf-8

# In[1]:

import requests
import lxml
from bs4 import BeautifulSoup
import MySQLdb

def getNews(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.text,"lxml")
    print soup
    title = soup.find("title").text
    print "Title: "+title
    
    time = soup.find("time")
    print "Time: "+time['datetime']
    
    date = soup.find("time").text.strip()    
    print "Date: "+date
    
    description = soup.find("meta",property="og:description")
    print "Description: "+description['content']
    
    content = soup.find("div","clummbox clear-fix").find_all("p")
    print "Content: "
    text=""
    for i in content:
        text=text+i.text
    print text
    
hotNews = "http://www.chinatimes.com/hotnews/click"
res = requests.get(hotNews)
soup = BeautifulSoup(res.text,"lxml")
getNews("http://www.chinatimes.com/realtimenews/20180313001125-260407")
url_search = soup.find_all("div","content")
url_search[10:]=()
for i in url_search:
    url = i.find("a").get("href")
    title = i.find("a").text
    getNews(url)


# In[1]:

import requests
import lxml
from bs4 import BeautifulSoup
res = requests.get("http://www.chinatimes.com/realtimenews/20180315000891-260402")
soup = BeautifulSoup(res.text,"lxml")
title = soup.find("title").text
print "Title: "+title
print soup


keywords = soup.find(attrs={"name":"news_keywords"})['content']  
print keywords


# In[ ]:



