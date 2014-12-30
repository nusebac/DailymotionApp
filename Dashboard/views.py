from django.shortcuts import render
from django.template import Context
import twitter
import MySQLdb
import random
import urllib
# Create your views here.

trend_name=[]
tech_id=[]
trend_desc=[]
trend_lang=[]
trend_topic=[]
trend_source=[]
trend_external=[]
trend_related=[]
trend_region=[]
trend_age=[]
trend_temporality=[]
trend_score=[]
trend_upid = []
trend_update = []
trend_create=[]
trend_date=[]
trend_sex=[]
test_today=[]
test_next=[]
test_two=[]
test_three=[]

conn = MySQLdb.connect(host = "localhost",user = "NUSISS",passwd = "password",db = "DAILYMOTIONAPP")
cursor = conn.cursor()
cursor.execute("SELECT * FROM trends_all")
rows = cursor.fetchall()

def home(request):
    for data in rows:
        tech_id.append(data[0])
        trend_name.append(data[1])
        trend_desc.append(data[2])
        trend_lang.append(data[3])
        trend_date.append(data[4])
        trend_create.append(data[5])
        trend_update.append(data[6])
        trend_upid.append(data[7])
        trend_score.append(data[8])
        trend_temporality.append(data[9])
        trend_sex.append(data[10])
        trend_age.append(data[11])
        trend_region.append(data[12])
        trend_related.append(data[13])
        trend_external.append(data[14])
        trend_source.append(data[15])
        trend_topic.append(data[16])
    cursor.execute("SELECT * FROM `trends_all` WHERE DATE(`Created_DATE`) = CURDATE()")
    today = cursor.fetchall()
    for today_date in today:
        test_today.append(today_date[1])
    cursor.execute("SELECT * FROM `trends_all` WHERE DATE(`Created_DATE`) = DATE_ADD(CURDATE(),INTERVAL -1 DAY)")
    one_day = cursor.fetchall()
    for next_date in one_day:
        test_next.append(next_date[1])
    cursor.execute("SELECT * FROM `trends_all` WHERE DATE(`Created_DATE`) = DATE_ADD(CURDATE(),INTERVAL -2 DAY)")
    two_day = cursor.fetchall()
    for two_date in two_day:
        test_two.append(two_date[1])

    cursor.execute("SELECT * FROM `trends_all` WHERE DATE(`Created_DATE`) = DATE_ADD(CURDATE(),INTERVAL -3 DAY)")
    three_day = cursor.fetchall()
    for three_date in three_day:
        test_three.append(three_date[1])

    template = "index.html"
    test = random.sample(test_today, 10)
    test1 = random.sample(test_next, 10)
    test2 = random.sample(test_two, 10)
    #test3 = random.sample(test_three, 10)
    cursor.execute("SELECT * FROM trends_all WHERE Trend_Name=%s",(test[0]))
    new = cursor.fetchone()
    #content = {trend_name}
    content = Context({"Data": new,'Tech_ID': tech_id,'trends_today': test,'trends_next': test1,'trends_two': test2,'trends_three': test_three, "trend_desc":trend_desc,"trend_lang": trend_lang,"Created_Date": trend_create,"Updated_Date": trend_update,"trend_score": trend_score,"trend_temporality": trend_temporality,"trend_Sex": trend_sex,"trend_age": trend_age,"trend_region": trend_region,"trend_related": trend_related,"trend_external": trend_external,"trend_source": trend_source,"trend_topic": trend_topic})
    return render(request,template,content)




def common(request):
    for data in rows:
        tech_id.append(data[0])
        trend_name.append(data[1])
        trend_desc.append(data[2])
        trend_lang.append(data[3])
        trend_date.append(data[4])
        trend_create.append(data[5])
        trend_update.append(data[6])
        trend_upid.append(data[7])
        trend_score.append(data[8])
        trend_temporality.append(data[9])
        trend_sex.append(data[10])
        trend_age.append(data[11])
        trend_region.append(data[12])
        trend_related.append(data[13])
        trend_external.append(data[14])
        trend_source.append(data[15])
        trend_topic.append(data[16])
    content = Context({"Data": rows,'Tech_ID': tech_id,'trend_name': trend_name, "trend_desc":trend_desc,"trend_lang": trend_lang,"Created_Date": trend_create,"Updated_Date": trend_update,"trend_score": trend_score,"trend_temporality": trend_temporality,"trend_Sex": trend_sex,"trend_age": trend_age,"trend_region": trend_region,"trend_related": trend_related,"trend_external": trend_external,"trend_source": trend_source,"trend_topic": trend_topic})
    template = "common.html"
    return render(request,template,content)

def query(request, value):
    content = Context({"Data": value})
    template = "index.html"
    return render(request, template, content)

conn.close