# -*- coding: utf-8 -*-
"""
Created on Wed Jan  4 01:59:02 2017

@author: frdam
"""

import csv
import requests
import datetime




class Quote(object):
  
  
  def __init__(self):
    self.symbol = ''
    self.date,self.open_,self.high,self.low,self.close,self.volume = ([] for _ in range(6))

  def append(self,dt,open_,high,low,close,volume):
    self.date.append(dt)
    self.open_.append(open_)
    self.high.append(high)
    self.low.append(low)
    self.close.append(close)
    self.volume.append(volume)
    
  
  def to_csv(self):
    return ''.join(["{0},{1},{2},{3},{4},{5},{6}\n".format(self.symbol,
              self.date[bar],self.open_[bar],self.high[bar],self.low[bar],self.close[bar],self.volume[bar]) 
              for bar in iter(range(len(self.close)))])
    
  def write_csv(self,filename):
    with open(filename, mode='wt', encoding='utf-8') as f:
      f.write(self.to_csv())
        
  def read_csv(self,filename):
    self.symbol = ''
    for line in open(filename, mode='rt', encoding='utf-8'):
      #print(line)
      symbol,ds,open_,high,low,close,volume = line.rstrip().split(',')
      self.symbol = symbol
      self.append(ds,open_,high,low,close,volume)
    return True

  def __repr__(self):
    return self.to_csv()
        

    
    
class GoogleQuote(Quote):
    
  ''' Daily quotes from Google. Date format='yyyy-mm-dd' '''
  def __init__(self,symbol,start_date,end_date=datetime.date.today().isoformat()):
    super(GoogleQuote,self).__init__()
    self.symbol = symbol.upper()
    start = datetime.date(int(start_date[0:4]),int(start_date[5:7]),int(start_date[8:10]))
    end = datetime.date(int(end_date[0:4]),int(end_date[5:7]),int(end_date[8:10]))
    url_string = "http://www.google.com/finance/historical?q={0}".format(self.symbol)
    url_string += "&startdate={0}&enddate={1}&output=csv".format(
                      start.strftime('%b %d, %Y'),end.strftime('%b %d, %Y'))
   

    # print (url_string) # check url link string
    download = requests.Session().get(url_string)
    decoded_content = download.content.decode('utf-8')
    cr = csv.reader(decoded_content.splitlines(), delimiter=',')
    csv_list = list(cr)
    """
    for row in csv_list:   # check data is retrivate correctly  
        print(row)
    """
    for row in csv_list:
       ds,open_,high,low,close,volume = row
       self.append(ds,open_,high,low,close,volume)

      
if __name__ == '__main__':
  q = GoogleQuote('aapl','2016-01-01')              # download year to date Apple data
  #print( q)                                           # print it out
  q = GoogleQuote('orcl','2016-11-01','2016-11-30') # download Oracle data for February 2011
  q.write_csv('orcl.csv')                           # save it to disk
  q = Quote()                                       # create a generic quote object
  q.read_csv('orcl.csv')                            # populate it with our previously saved data
  print (q)                                         # print it out
        