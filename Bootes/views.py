from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
import pandas as pd
import datetime
import cryptocompare
import time
import datetime
import numpy as np
#from coinmarketcap import Market
#coinmarketcap=Market()

# Create your views here.
def DataSearch(request):
    template = loader.get_template('Bootes/BootesHome.html')

    #Consume cryptocompare API for desired cryptocurrency data
    def historical_data(symbol, timediv, comparison_symbol='USD', all_data=True, limit=1, aggregate=1, exchange='', ):
        if timediv == 'minute':
            url='https://min-api.cryptocompare.com/data/histominute?fsym={}&tsym={}&limit={}&aggregate={}'\
            .format(symbol.upper(), comparison_symbol.upper(), limit, aggregate, exchange)
        if timediv == 'day':
            url='https://min-api.cryptocompare.com/data/histoday?fsym={}&tsym={}&limit={}&aggregate={}'\
            .format(symbol.upper(), comparison_symbol.upper(), limit, aggregate, exchange)
        if not exchange:
            exchange = 'CCCAGG'
            url+= '&e={}'.format(exchange)
        if all_data:
            url+='&allData=True'
        print(url)
        page=requests.get(url)
        data=page.json()['Data']
        df=pd.DataFrame(data)
        if df.empty == False:
            df['timestamp']=[datetime.datetime.fromtimestamp(d) for d in df.time]
            print('dataframe filled')
        elif df.empty == True:
            print('empty dataframe')
            df=""
        return df

    #Obtain today's major cryptocurrency data and format appropriately for d3 render
    Q = 'BTC', 'ETH', 'XRP'
    Q1_hist = historical_data(Q[0], 'minute').tail(1440)
    Q2_hist = historical_data(Q[1], 'minute').tail(1440)
    Q3_hist = historical_data(Q[2], 'minute').tail(1440)

    #adjust timedata offset for tz:America/Toronto
    Q1_hist['timestamp'] += datetime.timedelta(hours=5)
    Q2_hist['timestamp'] += datetime.timedelta(hours=5)
    Q3_hist['timestamp'] += datetime.timedelta(hours=5)

    #Get current price for major cryptocurrencies
    Q1_now = cryptocompare.get_price(Q[0], 'USD')[Q[0]]['USD']
    Q2_now = cryptocompare.get_price(Q[1], 'USD')[Q[1]]['USD']
    Q3_now = cryptocompare.get_price(Q[2], 'USD')[Q[2]]['USD']
    print(type(Q1_now))

    #Format data for d3.js
    Q1_hist = pd.DataFrame.to_json(Q1_hist[['timestamp', 'close']].rename(index=str, columns={'timestamp':'x', 'close':'y'}), orient='records')
    Q2_hist = pd.DataFrame.to_json(Q2_hist[['timestamp', 'close']].rename(index=str, columns={'timestamp':'x', 'close':'y'}), orient='records')
    Q3_hist = pd.DataFrame.to_json(Q3_hist[['timestamp', 'close']].rename(index=str, columns={'timestamp':'x', 'close':'y'}), orient='records')

    #Obtain cryptocurrency data and format appropriately for d3 rendering
    if request.method == 'GET' and request.GET.get('search_box',None) != None:
        search_query = request.GET.get('search_box', None)
        TickSym=search_query.upper()
        CurrentPrice = cryptocompare.get_price(search_query.upper(), 'USD')[TickSym]['USD']
        CurrentTime = datetime.datetime.now()
        
        #Store data in time increments for tab display
        m1_hist = historical_data(search_query.upper(), 'minute').tail(43200) #1 month
        daily_hist = m1_hist.tail(1440) #1 day
        all_hist = historical_data(search_query.upper(), 'day') #all time
        m6_hist = all_hist.tail(183)#6 months
        y1_hist = all_hist.tail(365)#1 year

        #adjust cryptocompare timedata offset for tz:America/Toronto
        m1_hist['timestamp'] += datetime.timedelta(hours=5)
        daily_hist['timestamp'] += datetime.timedelta(hours=5)

        #Format data for d3.js
        m1_hist = pd.DataFrame.to_json(m1_hist[['timestamp', 'close']].rename(index=str, columns={'timestamp':'x', 'close':'y'}), orient='records')
        daily_hist = pd.DataFrame.to_json(daily_hist[['timestamp', 'close']].rename(index=str, columns={'timestamp':'x', 'close':'y'}), orient='records')
        m6_hist = pd.DataFrame.to_json(m6_hist[['timestamp', 'close']].rename(index=str, columns={'timestamp':'x', 'close':'y'}), orient='records')
        y1_hist = pd.DataFrame.to_json(y1_hist[['timestamp', 'close']].rename(index=str, columns={'timestamp':'x', 'close':'y'}), orient='records')
        all_hist = pd.DataFrame.to_json(all_hist[['timestamp', 'close']].rename(index=str, columns={'timestamp':'x', 'close':'y'}), orient='records')
        
        return HttpResponse(template.render({"Q1" : Q[0], "Q2" : Q[1], "Q3" : Q[2], "Q1_now" : Q1_now, "Q2_now" : Q2_now, "Q3_now" : Q3_now, "Q1_hist" : Q1_hist, "Q2_hist" : Q2_hist, "Q3_hist" : Q3_hist, "CurrentPrice" : CurrentPrice, "CurrentTime" : CurrentTime, "daily_hist" : daily_hist, "m1_hist" : m1_hist, "m6_hist" : m6_hist, "y1_hist" : y1_hist, "all_hist" : all_hist, "TickSym" : TickSym}))
    else:
        search_query = "You haven't entered anything."
        return HttpResponse(template.render())
