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
    def days_historical_data(symbol, comparison_symbol='USD', all_data=True, limit=1, aggregate=1, exchange=''):
        url='https://min-api.cryptocompare.com/data/histominute?fsym={}&tsym={}&limit={}&aggregate={}'\
        .format(symbol.upper(), comparison_symbol.upper(), limit, aggregate, exchange)
        if not exchange:
            exchange = 'CCCAGG'
            url+= '&e={}'.format(exchange)
        if all_data:
            print('all_data is true')
            url+='&allData=True'
        print('api url is: ' + url)
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
    if request.method == 'GET' and request.GET.get('search_box',None) != None:
        search_query = request.GET.get('search_box', None)
        TickSym=search_query.upper()
        currency_data = cryptocompare.get_price(search_query.upper(), 'USD')[TickSym]['USD']
        current_time = datetime.datetime.now()
        histo_crypto = days_historical_data(search_query.upper()).tail(1440)
        histo_crypto['timestamp'] += datetime.timedelta(hours=5) #adjust cryptocompare timedata offset for tz:America/Toronto
        print(histo_crypto['close'].tail(10))
        histo_crypto = pd.DataFrame.to_json(histo_crypto[['timestamp', 'close']].rename(index=str, columns={'timestamp':'x', 'close':'y'}), orient='records')
        return HttpResponse(template.render({"currency_data" : currency_data, "current_time" : current_time, "histo_crypto" : histo_crypto, 'TickSym' : TickSym}))
    else:
        search_query = "You haven't entered anything."
        return HttpResponse(template.render())
