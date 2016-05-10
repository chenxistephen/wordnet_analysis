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

def generate_xml_element(synset):
    e = etree.Element('synset')
    e.set('wnid', str(synset.synset.offset()))
    e.set('name', str(synset.synset.name()))
    e.set('words', ','.join(synset.synset.lemma_names()))
    e.set('gloss', str(synset.synset.definition()))
    for c in synset.hyponyms:
        ec = generate_xml_element(c)
        e.append(ec)
    return e
    
def tree2list(synset, namelist):
    e = etree.Element('synset')
    #e.set('wnid', str(synset.synset.offset()))
    namelist.append(str(synset.synset.name()).split('.')[0])
    #e.set('words', ','.join(synset.synset.lemma_names()))
    #e.set('gloss', str(synset.synset.definition()))
    for c in synset.hyponyms:
        ec = tree2list(c, namelist)
        # e.append(ec)
    #return e 

def getTreeList(synset):
    namelist = []
    tree2list(synset, namelist)
    return namelist

def main():
    #wnIdToSynset = get_all_synsets()
    imnet_set = imgnet_synset('clothing')
    imnet_list = getTreeList(imnet_set)
    
    print('finished writing the xml file')
    


def wnGetTreeList(entity, treelist, idlist):
    ename = str(entity.name().split('.')[0])
    treelist.append(ename)
    idlist.append(entity.offset())
    for c in entity.hyponyms():
        wnGetTreeList(c, treelist, idlist)

def getWordNetList(categ='clothing'):
    entity = wn.synsets(categ)
    entity = entity[0]
    treelist = []
    idlist = []
    wnGetTreeList(entity, treelist, idlist)
    return treelist, idlist
    
    
    
    
    
    
    
if(__name__ == '__main__'):
    main()