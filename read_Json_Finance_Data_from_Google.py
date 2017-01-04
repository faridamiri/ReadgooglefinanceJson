# -*- coding: utf-8 -*-
"""
Created on Tue Jan  3 23:52:43 2017

@author: frdam
"""

import urllib
import time

def GoogleFinanceAPI(symbol,exchange):
   fgurl = "http://finance.google.com/finance/info?client=ig&q="
    
     
   req = fgurl+"%s:%s"%(exchange,symbol)
   res = urllib.request.urlopen(req)
   data = res.read()
   return(data.decode('utf-8'))
  
    

while 1:
    quote = GoogleFinanceAPI("MSFT","NASDAQ")
    print (quote)
    time.sleep(30)
        