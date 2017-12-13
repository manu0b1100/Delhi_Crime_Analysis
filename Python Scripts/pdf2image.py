from PIL import Image
import pytesseract
from wand import image
import os
import pandas
#Converting first page into JPG
data=[]

info={
"address":(896,2388,3736,2500),
"acts":(376,1472,1360,1572),
"section":(1792,1480,2252,1600),
"datefrom":(2028,1716,2424,1820),
"dateto":(3092,1716,3444,1800),
"day":(700,1720,1168,1800),
"timefrom":(2028,1800,2388,1900),
"timeto":(3092,1800,3444,1900),
"pstime":(3408,1900,3724,2008),
"psdate":(2560,1900,2928,1988),
"pahar":(1100,1800,1396,1892)
}
c=0
curdir=""
curfile=""
if(not os.path.exists("my_csv.csv")):
    #df=pandas.DataFrame(columns=["acts","address","datefrom","dateto","day","district","filename","link","pahar","psdate","pstation","pstime","section","timefrom","timeto",])
    df=pandas.DataFrame(columns=["acts","address","datefrom","dateto","day","district","filename","link","pahar","psdate","pstation","pstime","section","timefrom","timeto"])

    df.to_csv("my_csv.csv",index=False)

df=pandas.read_csv("my_csv.csv")
print(df.shape[0])
count=df.shape[0]
for dir,subdirlist,filelist in os.walk('Firs'):
    print(dir)

    filelist.sort()
    if(len(filelist)>0):
        for file in filelist:
            if count != 0:
                count -= 1
                continue
            datum = {}
            datum["filename"] = file
            datum["district"] = dir.split('/')[-2]
            datum["pstation"] = dir.split('/')[-1]
            datum["link"] = "http://59.180.234.21:8080/citizen/gefirprint.htm?firRegNo=" + file[:-4]
            print(file)
            try:
                with image.Image(
                        filename=dir+"/"+file+"[0]",
                        resolution=500) as img:
                    try:
                        img.save(filename="temp.jpg")
                    except:
                        continue
            except:
                continue


            img = Image.open('temp.jpg')
            for (key, val) in info.items():
                img2 = img.crop(val)
                datum[key] = pytesseract.image_to_string(img2)
                print(pytesseract.image_to_string(img2))
            data.append(datum)
            c+=1
            print(datum)

            if c>20:
                c=0
                df1 = pandas.DataFrame(data)
                df1.to_csv('my_csv.csv', mode='a',index=False,header=False)
                data=[]

df1 = pandas.DataFrame(data)
df1.to_csv('my_csv.csv', mode='a', header=False,index=False)
print(data)