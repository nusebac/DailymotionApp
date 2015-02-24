# -*- coding: utf-8 -*-
"""
Created on Tue Jan 13 13:28:57 2015

@author: NUS-ISS
"""

import MySQLdb
import datetime

conn = MySQLdb.connect("localhost","NUSISS","password","dailymotionapp")
cur = conn.cursor()

cur.execute("SELECT * FROM trends_all")
rows = cur.fetchall()

for row in rows:
    if not row[6]:
        if row[5].date() == datetime.date.today():
            print "New"
            new = "New"
            cur.execute("UPDATE TRENDS_ALL SET Trend_Temporality =%s WHERE Trend_Name =%s LIMIT 1 ",(new,row[2]))
            conn.commit()
        else:
            print "New Short Term"
            newshort = "Short Term"
            cur.execute("UPDATE TRENDS_ALL SET Trend_Temporality =%s WHERE Trend_Name =%s LIMIT 1 ",(newshort,row[2]))
            conn.commit()
    else:
        diff= ((row[6].date()-row[5].date()).days)
        print row[6]
        print row[5]
        print diff
        if diff == 1:
            print "Mid Term"
            mid ="Mid Term"
            cur.execute("UPDATE TRENDS_ALL SET Trend_Temporality =%s WHERE Trend_Name =%s LIMIT 1 ",(mid,row[2]))
            conn.commit()
        elif diff > 1:
            print "Long Term"
            lon ="Long Term"
            cur.execute("UPDATE TRENDS_ALL SET Trend_Temporality =%s WHERE Trend_Name =%s LIMIT 1 ",(lon,row[2]))
            conn.commit()
        else:
            print "Short Term"
            short = "Short Term"
            cur.execute("UPDATE TRENDS_ALL SET Trend_Temporality =%s WHERE Trend_Name =%s LIMIT 1 ",(short,row[2]))
            conn.commit()            
cur.close
