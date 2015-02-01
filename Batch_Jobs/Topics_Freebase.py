# -*- coding: utf-8 -*-
"""
Created on Sun Jan 25 02:12:41 2015
@author: HP
"""

import MySQLdb
import json
import requests
import urllib

conn = MySQLdb.connect("localhost","NUSISS","password","dailymotionapp")
cursor = conn.cursor()
cursor.execute("SELECT * FROM TRENDS_NNP")
rows = cursor.fetchall()
api_key = 'AIzaSyD-K6erCyq2PQZc_yPf1a_PcRogjhbtW2A'
service_url = 'https://www.googleapis.com/freebase/v1/search'
newdata=''
def freebas(query1,data):
    print query1
    if data ==[]:
        new = query1.rsplit(" ",1)[0]
        print "inside 20 "+str(new)
        params = {
        'query': new,
        'key': api_key
                 }
        url = service_url + '?' + urllib.urlencode(params)
        #requesting1 = "https://www.googleapis.com/freebase/v1/search?%s=Python&indent=true&key=AIzaSyA__H2oL6VqJvXX8pHTtIGLJnCSfg1Tf68"%(new)
        ndata = requests.get(url)
        print "inside 23 "+str(ndata)        
        status = ndata.status_code
        if status == 200:
            print "inside 25 "+str(status)
            newdata = json.loads(ndata.content)['result']
            print "inside 27 "+str(newdata)
            data = newdata
            query =new.rsplit(" ",1)[0]
            return freebas(query,data)
        else:
            if query1 == new:
                exit
            else:
                query =new.rsplit(" ",1)[0]
                return freebas(query,data)
            
    else:
        print data
        exit

for i in range(len(rows)):
    row = rows[i][1]
    print row
    data=[]
    query = row.lstrip()#.replace(" ","+")
    print query
    freebas(query,data)
    #requesting = "https://www.googleapis.com/freebase/v1/search?%s=Python&indent=true"%(query)
    #print requesting    
    #rdata = requests.get(requesting)
    #print rdata.status_code
    #print rdata.headers
    #print rdata.content
    #status = rdata.status_code
    #data = json.loads(rdata.content)['result']
    #print status
    #print data    
#Costa+2-0+Full+CHEWHU+31+COYI+CFC+62+Terry+Chelsea
