from NewsAggregator import NewsAggregator
from NewsArticle import NewsArticle
from XMLparser import *
from nltk.corpus import stopwords
from multiprocessing import Pool, Process, Value, Lock
import multiprocessing
import signal
import sys,os
from os import listdir
from os.path import isfile, join
from time import sleep
from ProgressBar import ProgressBar
from ProgressBar import SupportBar


#some Countries
countries = ["Greece"]

#set 50% similarity
aggr = NewsAggregator(0.50)

#Read all files from folder
xmlfiles = [ f for f in listdir("filesXml") if isfile(join("filesXml",f)) ]
progressBar = ProgressBar(int(len(xmlfiles)))
supportBar = SupportBar()

#create file for results
results = open('results.txt', 'w+')
debug = open('debug.txt', 'w+')

id = -1
for filename in xmlfiles:
    larct = parse("filesXml/" + filename)
    sys.stdout.write("(" + str(len(larct)) + "/" )
    sys.stdout.flush()
    for arcticle in larct:
        id += 1
        try:
            newarticle = NewsArticle(id, arcticle[0], arcticle[1], arcticle[2], arcticle[3], arcticle[4], countries)
            newarticle.extract_metadata()

            aggr.add_article(newarticle)
            
            #Update StatusBar
            supportBar.increase()
            size = len(str(supportBar.get()))
            spaces = ' ' * (4 - size)
            sys.stdout.write("{0}){1}\b\b\b\b\b".format(supportBar.get(), spaces))
            sys.stdout.flush()
            
        except KeyboardInterrupt:
            print "\nProgram Closed Successfully!"
            sys.exit(1)
        except Exception:
            print "\nException occurred!"
    supportBar.init()
    progressBar.update()
    
    #Write to Debug File
    debug.write(filename + "\n######################## Done.\n")
    for topic in aggr.topics:
        if len(aggr.topics[topic]) > 1:
            debug.write("---------------------------------------------------------\n")
            for idx in aggr.topics[topic]:
                debug.write(aggr.articles[idx].url + "\n")
            debug.write("---------------------------------------------------------\n")
            debug.flush()
    

#print "All filenames Completed."

for topic in aggr.topics:
    if len(aggr.topics[topic]) > 1:
        results.write("---------------------------------------------------------\n")
        results.write("MATCH FOUND\n")
        for id in aggr.topics[topic]:
            results.write(aggr.articles[id].url + "\n")
        results.write("---------------------------------------------------------\n")
        results.flush()





    
    
    
