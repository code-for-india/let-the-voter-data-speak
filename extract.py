import os
import re
import featch
import urllib2
import urllib
from bs4 import BeautifulSoup
from mysqlConnect import mysqlConnection
import Queue
import metaData

my=mysqlConnection()
db=my.getConnection("Electroal_list")
selectDB = db.cursor()

queue=Queue.Queue()

def removeNonAscii(s):
    return "".join(filter(lambda x: ord(x)<128, s))

def getFiles(dirPath):
    "get the list of files in the directory"
    onlyfiles = [ f for f in os.listdir(dirPath) if os.path.isfile(os.path.join(dirPath,f)) ]
    return onlyfiles

def getDir(folder):
    return [d for d in (os.path.join(folder, d1) for d1 in os.listdir(folder)) if os.path.isdir(d)]

for fPdfDir in getDir("./pdf"):
    for fpdf in getFiles(fPdfDir):
        temp=fPdfDir.split("/")
        outName="./text/"+temp[2]
        if os.path.exists(outName+"/"+fpdf[:-3]+"txt"):
            print "Exists"
        else:
            command="pdftotext "+fPdfDir+"/"+fpdf
            os.system(command)
            try:
                if not os.path.exists(outName):
                    os.makedirs(outName)
                    print outName+" created directory"
            except Exception:
                ""
            os.system("mv "+fPdfDir+"/*.txt"+" "+outName)

urlList=["http://164.100.80.163/ceo1/SearchWithEpicNo_New.aspx"]
for fTxtDir in getDir("./text"):
    for ftxt in getFiles(fTxtDir):
        f=open(fTxtDir+"/"+ftxt)
        temp=fTxtDir.split("/")
        district=temp[2]
        for EPICNo in re.findall("[A-Z]{3}[0-9]{7}",f.read()):
            for url in urlList:
                params = urllib.urlencode({'ctl00$ContentPlaceHolder1$ddlDistrict':district , 'ctl00$ContentPlaceHolder1$txtEpic':
                               EPICNo,'__EVENTTARGET':'','__EVENTARGUMENT':'','__LASTFOCUS':'','__VIEWSTATE':'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'
                               ,'ctl00$ContentPlaceHolder1$btnSearch':'Search'})
                t=featch.getData(url,params,queue,enableMoreDetails=False)
                t.setDaemon(True)
                t.start()
                try:
                    data=queue.get()
                    print (data["Rel_FirstName"],data["FirstName"],data["ACNO"],data["PartNo"],data["LastName"],data["age"],data["Rel_LastName"],data["AssemblyConstituency"],data["sex"],data["SlnNo"])
                    selectDB.execute("INSERT INTO Electroal_kar VALUES (\'%s\',\'%s\',\'%s\',%d,%d,\'%s\',%d,\'%s\',\'%s\',\'%s\',%d)" % (EPICNo,data["Rel_FirstName"],data["FirstName"],int(data["ACNO"]),int(data["PartNo"]),data["LastName"],int(data["age"]),data["Rel_LastName"],data["AssemblyConstituency"],data["sex"],int(data["SlnNo"])))
                    print "Successful"
                    db.commit()
                except Exception, e:
                    db.rollback()
                    print e
                    print "Insert Failed"

urlList=["http://ceokarnataka.kar.nic.in/ElectionFinalroll2014/Dist_List.aspx"]
stateName=["rnataka"]
for i in xrange(len(urlList)):
    url=urlList[i]
    state=stateName[i]
    head,data=metaData.getMetaData(url,None,id="ctl00_ContentPlaceHolder1_GridView1")
    for i in xrange(0,len(data),2):
        fixData=removeNonAscii(data[i+1].text)
        print("INSERT INTO DistrictInfo VALUES (\'%s\',%d,\'%s\')" % (state,int(data[i].text),fixData))
        try:
            selectDB.execute("INSERT INTO DistrictInfo VALUES (\'%s\',%d,\'%s\')" % (state,int(data[i].text),fixData))
            print "Successful"
            db.commit()
        except Exception, e:
            db.rollback()
            print e
            print "Insert Failed"