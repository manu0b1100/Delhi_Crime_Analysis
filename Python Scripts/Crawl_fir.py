import requests
import os



for dir,subdirlist,filelist in os.walk('Firs'):
    print(dir)
    if(len(filelist)>0):
        count=0
        f=open(dir+'/links.txt','r')
        path=""
        for line in f.readlines():
            path=line+"00000"
            count+=1
        f.close()
        print("test"+path)
        if path == "--eof--00000":
            continue

        f3=open(dir+'/links.txt','a')
        lis=path.split('=')
        if len(lis)>0:
            lowerval=int(lis[1][:-5])+1
            c=0
            while(c<5 and count<30):
                count+=1
                url=('=').join([lis[0],str(lowerval)])
                print(url)
                response = requests.get(url)
                print(response)
                lowerval += 1
                print(response.content.__len__())
                if response.content.__len__()<20:
                    c+=1
                    continue
                print(lowerval)
                with open(dir+"/" + str(lowerval-1) + ".pdf", 'wb') as f2:
                    f2.write(response.content)
                f3.write(url+"\n")
                c=0
            f3.write("--eof--")