import urllib2
import urllib
from bs4 import BeautifulSoup
import threading
import Queue

class getData(threading.Thread):
    queue = Queue.Queue()
    def run(self):
        headers = {"Content-type": "application/x-www-form-urlencoded","Accept":"text/plain"}
        # Send HTTP POST request
        request = urllib2.Request(self.url,self.params,headers)
        response = urllib2.urlopen(request)
        html=response.read()
        soup = BeautifulSoup(html)
        if self.enableMoreDetails:
            ""
            #add code to featch from the more details button
        else:
            if soup.find_all(id="ctl00_ContentPlaceHolder1_GridView1")!=[]:
                html=soup.find_all(id="ctl00_ContentPlaceHolder1_GridView1")[0]
                self.queue.put({html.find_all("th")[i].text:html.find_all("td")[i].text for i in xrange(len(html.find_all("th")))})

    def __init__(self,url,params,jobsData,enableMoreDetails=False):
        self.queue=jobsData
        threading.Thread.__init__(self)
        self.url=url
        self.params=params
        self.enableMoreDetails=enableMoreDetails

