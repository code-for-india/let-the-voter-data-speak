import os
import re
import featch
import urllib2
import urllib
from bs4 import BeautifulSoup
from mysqlConnect import mysqlConnection
import Queue

def getMetaData(url,params,id):
    headers = {"Content-type": "application/x-www-form-urlencoded","Accept":"text/plain"}
    # Send HTTP POST request
    data=[]
    request = urllib2.Request(url,params,headers)
    respose=urllib2.urlopen(request)
    soup=BeautifulSoup(respose.read())
    soup=soup.find_all(id=id)[0]
    temp1=soup.find_all("th")
    temp2=soup.find_all("td")
    return temp1,temp2