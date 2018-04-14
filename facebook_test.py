
# coding: utf-8

# In[54]:

import requests
import json
token = 'EAACEdEose0cBAPIr4wJf5F8YzmQqxGVBN3XWZCuZATN6cpkx6FAHejFrdv9QFRfZBNwAXeKj5i8vh8Sq5J09mDxjv3iPLDypLGr94lLpCcOS5UQPhCTuhPnZBhfotbTZB4XyM6yVIf7ZAoRa4RZAccWWWq3eleZA3njZAixPkT5QR15QMTqmo5YdoV09TLkDWZCk0ZD' #貼上token
res=requests.get("https://graph.facebook.com/v2.11/me?fields=likes&&access_token=%s"%(token))
#print res.text
#data = res.json
#print data['likes']
jsondata = json.loads(res.text)
news={}
for data in jsondata['likes']['data']:
    name = data['name']
    id = data['id']
    print name
    print id
    news[name]=id
print jsondata['likes']['data'][0]['name']


# In[ ]:



