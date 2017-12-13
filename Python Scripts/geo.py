import requests
import json
import os
import pandas as pd
from queue import Queue
from threading import Thread
from time import time
import numpy as np


class Geocoding:
    def __init__(self, input_file, output_file,start,end):

        os.chdir('/home/manobhav/PycharmProjects/FirCrawler/Dataset3/')
        self.start=start
        self.end=end
        self.frame = pd.read_csv(input_file)
        self.frame = self.frame.replace(np.nan, '', regex=True)
        # self.frame.head() #Testing
        self.baseurl = "https://maps.googleapis.com/maps/api/geocode/json?"
        self.key = "AIzaSyBjS9_-orNS7CrEdNzJLLV-mrGsNsqVasQ"
        self.q = Queue()
        self.results = []
        self.outputfile = output_file
        if (not os.path.exists(self.outputfile)):
            # df=pandas.DataFrame(columns=["acts","address","datefrom","dateto","day","district","filename","link","pahar","psdate","pstation","pstime","section","timefrom","timeto",])
            col=[]
            col.extend(self.frame.columns)
            col.extend(["Formatted_address","Lat","Long"])
            df = pd.DataFrame(columns=col)

            df.to_csv(self.outputfile, index=False)

        self.startThreads()

    def getCityNames(self):
        #self.cities = self.frame.City[self.frame.City.isnull() == False].unique().tolist()
        for c in self.frame.iloc[self.start:self.end].address.unique():
            if c !="" and "KNOWN" not in c:
                self.q.put(c)

    def getLongLat(self, i):
        while True:
            print('thread {} running'.format(i))
            resultdict = {}
            resultdict['address'] = self.q.get()
            payload = {'address': resultdict['address'], 'key': self.key}
            jsonstring = requests.get(self.baseurl, payload).text

            jsondict = json.loads(jsonstring)

            if jsondict['status'] == 'OK':
                resultdict['Lat'] = jsondict['results'][0]['geometry']['location']['lat']
                resultdict['Long'] = jsondict['results'][0]['geometry']['location']['lng']
                resultdict['Formatted_address']=jsondict['results'][0]['formatted_address']
                # for l in jsondict['results'][0]['address_components']:
                #     if l['types'][0] == "administrative_area_level_1":
                #         resultdict['State'] = l['long_name']
            self.results.append(resultdict)
            print(resultdict)
            self.q.task_done()

    def startThreads(self):
        ts = time()
        for i in range(4):
            t1 = Thread(target=self.getLongLat, args=(i,))
            t1.setDaemon(True)
            t1.start()

        self.getCityNames()
        self.q.join()
        print("the process took {} seconds".format(ts - time()))
        self.update_Data()

    def update_Data(self):

        res = pd.DataFrame(self.results)
        updatedframe = pd.merge(self.frame.iloc[self.start:self.end], res, on='address', how='left', sort=False)
        updatedframe.to_csv(self.outputfile, mode='a',header=False,index=False)


geo = Geocoding('charged_address_time.csv', 'charged_address_time_lat_long.csv.csv',2000,2100)
