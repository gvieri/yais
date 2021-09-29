#
# (c) Vieri Giovambattista 2021 all rights reserved 
# License: AGPL 3.0
import os
import shutil

rootdir="./data/"

origdir  =rootdir+"original/"
traindir =rootdir+"train/"
valdir   =rootdir+"validation/"


os.makedirs(traindir,exist_ok=True)
os.makedirs(valdir,exist_ok=True)

selector=4

def processfiles(source,train,val):  ### this f() move files from source n val and train dirs.
    c=0 
    print ("source %s" % source)
    print ("train  %s" % train)
    print ("val    %s" % val)
    for f in os.listdir(source):
        if os.path.isdir(f):
            print("why in whole world the "+f+" is a dir ? ") 
        sf=os.path.join(source,f)
        c=c+1
        if c==selector:
            c=0
            shutil.copy(sf,val)
        else: 
            shutil.copy(sf,train)

for d in os.listdir(origdir):
    if os.path.isdir(d) : 
        print (d) 
        traindircat=os.path.join(traindir,d)
        valdircat=os.path.join(valdir,d)
        origdircat=os.path.join(origdir,d)
        print(origdircat+" | "+valdircat+" | "+traindircat)
        os.makedirs(traindircat,exist_ok=True)
        os.makedirs(valdircat,exist_ok=True)
        processfiles(origdircat,traindircat,valdircat)
