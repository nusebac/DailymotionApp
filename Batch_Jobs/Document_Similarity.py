# -*- coding: utf-8 -*-
"""
@author: HP
"""
import MySQLdb
from fuzzywuzzy import fuzz

conn = MySQLdb.connect("localhost","NUSISS","password","dailymotionapp")
cursor = conn.cursor()
cursor.execute("SELECT * FROM TRENDS_NNP")
rows = cursor.fetchall()
cursor.execute("SELECT * FROM TRENDS_SIMILAR")
nez = cursor.fetchall()
key_store =[]
key_stores=[]
none=0
for ne in nez:
    key_store.append(ne[0])
    key_stores.append(ne[1])

for i in range(len(rows)):
    if rows[i][0] not in key_store:
        print rows[i][0]
        print rows[i][1] 
        for newrow in rows:
            ratiofinal = ((fuzz.ratio(rows[i][1],newrow[1]))+(fuzz.partial_ratio(rows[i][1],newrow[1]))+(fuzz.token_sort_ratio(rows[i][1],newrow[1]))+(fuzz.token_set_ratio(rows[i][1],newrow[1])))/4
            if int(ratiofinal) >= 50 and ratiofinal < 100:
                if rows[i][0] in key_store:
                    if newrow[0] in key_stores:
                        print "Already Updated to DB"
                        break
                    else:
                        cursor.execute("INSERT INTO TRENDS_SIMILAR (TECHNICAL_ID,RELATED_TRENDS) VALUES(%s,%s)",(rows[i][0],newrow[0]))
                        conn.commit()
                        break
                else:
                    cursor.execute("INSERT INTO TRENDS_SIMILAR (TECHNICAL_ID,RELATED_TRENDS) VALUES(%s,%s)",(rows[i][0],newrow[0]))
                    conn.commit()
    else:
        print "Alredy exist : "+str(rows[i][0])
                
for i in range(len(rows)):
    if rows[i][0] not in key_store:
        cursor.execute("INSERT INTO TRENDS_SIMILAR (TECHNICAL_ID,RELATED_TRENDS) VALUES(%s,%s)",(rows[i][0],none))
        conn.commit()        
conn.close()

