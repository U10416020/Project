
# coding: utf-8

# In[84]:


import requests
import lxml
import re
from bs4 import BeautifulSoup

#res=requests.get("https://tw.news.appledaily.com/local/realtime/20180131/1289265/")
#res = requests.get("https://tw.news.appledaily.com/international/realtime/20180131/1288846/")
#res = requests.get("https://goo.gl/CDB6w2")
#res = requests.get("https://tw.sports.appledaily.com/realtime/20180201/1289801/")
#res = requests.get("https://goo.gl/baE3Cp")
res = requests.get("https://goo.gl/pmXT6X")
#print res.text
soup = BeautifulSoup(res.text,"html.parser")
#soup = BeautifulSoup(res.text,"lxml")

#print soup
title = soup.title.string
print "Title: "+title

content = soup.find("div","ndArticle_margin").p
print content

span = str(content.span)

#print strong
content_new = str(content)
content_new = content_new[content_new.find("<p>")+len("<p>"):]
#print content_new
result = re.findall("報導\)|報導\）",content_new)
content_new = content_new[:content_new.find(result[0])+len(result[0])]
#content_new = content_new[:re.search(")|）",content_new)]
#print content_new
strong = content.find_all('strong')
#count=0
if strong!=[]:
    for value in strong:
        value = str(value)
        if(content_new.find(value)!=-1):            
            if content_new.find(value)<(len(content_new)/2):
                content_new= content_new[content_new.find(value)+len(value):]
            else:
                content_new = content_new[:content_new.find(value)]

#content_new = content_new.split("<br/><br/>")
content_new = re.split("<br/>",content_new)
#\xc2\xa0
content_new1=""
for value in content_new:
    content_new1+=value
if content_new1.find(span)!=-1:
    content_span = content_new1.split(span)    
    span = span[span.find(">")+1:]
    span = span[:span.find("<")]    
    content_new1 = content_span[0]+span+content_span[1]
print content_new1




