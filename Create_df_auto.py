import requests
import sys
from bs4 import BeautifulSoup
import lxml
import urllib.request
import codecs
import pandas as pd

name = []
param = []
km = []
year = []
price = []
param_1 = []
param_2 = []
param_3 = []
param_4 = []
param_5 = []
n = 0

def Data_Frame_of_cars ():
    """
    Functhion for parsing URL https://auto.ru/sankt-peterburg/cars/all/
    """
    #Parsing URL
    for i in range (1,50):
        url = "https://auto.ru/sankt-peterburg/cars/all/?page={}".format(i)
        f = urllib.request.urlopen(url).read()
        soup = BeautifulSoup (f)

        req = soup.find_all("a", {"class":"Link ListingItemTitle-module__link"})

        for i in req:
            name.append(i.get_text('href', {"target=":"_blank"}))
        
        
        req = soup.find_all("div", {"class":"ListingItemTechSummaryDesktop__cell"})


        for i in req:
            param.append(i.get_text('div', {"class=":"ListingItemTechSummaryDesktop__cell"}))
        

        req = soup.find_all("div", {"class":"ListingItemPrice-module__content"})

        for i in req:
            price.append(i.get_text('div', {"class=":"ListingItemPrice-module__content"}))
        
        
        req = soup.find_all("div", {"class":"ListingItem-module__year"})

        for i in req:
            year.append(i.get_text('div', {"class":"ListingItem-module__year"}))
        
        req = soup.find_all("div", {"class":"ListingItem-module__kmAge"})

        for i in req:
            km.append(i.get_text('div', {"class":"ListingItem-module__kmAge"}))
        
        
        for i in param:
            if i.find ('опций') != -1 or i.find ('опция') != -1 or i.find ('опции') != -1:
                param.remove (i)
                
     #Create param           
    for i in range (0, len (param), 5):
        param_1.append (param [i])
        param_2.append (param [i-1])
        param_3.append (param [i-2])
        param_4.append (param [i-3])
        param_5.append (param [i-4])
    for i in price:
        if i.find ('до') != -1:
            price.remove (i)

     #Find and kill missing value   
    while len (price) != len (name):
        price.append ('1 000 000 ₽')

    
    #Create DataFrame whis params, name of cars e.t.c
    df = pd.DataFrame ({'Name':name,
                    'Km':km,
                   'Param_1':param_1,
                    'Param_2':param_2,
                    'Param_3':param_3,
                    'Param_4':param_4,
                    'Param_5':param_5,
                   'Year':year,
                    'Price': price})
    
    df.to_csv("output.csv")
    return df