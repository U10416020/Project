
# coding: utf-8

# In[21]:


import requests
import lxml
import json,re
from bs4 import BeautifulSoup

#Crawl news content from website
def crawlNews(url):
    res = requests.get(url)
    #print res.text
    soup = BeautifulSoup(res.text,"html.parser")

    #print soup
    title = soup.title.string
    print "Title: "+title

    content = soup.find("div","ndArticle_margin").p
    print content
    span = str(content.span)
    
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
        print span
        content_new1 = content_span[0]+span+content_span[1]
    
    print content_new1

#get posts comments
def getcomments(data):
    for comments in data['data']:
        com_message = comments['message']
        com_id = comments['id']
        print com_id+": "
        print com_message
    if 'next' in data['paging']:
        next = data['paging']['next']
        res = requests.get(next)
        commentsdata=json.loads(res.text)
        getcomments(commentsdata)
        
#Collect posts from apple news FB fans club         
token = 'EAACEdEose0cBAIKhZAOmd7gZBj4Gjh6iwHTMa5aiMYBJ9oQvevKD8EbzvLifiyIqKqJ6xilSGBel0owIQ1RVyDAGkyNN2CUV7LWs9j38ZBgBMZBAi2YHhfKoOPuXePtM4tJiWMUWmIGHQ6Yf1uCRvpC4iyvWnTRQnagDx4spmsmQ3U1yZCJZBsIZAmRfV9e0jcZD'        
res=requests.get("https://graph.facebook.com/v2.11/352962731493606?fields=posts{created_time,message,comments,story,link,shares,reactions.type(LIKE).limit(0).summary(1).as(like),reactions.type(LOVE).limit(0).summary(1).as(love),reactions.type(HAHA).limit(0).summary(1).as(haha),reactions.type(WOW).limit(0).summary(1).as(wow),reactions.type(SAD).limit(0).summary(1).as(sad),reactions.type(ANGRY).limit(0).summary(1).as(angry)}&&access_token=%s"%(token))
postdata=json.loads(res.text)

for data in postdata['posts']['data']:   
    if ('story' in data) == False:        
        time = data['created_time']
        message = data['message']
        #if 'message' in data:
         #   message = data['message']
        #else:
           # message = data['story']
        id = data['id']  
        link = data['link']
        like = data['like']['summary']['total_count']
        love = data['love']['summary']['total_count']
        haha = data['haha']['summary']['total_count']
        wow = data['wow']['summary']['total_count']
        sad = data['sad']['summary']['total_count']
        angry = data['angry']['summary']['total_count']
        if 'shares' in data:
            share = data['shares']['count']
        else:
            share = 0

        if message.find("https://")!= -1:
            videolink = link
            link = message[message.find("https://"):len(message)]
        crawlNews(link)
        print "Time: " + time +"\nmessage: "+message+"\nlink: "+link +"\nID: "+id+"\nShare: "+str(share)+"\nLike: "+str(like)+"\nLove: "+str(love)+"\nHaha: "+str(haha)+"\nWow: "+str(wow)+"\nSad: "+str(sad)+"\nAngry: "+str(angry)+"\nComments:"    
        if 'comments' in data:
            getcomments(data['comments'])


# In[ ]:



