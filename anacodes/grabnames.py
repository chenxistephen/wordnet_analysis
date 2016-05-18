import simplejson as json
from nltk.corpus import wordnet as wn
import ana_wn as aw
import sys
import csv

def buildIndex(objs=[], imglist=[], wnnamelist=[]):
    
    
    objfile = "E:\Data\Genome\meta_data\objects.json"
    imgfile = "E:\Data\Genome\meta_data\image_data.json"

    if len(objs)==0:
        print "loading ", objfile
        objs = json.load(open(objfile))
    if len(imglist)==0:
        print "loading ", imgfile
        imglist = json.load(open(imgfile))
    if len(wnnames)==0:
        wnnamelist, wnidlist = aw.getWordNetList('clothing')
    
    objNum = len(objs)
    assert(objNum == len(imglist))
    
    vgimglist = []
    vgclslist = []
    
    for i, x in enumerate(objs):
        imgId = imglist[i]['id']
        for y in x['objects']:
            if len(y['names']) ==0:
                print "Empty string!"
                continue
            # print y['names']
            objcls = y['names'][0].encode('ascii', 'ignore')
            # print "objcls", objcls
            if (len(objcls))==0:
                continue
            if len(str(objcls).split())==0:
                continue
            if str(objcls).split()[0] == 'the':
                after = " ".join(str(objcls).split()[1:]) 
                print "Join ", objcls, " to ", after
                objcls = after
            yname = aw.unstr(y['names'][0])
            if yname in wnnamelist:
                vgimglist.append(imgId)
                vgclslist.append(y['names'][0].encode('ascii','ignore'))
                print "Image %s : %s" %(str(imgId), str(y['names'][0]))
    
    return vgimglist, vgclslist
    
def count2csv(counter, filename='genome_clothes_counter'):
    with open(filename+'.csv', 'wb') as csvfile:
        writer = csv.writer(csvfile)
        for key, count in counter.iteritems():
            clsname = key
            writer.writerow([clsname.encode('ascii','ignore'), count])
                
def list2csv(vgimglist, vgclslist, filename='genome_clothes_imglist'):
    vgclslist =[x.encode('UTF8') for x in vgclslist]
    with open(filename+'.pickle','w') as f:
        pickle.dump([vgimglist, vgclslist],f)
    with open('genome_clothes_imglist.csv', 'wb') as csvfile:
        writer = csv.writer(csvfile)
        imgNum = len(vgimglist)
        for i in range(imgNum):
            writer.writerow([vgimglist[i], vgclslist[i].encode('ascii','ignore')]) 
            

        
    