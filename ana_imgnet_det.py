from nltk.corpus import wordnet as wn


def wnid_imgnet_det():
    filename = "E:\Data\ILSVRC2015\data\map_det.txt"
    wnidlist = []
    namelist = []
    with open(filename, 'r') as f:
        for line in f.readlines():
            wnid = str(line).split()[0]
            wnid = int(wnid[1:]) # starts from n0xxx
            wnidlist.append(wnid)
            namelist.append(str(line).split()[2])
    imdict = dict(zip(wnidlist, namelist))
    return wnidlist, namelist, imdict
    
def name_by_wnid(imdict, wnidlist):
    return [imdict[x] for x in wnidlist]
    
