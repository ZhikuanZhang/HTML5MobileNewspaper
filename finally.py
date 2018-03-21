import pymysql
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.error import HTTPError,URLError
from tkinter import *

def getNews(firsturl,newsblock,lasturl,newsNo,paperid,newsdate):
    nyear = newsdate[0:4]
    nmonth = newsdate[4:6]
    nday = newsdate[6:]
    stringdate = nyear + "-" + nmonth + "/" + nday
    newsurl = firsturl + stringdate + "/" + lasturl
    print(newsurl)
    try:
        html = urlopen(newsurl)
    except (HTTPError,URLError) as e:
        return None
    try:
        bsObj = BeautifulSoup(html)
        title = bsObj.findAll("h1")
        links = bsObj.findAll("p")
        print(title)
    except AttributeError as e:
        return None
    i=1
    text=""

    for link in links:

        text+=str(link)
        if i==((links.__len__()-2)):
            break
        i=i+1
    l=int(text.__len__()/2)
    text=text[0:l]
    title=str(title)
    if(title.__len__()<=4):
        return 0;
    title=title.split('>')[1]
    title=title.split('<')[0]
    if(title=="图片报道" or title=="广告"):
        return 0;
    id = newsdate + "0010" + newsblock + str(newsNo)
    print(id + " " + newsdate+" "+paperid)
    pdf_lasturl = "rmrb" + nyear + nmonth + nday + "0" + newsblock + ".pdf"
    cur.execute('Insert Into news(id,date,paperid,block,title,text) values (%s,%s,%s,%s,%s,%s)',
                (id,newsdate,paperid,newsblock,title,text))
    cur.connection.commit()
    return 1;

def getPDF(firsturl,newsdate,block,lasturl,paperid):
    nyear = newsdate[0:4]
    nmonth = newsdate[4:6]
    nday = newsdate[6:]
    stringdate = nyear + "-" + nmonth + "/" + nday
    pdfurl = firsturl + stringdate + "/" + "0"+str(block) + "/" + lasturl
    print (pdfurl)
    r = requests.get(pdfurl)
    if r==None:
        return
    with open("E:\\Code\\newspaper\\pdf\\"+lasturl,"wb") as code:
        code.write(r.content)

def update(event):
    print("updating.......")
    newsdate = e2.get()
    newsblock = 1
    i=1;
    j=1;
    if e1.get() == "001":
        pdf_firsturl = "http://paper.people.com.cn/rmrb/page/"
        news_firsturl = "http://paper.people.com.cn/rmrb/html/"
    while (newsblock <= 9):
        i=1;
        j=1;
        pdf_lasturl = "rmrb" + newsdate + "0" + str(newsblock) + ".pdf"
        while (i <= 9):
            news_lasturl = "nw.D110000renmrb_" + newsdate + "_" + str(i) + "-" + "0" + str(newsblock) + ".htm"
            flag = getNews(news_firsturl, str(newsblock), news_lasturl, j, e1.get(), newsdate)
            i = i + 1
            if (flag == 0):
                continue
            j = j + 1;
        newsblock=newsblock+1
    #   getPDF(pdf_firsturl,stringdate,str(newsblock),pdf_lasturl,"001")
    print("update complete!")

def transform(event):
    print("transforming......")
    newsdate = e2.get()
    newsblock = 1
    if e1.get() == "001":
        pdf_firsturl = "http://paper.people.com.cn/rmrb/page/"
    while (newsblock <= 9):
        pdf_lasturl = "rmrb" + newsdate + "0" + str(newsblock) + ".pdf"
        getPDF(pdf_firsturl, newsdate, str(newsblock), pdf_lasturl, "001")
        newsblock = newsblock + 1
    print("transform complete!")

conn = pymysql.connect(host='127.0.0.1',user='root',
                       passwd=None,db='mysql',charset='utf8')
cur = conn.cursor()
print("database connect correct")
cur.execute("use test")
master = Tk()
master.title("UpdateSystem")
master.resizable(False, False)
Label(master, text="报刊编号:").grid(sticky=E)
Label(master, text="发行时间:").grid(sticky=E)
Label(master, text="版块编号:").grid(sticky=E)
e1 = Entry(master)
e2 = Entry(master)
e3 = Entry(master)
e1.grid(row=0, column=1)
e2.grid(row=1, column=1)
e3.grid(row=2, column=1)

photo = PhotoImage(file='newspaper.png')
label = Label(image=photo)
label.image = photo
label.grid(row=0, column=2, columnspan=2, rowspan=2, sticky=W+E+N+S, padx=5, pady=5)

button1 = Button(master, text='更新报刊')
button1.bind("<Button-1>",update)
button1.grid(row=2, column=2)

button2 = Button(master, text='转换-PDF')
button2.bind("<Button-1>",transform)
button2.grid(row=2, column=3)

mainloop()