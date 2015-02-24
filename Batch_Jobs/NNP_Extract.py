# -*- coding: utf-8 -*-
"""
@author: HP
"""
import twitter
import nltk
import nltk.data
from collections import Counter
from nltk import word_tokenize
from nltk.corpus import stopwords
import re
import string
from ttp import ttp
import MySQLdb

text=[]
text1=[]
data_news=[]
news_stops = set([u'Zee',u'Daily',u'News',u'Times',u'India'])
tweet_stops =set(["\\","u'RT","``"])
final_dta={}
final_dtas={}
status_text=[]
docs={}
docs_twitter={}
abc=[]
data_nnp=[]
CONSUMER_KEY = 'Yh29IuH0ndtxH6vumCuTbXfgM'
CONSUMER_SECRET = '3U47dQUNKgK10GsdqFWAIZhK1FXMAgsH7202D2unFfTlFL7tO3'
OAUTH_TOKEN = '2601327644-vR76nR8f3OmmHovovjhGP9xnbwYvhObOGMWE8MK'
OAUTH_TOKEN_SECRET = 'LBbepbSp0iOAeyW8UDKLNpt43ZUSkzh866N4whFQ3mMdE'

auth = twitter.oauth.OAuth(OAUTH_TOKEN,OAUTH_TOKEN_SECRET,CONSUMER_KEY,CONSUMER_SECRET)

twitter_api = twitter.Twitter(auth=auth)

conn = MySQLdb.connect("localhost","NUSISS","password","dailymotionapp")
cursor = conn.cursor()
cursor.execute("SELECT * FROM TRENDS_ALL")
rows = cursor.fetchall()
cursor.execute("SELECT * FROM TRENDS_NNP")
nnps = cursor.fetchall()
for nnp in nnps:
    data_nnp.append(nnp[0])
    
for i in range(len(rows)):
    if rows[i][15] == "Twitter":
        if rows[i][0] not in data_nnp:
            print rows[i][0]
            text.append(rows[i][1])
    else:
        if rows[i][0] not in data_nnp:
            print rows[i][0]
            text1.append(rows[i][2])

punctuations = list(string.punctuation)
english_stops = set(stopwords.words('english'))
data_twitter=[]
count =30
for i in range(len(text)):
    search_tweet = twitter_api.search.tweets(q=text[i],count =count)
    stats = search_tweet['statuses']
    status_text.append([status1['text'] for status1 in stats])
    for i in range(len(status_text)):
        p = ttp.Parser()
        result = p.parse(str(status_text[i]))
    a = result.users
    for row in rows:
        if row[1] == text[i]:
            if row[0] not in data_nnp:
                tweet = row[0]        
    for tweets in range(len(status_text)):
        b_tweet = nltk.pos_tag(word_tokenize(re.sub(r"http\S+", "", str(status_text[tweets]))))
        d_tweet = [j for j in b_tweet if j[0] not in punctuations]
        d1_tweet = [word for word in d_tweet if word[0] not in english_stops]
        for i in d1_tweet:
            d2_tweet = [word for word in i if word not in a]
            for word in d2_tweet:
                if "\\" not in d2_tweet[0] and "u'RT" not in d2_tweet[0] and "u'" not in d2_tweet[0] and "``" not in d2_tweet[0] and "''" not in d2_tweet[0] and "RT" not in d2_tweet[0]:
                    if(word=='NN' or word=='NNP' or word=='NNS' or word=='NNPS'):
                        print d2_tweet
                    try:
                        if d2_tweet[1]:
                            data_twitter.append(d2_tweet[0])
                    except:
                        print "None"
        abc =[]
        top=[]
        abc.append(Counter(data_twitter).most_common(10))
        for j in range(0,10):
            print top.append(abc[0][j][0])
        final_dtas[tweet]=set(top)
        data_twitter =[]

for key,val in final_dtas.iteritems():
    stri =''
    for values in val:
        stri = stri + ' '+str(values)    
        docs_twitter[key] = stri

for i in range(len(text1)):
    b = nltk.pos_tag(word_tokenize(text1[i]))
    for row in rows:
        if row[1] == text1[i]:
            if row[0] not in data_nnp:
                doc = row[0]
    #doc = 'doc'+str(i)
    #print doc
    b1 = [n1 for n1 in b if n1[0] not in news_stops]
    for k in b1:
        for l in k:
            if(l=='NN' or l=='NNP' or word=='NNS' or word=='NNPS'):
                data_news.append(k[0])
                print k[0]
    final_dta[doc]=data_news
    data_news =[]


for key,val in final_dta.iteritems():
    stri =''
    for values in val:
        stri = stri + ' '+str(values)    
        docs[key] = stri

sum_doc =dict(docs.items() + docs_twitter.items())

for key,val in sum_doc.iteritems():
    print key
    print val
    try:
        cursor.execute("INSERT INTO TRENDS_NNP (TECHNICAL_ID,TRENDS_NNP_TexT) VALUES (%s,%s)",(key,val))
        conn.commit()
    except:
        print "Some key error "+(str(key))

conn.close()
