# -*- coding: utf-8 -*-
"""
Created on Mon Dec 29 14:00:06 2014

@author: NUS-ISS TEAM
"""
import MySQLdb
import twitter
import json
import feedparser
from bs4 import BeautifulSoup
import urllib2
import time
import datetime
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

connect = MySQLdb.connect("localhost","NUSISS","password","dailymotionapp")
cur = connect.cursor()
############################### Twitter ################################

CONSUMER_KEY = 'Yh29IuH0ndtxH6vumCuTbXfgM'
CONSUMER_SECRET = '3U47dQUNKgK10GsdqFWAIZhK1FXMAgsH7202D2unFfTlFL7tO3'
OAUTH_TOKEN = '2601327644-vR76nR8f3OmmHovovjhGP9xnbwYvhObOGMWE8MK'
OAUTH_TOKEN_SECRET = 'LBbepbSp0iOAeyW8UDKLNpt43ZUSkzh866N4whFQ3mMdE'

auth = twitter.oauth.OAuth(OAUTH_TOKEN,OAUTH_TOKEN_SECRET,CONSUMER_KEY,CONSUMER_SECRET)

twitter_api = twitter.Twitter(auth=auth)

print twitter_api

India_ID = 2295420
trend_region="India"
world_trends = twitter_api.trends.place(_id=India_ID)
print json.dumps(world_trends,indent=1)

trend_name=[]
timezone=[]
dat=[]
#index=[]
lang="English"
trendscore = 1
temporality = "Short Term"
status=[]
status_text=[]
status_names=[]
status_lang=[]
gender=[]
count = 1
trend_url=[]
cur.execute("SELECT * FROM TRENDS_ALL")
rows =cur.fetchall()
for var in rows:
    dat.append(var[1])
    #index.append(var[5])

for trend in world_trends[0]['trends']:
    trend_name.append(trend['name']) # Trend HashTag
    trend_url.append(trend['url'])
    #print trend['as_of']
    print trend['name']
    for date in world_trends:
        #created_date =(date['created_at'])
        dated= date['as_of'].replace("T",' ').replace("Z",'')
        #print date['created_at']
        search_tweet = twitter_api.search.tweets(q=trend['name'],count =count)
        stats = search_tweet['statuses']
        status.append(stats)
        status_text.append([status1['text'] for status1 in stats])
        status_names.append([name['user']['name'] for name in stats])
    if ' ' in str(name['user']['name']):
        stats = name['user']['name'].split()
        try:
            if stats[1]:
                take = stats[0]
                take1 = stats[1]
                data1 = json.load(urllib2.urlopen("https://gender-api.com/get?name="+str(take)+"&key=AXBxyGlwqpuzMSeuvK"))
        except:
            take = stats[0]
            data1 = json.load(urllib2.urlopen("https://gender-api.com/get?name="+str(take)+"&key=AXBxyGlwqpuzMSeuvK"))
        if data1["gender"] == "unknown":
            data1 = json.load(urllib2.urlopen("https://gender-api.com/get?name="+str(take1)+"&key=AXBxyGlwqpuzMSeuvK"))
    else:
        take = str(name['user']['name']).split()
        data1 = json.load(urllib2.urlopen("https://gender-api.com/get?name="+str(take)+"&key=AXBxyGlwqpuzMSeuvK"))
    #for var in rows:
    if str(trend['name']) in dat:
        ts = time.time()
        datedw = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        up_ID = 1#var[5]+1
        cur.execute("UPDATE TRENDS_ALL SET Updated_DATE =%s,Update_ID=%s WHERE Trend_Name =%s LIMIT 1 ",(datedw,up_ID,str(trend['name'])))
        connect.commit()            
        print "Inside old"
    else:
        Trend_Source ="Twitter"
        up=1
        cur.execute("INSERT INTO TRENDS_ALL (Trend_Name,Trend_Description,Trend_Language,Created_DATE,Update_ID,Trend_Score,Trend_Temporality,Trend_Sex,Trend_Region,Trend_Source,Trend_ExternalLinks) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(str(trend['name']),str(status1['text']),lang,dated,up,trendscore,temporality,str(data1["gender"]),trend_region,Trend_Source,str(trend['url'])))
        connect.commit()            
        print "Inside new"
        
def datab(data,Trend_Source,Link):
    #for news in rows:
    ts = time.time()
    dated = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    #print news[1]
    if str(data) in dat:
        up_ID = 1#news[5]+1
        cur.execute("UPDATE TRENDS_ALL SET Updated_DATE =%s,Update_ID=%s WHERE Trend_Name =%s LIMIT 1 ",(dated,up_ID,str(data)))
        connect.commit()            
        print "Inside old"
    else:
        up=1
        cur.execute("INSERT INTO TRENDS_ALL (Trend_Name,Trend_Description,Trend_Language,Created_DATE,Update_ID,Trend_Score,Trend_Temporality,Trend_Region,Trend_Source,Trend_ExternalLinks) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(str(data),str(data),lang,dated,up,trendscore,temporality,trend_region,Trend_Source,Link))
        connect.commit()            
        print "Inside new"
        

############################### Twitter ################################

############################### Google News ################################

gnews = feedparser.parse("https://news.google.com.sg/news/feeds?cf=all&ned=in&hl=en&output=rss")
for i in range (0,len(gnews['entries'])):
    Trend_Source ="Google News"
    print gnews['entries'][i]['title']
    link = gnews['entries'][i]['link']
    datab(gnews['entries'][i]['title'][:150],Trend_Source,link)
    
############################### Google News ################################

############################### Google Trends ################################

page1 = urllib2.urlopen("http://www.google.com/trends/?geo=IN")
soup = BeautifulSoup(page1)
a2= soup.find_all("div",{'class' :'landing-page-hottrends-single-trend-container'})
b2= soup.find_all("span",{'class' :'hottrends-single-trend-info-line-number'})
for i in range (0,len(a2)):
    Trend_Source ="Google Trends"
    print a2[i].attrs['id'] #,b2[i].contents[0]
    link = "http://www.google.com/trends/?geo=IN"
    datab(a2[i].attrs['id'][:150],Trend_Source,link)
 
############################### Google Trends ################################

############################### CNN IBN Live News ############################

ibn = feedparser.parse("http://ibnlive.in.com/ibnrss/top.xml")
for i in range(0,len(ibn['entries'])):
    Trend_Source ="CNNIBN NEWS"
    print "News ID:%s & Title:%s"%(str(i),ibn['entries'][i]['title'])
    link = ibn['entries'][i]['link']
    datab(ibn['entries'][i]['title'][:150],Trend_Source,link)
	
############################### CNN IBN Live News ############################
 
############################### NDTV News ################################ 
ndtv = feedparser.parse("http://feeds.feedburner.com/NDTV-Trending?format=xml")
print ndtv['feed']['title']
for i in range (0,len(ndtv['entries'])):
    Trend_Source ="NDTV News"
    print "News Type : %s || Title: %s"%(ndtv['entries'][i]['category'],ndtv['entries'][i]['title'])
    link = ndtv['entries'][i]['link'] 
    datab(ndtv['entries'][i]['title'][:150],Trend_Source,link)
############################### NDTV News ################################
 

cur.execute("SELECT * FROM TRENDS_ALL")
newrow=cur.fetchall()
for row in newrow:
    print row
cur.close

#INSERT INTO TRENDS(Trend_Name,Created_DATE,Update_ID) VALUES("#PKwithPhilips","2014-12-24 03:51:16Z","1") 
#UPDATE TRENDS SET Updated_DATE ='2014-12-24 04:40:38' WHERE Trend_Name = "#PKwithPhilips"
