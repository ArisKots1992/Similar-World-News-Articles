from NewsAggregator import NewsAggregator
from NewsArticle import NewsArticle
from XMLparser import *
from nltk.corpus import stopwords
from multiprocessing import Pool, Process, Value, Lock
import multiprocessing
import signal
import sys,os
from time import sleep

#Handle CTR+C
#def signal_handler(signal, frame):
#    print('You pressed Ctrl+C!')
#    sys.exit(0)
#signal.signal(signal.SIGINT, signal_handler)


#each Article has a unique local_id
id = Value('i',0)
lock = Lock()

#some Countries
countries = ["Greece"]

def parallel_arct(arg):
    arcticle = arg
    local_id = 0
    with lock:
        local_id = id.value
        id.value += 1
    newarticle = NewsArticle(local_id, arcticle[0], arcticle[1], arcticle[2], arcticle[3], arcticle[4], countries)
    newarticle.extract_metadata()
    return newarticle
    
    
#set 40% similarity
aggr = NewsAggregator(0.40)

#Number of Pools
proc_pool = Pool(processes = 2*multiprocessing.cpu_count())


xmlfiles = ["cbsnews.xml", "Global News.xml", "chathamdailynews.xml", "Sky-News.xml", "npr.xml",
            "whittierdailynews.xml", "dailynews.xml", "galvestondailynews.xml", "cbc.xml", "metro.xml", "Latimes.xml",
            "thestar.xml", "Huffingtonpost.xml", "express.xml", "rte.xml", "nwfdailynews.xml", "irishtimes.xml",
            "zeenews-india.xml", "scrippsobfeeds.xml", "Breaking News.xml", "abcnews.xml", "Independent.xml",
            "Yahoo.xml", "Telegraph.xml", "FOX News.xml", "nbcnews.xml", "news24.xml", "Reuters.xml", "Google.xml",
            "caribbeannewsnow.xml", "The Guardian.xml", "BBC.xml", "CNN.xml", "dailymail.xml", "sciencedaily.xml",
            "tvnz.xml"]




for filename in xmlfiles:
    larct = parse("filesXml/" + filename)
    #for arcticle in larct:
        #newarticle = NewsArticle(id, arcticle[0], arcticle[1], arcticle[2], arcticle[3], arcticle[4], countries)
        #newarticle.extract_metadata()
        
    try:
        newsarticles = proc_pool.map_async(parallel_arct, larct).get(9999999999)
               
        for newarticle in newsarticles:
            aggr.add_article(newarticle)
		    		
        print filename + " Done."
        print aggr.topics
        for topic in aggr.topics:
            if len(aggr.topics[topic]) > 1:
                print "---------------------------------------------------------"
                for id in aggr.topics[topic]:
                    print aggr.articles[id].url
                print "---------------------------------------------------------"
    except KeyboardInterrupt:
        proc_pool.terminate()
        print "Program Closed Successfully!"
        sys.exit(1)
    except Exception:
        print "Exception occurred!"

#    newsarticles = proc_pool.map(parallel_arct, larct)
#    
#    for newarticle in newsarticles:
#        aggr.add_article(newarticle)
#        
#    print filename + " done"
#    print aggr.topics
#    for topic in aggr.topics:
#        if len(aggr.topics[topic]) > 1:
#            print "---------------------------------------------------------"
#            print "MATCH FOUND"
#            for id in aggr.topics[topic]:
#                print aggr.articles[id].url
#            print "---------------------------------------------------------"

print "All filenames Completed."

for topic in aggr.topics:
    if len(aggr.topics[topic]) > 1:
        print "###########################################################"
        print "MATCH FOUND"
        for id in aggr.topics[topic]:
            print aggr.articles[id].url
        print "###########################################################"
        





    
    
    
