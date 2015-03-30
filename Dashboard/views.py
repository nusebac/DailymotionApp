from django.shortcuts import render
from django.template import Context
import twitter
import MySQLdb
import random
import urllib
# Create your views here.
test_today=[]
test_next=[]
test_two=[]
test_three=[]

conn = MySQLdb.connect(host = "localhost",user = "NUSISS",passwd = "password",db = "DAILYMOTIONAPP")
cursor = conn.cursor()
cursor.execute("SELECT * FROM trends_all")
rows = cursor.fetchall()
cursor.execute("SELECT * FROM trends_same")
similarity = cursor.fetchall()

def home(request):
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
    #test2 = random.sample(test_two, 10)
    test3 = random.sample(test_three, 10)
    cursor.execute("SELECT * FROM trends_all WHERE Trend_Name=%s",(test[0]))
    new = cursor.fetchone()
    cursor.execute("SELECT * FROM trends_similar WHERE TECHNICAL_ID=%s",(new[0]))
    simil = cursor.fetchall()
    #content = {trend_name}
    content = Context({"Data": new,"Similar": simil,'trends_today': test,'trends_next': test1,'trends_two': test3,'trends_three': test3})
    return render(request,template,content)

def common(request):
    cursor.execute("SELECT * FROM trends_all")
    similarity = cursor.fetchall()
    content = Context({"Data": similarity})
    template = "common.html"
    return render(request,template,content)

def news(request):
    cursor.execute("SELECT * FROM trends_all WHERE trend_topic = 'NewsPol'")
    similarity = cursor.fetchall()
    content = Context({"Data": similarity})
    template = "News.html"
    return render(request,template,content)

def sports(request):
    cursor.execute("SELECT * FROM trends_all WHERE trend_topic = 'Sports'")
    similarity = cursor.fetchall()
    content = Context({"Data": similarity})
    template = "Sports.html"
    return render(request,template,content)

def movies(request):
    cursor.execute("SELECT * FROM trends_all WHERE trend_topic = 'Movies'")
    similarity = cursor.fetchall()
    content = Context({"Data": similarity})
    template = "Movies.html"
    return render(request,template,content)

def celeb(request):
    cursor.execute("SELECT * FROM trends_all WHERE trend_topic = 'CELEB'")
    similarity = cursor.fetchall()
    content = Context({"Data": similarity})
    template = "Celeb.html"
    return render(request,template,content)

def comedy(request):
    cursor.execute("SELECT * FROM trends_all WHERE trend_topic = 'TVCOM'")
    similarity = cursor.fetchall()
    content = Context({"Data": similarity})
    template = "Comedy.html"
    return render(request,template,content)

def charts(request):
    content={}
    template = "charts.html"
    return render(request,template,content)

def France(request):
    conn = MySQLdb.connect(host = "localhost",user = "NUSISS",passwd = "password",db = "DAILYMOTIONAPP")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM trends_all WHERE Trend_Region = 'France'")
    similarity = cursor.fetchall()
    content = Context({"Data": similarity})
    template = "France.html"
    return render(request,template,content)


def query(request, value):
    content = Context({"Data": value})
    template = "index.html"
    return render(request, template, content)

conn.close