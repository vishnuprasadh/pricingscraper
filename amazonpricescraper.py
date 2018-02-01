#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 28 17:23:57 2018

@author: vishnuhari
"""


from bs4 import BeautifulSoup
from stem import Signal
from stem.control import Controller
import urllib3
import time

#Crawler which opens up with proxy
#
#
# Leverage settings @http://www.andrewwatters.com/privoxy/
class ConnectionFactory:
        
    user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
    header = {'user-agent':user_agent}
    
    numberofIps = 10
    secondsofdelay = 3
    #Holders
    defaultIP = "0.0.0.0"
    newIP = "0.0.0.0"
    oldIP="0.0.0.0"
    
    def createConnection(self):
        with Controller.from_port(port=9051) as controller:
            controller.authenticate(password = "dhd8adkeiuLDKGSU937")
            if controller.is_newnym_available():
                controller.signal(Signal.NEWNYM)
                print("NEWNYM called")
            controller.close()
            
    def createnewIP(self):
        #self.setdefaultproxy()
        if self.newIP == self.defaultIP:
            self.createConnection()
            self.newIP = self.openurl('http://icanhazip.com/')
            print("NewIP in base if set as {}".format(self.newIP))
            print(self.newIP)
        else:
            self.oldIP = self.newIP
            self.createConnection()
            self.newIP = self.openurl('http://icanhazip.com/')
            print("NewIP in else set as {}".format(self.newIP))
            print(self.newIP)
            
        waittime = 0
        while (self.oldIP == self.newIP):
            time.sleep(self.secondsofdelay)
            waittime+=self.secondsofdelay
            print("Waiting for {} sec for new IP".format(waittime))
            self.newIP = self.openurl('http://icanhazip.com/')
    
    def openurl(self,url):
        http = urllib3.PoolManager()
        proxy = urllib3.ProxyManager("http://127.0.0.1:8118",timeout=20)
        req = proxy.request(method='GET',url = url,headers=self.header)
        ip = req.data
        req.release_conn()
        return ip
    

class ParseFactory():
    
    def parseHtml(self,html):
        items = list()
        bs = BeautifulSoup(html,'html.parser')
        for rootelement in bs.find('ul',attrs={'id':'s-results-list-atf'}):
            for ref in rootelement.find('a'):
                items.append(item(ref['alt'], ref.parent['href']))
        bs.clear(decompose=True)
        return items


class item():
    name = ""
    url =""
    def __init__(self,name,url):
        self.name = name
        self.url = url
        

if __name__ == '__main__':
    connect = ConnectionFactory()
    parser = ParseFactory()
    eans = ['8901030373930','8904004400779']
    
    for i in range(0 , len(eans)):
        connect.createnewIP()
        url = 'https://www.amazon.in/s/field-keywords={0}'.format(eans[i])
        resp = connect.openurl(url)
        items = parser.parseHtml(resp)
        for item in items:
            print(item.name + " : " + item.url)
            
         
        