
# coding: utf-8

# In[17]:

import requests
import lxml
from bs4 import BeautifulSoup
import MySQLdb
from itertools import izip

def getNews(url,kind):
    res = requests.get(url)
    #print res.text
    #soup = BeautifulSoup(res.text,"html.parser")
    soup = BeautifulSoup(res.text,"lxml")

    #title = soup.title.string    
    if kind == u'娛樂' or kind == u'日韓' or kind == u'華流':
        title = soup.find(id="newsTitle").text
        date = soup.find("div","time").text
        content = soup.find("div","Content2").text.strip()
    else:
        title = soup.find("div","title").text.strip()
        date = soup.find("span","date").text
        content = soup.find("div",id="Content1").text.strip() 
        
        
    print "Title: "+title
    
    print "Date: "+date
    description = soup.find("meta",property="og:description")
    print "Description: "+description["content"]
    
    print "Content: "+content

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
        print "Title:"+title
        kind = j.text
        print "Kind: "+kind       
        href=i.get("href")
        print "HREF:"+href
        getNews("http://www.setn.com"+href,kind) 
       
    if page!= lastPage:
        getUrl("http://www.setn.com"+changePage)

hotNews = "http://www.setn.com/ViewAll.aspx?PageGroupID=0"
getUrl(hotNews)


# In[17]:

import requests
import lxml
from bs4 import BeautifulSoup
res = requests.get("http://www.setn.com/News.aspx?NewsID=357539")
soup = BeautifulSoup(res.text,"lxml")
#description = soup.find("meta",property="og:description")
#print "Description: "+description["content"]
description = soup.find(attrs={"name":"Description"})['content']  
print "Desciprtion : "+description
keywords = soup.find(attrs={"name":"Keywords"})['content']  
print keywords

print soup


# In[5]:




# In[ ]:



