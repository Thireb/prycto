#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from pprint import pprint
from webbrowser import get
from cryptocmd import CmcScraper
import json
import Scrap as sc
from Scrap import semantic_token as st
from datetime import datetime as dt
# import plotly.graph_objects as go

#opt = json.loads(open('/home/kenway/config.json','r').read())
opt = json.loads(open('./config.json','r').read())
loc = opt['dir_loc']

def current_time():
    now_time = dt.now()
    time_now = now_time.strftime("%H:%M:%S")
    return(str(time_now))

def log(i,o):
    log_string= "[{}] {}".format(current_time(),i)
    log_string_x=str()
    if (o == 0):
        log_string_x = "[\N{Heavy Multiplication X}] {}".format(log_string)
    elif (o == 1):
        log_string_x = "[\N{check mark}] {}".format(log_string)
    else:
        log_string_x = "[i] {}".format(log_string)
    print(log_string_x)
    if(opt['log_to_file']):
        file_log = open(opt['dir_loc']+"log.txt", "a")
        file_log.write(log_string_x+"\n")
        file_log.close()

def daysago(u):
    todaydate = dt.now().date()
    day = dt.fromordinal(dt.toordinal(todaydate) - u).date()
    return('{:%d-%m-%Y}'.format(day))

def get_reddit_posts(x):
    return(sc.raw_data(sc.get_subreddit_info(x)))

def get_analysis(x):
    return(st.semantic_token(get_reddit_posts(x)))

def crypto_plot_X(x, y, z):
    scraper = CmcScraper(x, y, z)
    jdj = scraper.get_data('json')
    li = list()
    li = json.loads(jdj)
    return(li)

def jout(l,m):
    with open(loc+"output-"+m+".json", "w") as outfile:
        outfile.write(json.dumps(l, indent=4, sort_keys=False))

def charts_return(x,y):
    map_out = dict()
    for ola in x:
        if(y==True):
            cmap = crypto_plot_X(ola, daysago(360), daysago(0))
            cmap.reverse()
            mapval = dict()
            for i in cmap:
                mapval[i["Date"]] = {"high": i["High"], "low": i["Low"], "open": i["Open"], "close": i["Close"]}
            map_out[ola] = mapval
        elif(y==False):
            oldx = json.loads(open(loc+'output-data.json','r').read())
            old = oldx[ola]
            try:
                log('Trying to Get Pervious day',3)
                cmap = crypto_plot_X(ola, daysago(1), daysago(0))
            except:
                log('Failed Previous day,',0)
                log('Trying to Get 2 days ago')
                cmap = crypto_plot_X(ola, daysago(2), daysago(0))
            cmap.reverse()
            log('Data Got for '+ola+', writing to JSON.',1)
            old[cmap[0]["Date"]] = {"high": cmap[0]["High"], "low": cmap[0]["Low"], "open": cmap[0]["Open"], "close": cmap[0]["Close"]}
            map_out[ola] = old
    return map_out

def analysis_return(x):
    map_out = dict()
    for data in x:
        xo = get_analysis(data)
        map_out[data] = xo
    return map_out

data_charts = charts_return(opt['symbol'],opt['cache_flag'])
data_analysis = analysis_return(opt['symbol'])

jout(data_charts,'data')
jout(data_analysis, 'analysis')

if(opt['cache_flag']==True):
    with open(loc+'config.json','r') as f:
        x = json.loads(f.read())
        x['cache_flag']=False
    with open(loc+'config.json','w') as lx:
        lx.write(json.dumps(x, indent=4, sort_keys=False))






 ####_-------------------#####   Test Code, Out of reach
# cmap = crypto_plot('ETH', daysago(20), daysago(0))
# for vals in l:
#         m[vals["Date"]] = {"high": vals["High"], "low": vals["Low"], "open": vals["Open"], "close": vals["Close"]}

# json_output = dict()


# print(json_output[daysago(1)]["high"])



# with open("output.json", "w") as outfile:
#     json.dump(json_output, outfile)

## You might need this later to send a graph but thats a might

# dates = []
# open_data = []
# high_data = []
# low_data = []
# close_data = []

# for candle in lolmap:
#     dates.append(candle['Date'])
#     open_data.append(candle['Open'])
#     high_data.append(candle['High'])
#     low_data.append(candle['Low'])
#     close_data.append(candle['Close'])

# fig = go.Figure(data=[go.Candlestick(x=dates,open=open_data, high=high_data,low=low_data, close=close_data)])
# fig.show()
