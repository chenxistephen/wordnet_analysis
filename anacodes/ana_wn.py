from nltk.corpus import wordnet as wn
from collections import namedtuple
from lxml import etree

#Synset = namedtuple('Synset', ['synset', 'hyponyms'])

class Synset:
    def __init__(self, synset, hyponyms):
        self.synset = synset
        self.hyponyms = hyponyms

def get_all_synsets():
    wnIdToSynset = {s.offset:s for s in wn.all_synsets()}
    print("%d synsets are read"%(len(wnIdToSynset)))
    return wnIdToSynset

def get_hyponyms(synset):
    hyponyms = []
    for c in synset.hyponyms():
        hyponyms.append(Synset(c, get_hyponyms(c)))
    for c in synset.instance_hyponyms():
        hyponyms.append(Synset(c, get_hyponyms(c)))
    return hyponyms
    
def get_all_entity_synsets(categ='clothing'):
    entity_syn = wn.synsets(categ)[0]
    entity = Synset(entity_syn, get_hyponyms(entity_syn))
    return entity

def get_child_wnids(synset, wnid_set):
    for c in synset.hyponyms:
        wnid_set.add(c.synset.offset())
    for c in synset.hyponyms:
        get_child_wnids(c, wnid_set)

def read_wnids(fn):
    wnids = []
    with open(fn) as fin:
        wnids = [int(l[:l.find(' ')]) for l in fin]
    print ("%d wnids are read in %s"%(len(wnids), fn))
    return wnids

def prune_entity_tree(synset, wnid_set):
    for i in range(len(synset.hyponyms)):
        synset.hyponyms[i] = prune_entity_tree(synset.hyponyms[i], wnid_set)
    synset.hyponyms[:] = [s for s in synset.hyponyms if (len(s.hyponyms)!=0 or s.synset.offset() in wnid_set)]
    return synset  

   
def unstr(s):
    # important, standarized "-" and " " to "_" for string matching
    s = s.replace('-','_')
    s = s.replace(' ','_')
    return s

def wnGetTreeList(entity, treelist, idlist):
    useLemma = 1
    ename = str(entity.name().split('.')[0])
    wordType = str(entity.name().split('.')[1]) # noun or verb
    if wordType != 'n':
        print ename, " is NOT a noun!"
        return;
    ename = unstr(ename) # important, standarized "-" and " " to "_" for string matching
    treelist.append(ename)
    idlist.append(entity.offset())
    if useLemma:
        for lm in entity.lemma_names(): # use lemma_names to increase recall
            lname = str(lm.split('.')[0])
            # print lname
            lname = unstr(lname)# important, standarized "-" and " " to "_" for string matching
            treelist.append(lname)
    
    for c in entity.hyponyms():
        wnGetTreeList(c, treelist, idlist)
        
# def getWordNetList_org(categ='clothing'):
    # entity = wn.synsets(categ)
    # entity = entity[0]
    # treelist = []
    # idlist = []
    # wnGetTreeList(entity, treelist, idlist)
    # return treelist, idlist        

def getWordNetList(categ='clothing'):
    entity = wn.synsets(categ)
    i = 0
    namelist = []
    idlist = []
    for en in entity:
        print categ, "[", str(i), "]:", en
        i+=1
        names = []
        ids = []
        wnGetTreeList(en, names, ids)
        namelist += names
        idlist += ids
    return namelist, idlist
    
    
    
    
    
    
    
if(__name__ == '__main__'):
    main()