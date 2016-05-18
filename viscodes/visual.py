# Written by Stephen Xi Chen based on https://visualgenome.org/api/v0/api_beginners_tutorial.html
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import api as vg
from PIL import Image as PIL_Image
import requests
from StringIO import StringIO
import json
import csv
import os
from collections import Counter


def visualize_regions(image, regions):
    response = requests.get(image.url)
    img = PIL_Image.open(StringIO(response.content))
    plt.imshow(img)
    ax = plt.gca()
    for region in regions:
        ax.add_patch(Rectangle((region.x, region.y),
                               region.width,
                               region.height,
                               fill=False,
                               edgecolor='red',
                               linewidth=3))
        ax.text(region.x, region.y, region.phrase, style='italic', bbox={'facecolor':'white', 'alpha':0.7, 'pad':10})
    fig = plt.gcf()
    plt.tick_params(labelbottom='off', labelleft='off')
    plt.show()
    

    
    
def regions(id):
    ids = vg.GetImageIdsInRange(startIndex=id, endIndex=id)
    image_id = ids[0]
    print "We got an image with id: %d" % image_id

    # matplotlib inline

    image = vg.GetImageData(id=image_id)
    print "The url of the image is: %s" % image.url

    regions = vg.GetRegionDescriptionsOfImage(id=image_id)
    print "The first region descriptions is: %s" % regions[0].phrase
    print "It is located in a bounding box specified by x:%d, y:%d, width:%d, height:%d" % (regions[0].x, regions[0].y, regions[0].width, regions[0].height)
    fig = plt.gcf()
    fig.set_size_inches(18.5, 10.5)
    visualize_regions(image, regions[:8])
    
def visualize_objects(image, objs):
    response = requests.get(image.url)
    img = PIL_Image.open(StringIO(response.content))
    plt.imshow(img)
    ax = plt.gca()

    for obj in objs:
        objx = float(obj['x'])
        objy = float(obj['y'])
        objw = float(obj['w'])
        objh = float(obj['h'])    
        ax.add_patch(Rectangle((objx, objy),
                               objw,
                               objh,
                               fill=False,
                               edgecolor='yellow',
                               linewidth=3))
        ax.text(objx, objy, obj['names'][0], style='italic', bbox={'facecolor':'white', 'alpha':0.7, 'pad':10})
    fig = plt.gcf()
    plt.tick_params(labelbottom='off', labelleft='off')
    plt.show()

def objects(id, objs, objNum=10):
    ids = vg.GetImageIdsInRange(startIndex=id, endIndex=id)
    image_id = ids[0]
    image = vg.GetImageData(id=image_id)
    if len(objs) ==0:
        objs = json.load(open("E:\Data\Genome\meta_data\objects.json"), encoding='ascii')
    visualize_objects(image, objs[id]['objects'][:objNum])
    
def loadlist(filename='E:\\Data\\Genome\\anacodes\\genome_clothes_imglist.csv'):
    # vgimglist, vgclslist = vis.loadlist()
    with open(filename) as filein:
        reader = csv.reader(filein, skipinitialspace = True)
        vgimglist, vgclslist = zip(*reader)     
    vgimglist = list(vgimglist)
    vgclslist = list(vgclslist)
    return vgimglist, vgclslist
    
def visualize_categ_objects(image, imgobjs, categ='suit', saveDir='E:\\Data\\Genome\\figures\\'):
    response = requests.get(image.url)
    img = PIL_Image.open(StringIO(response.content))
    plt.imshow(img)
    ax = plt.gca()
    catobjs = [ob for ob in imgobjs if ob['names'][0].encode('ascii', 'ignore')==categ]
    print "Id=%d, %s, %d" %(image.id, categ, len(catobjs))
    for obj in catobjs:
        objx = float(obj['x'])
        objy = float(obj['y'])
        objw = float(obj['w'])
        objh = float(obj['h'])    
        ax.add_patch(Rectangle((objx, objy),
                               objw,
                               objh,
                               fill=False,
                               edgecolor='yellow',
                               linewidth=3))
        ax.text(objx, objy, obj['names'][0], style='italic', bbox={'facecolor':'white', 'alpha':0.7, 'pad':10})
    fig = plt.gcf()
    plt.tick_params(labelbottom='off', labelleft='off')
    savePath = os.path.join(saveDir, categ)
    if not os.path.exists(savePath):
        os.makedirs(savePath)
    plt.savefig(os.path.join(savePath, str(image.id)+'.png'), bbox_inches='tight')
    #plt.show()    
    plt.clf()
    
def visImgCateg(imgOrd, imgIdx, objs, categ='suit'):
    image = vg.GetImageData(id=imgIdx)
    if len(objs) ==0:
        objs = json.load(open("E:\Data\Genome\meta_data\objects.json"), encoding='ascii')
    visualize_categ_objects(image, objs[imgOrd]['objects'],categ)
    
def getImgIdList(imglist):
    # allImgIdList = vis.getImgIdList(vgimglist)
    return [imglist[i]['id'] for i in range(len(imglist))]
    
def visCateg(vgclslist, vgimglist, imglist, objs, categ='suit'):
    ids = [index for (index, w) in enumerate(vgclslist) if w == categ]
    catImgIdList = [vgimglist[i] for i in ids]
    catImgIdList = list(set(catImgIdList))
    allImgIdList = getImgIdList(imglist)
    topNum = 10
    for imgName in catImgIdList[:min(topNum,len(catImgIdList))]:
        imgIdx = int(imgName)
        imgOrd = allImgIdList.index(imgIdx)
        visImgCateg(imgOrd, imgIdx, objs, categ)
        
def visAllCateg(vgclslist, vgimglist, imglist, objs):
    counter = Counter(vgclslist)
    counter = counter.most_common()
    for key, count in counter:
        categ = key
        visCateg(vgclslist, vgimglist, imglist, objs, categ)
        