from nltk.corpus import wordnet as wn
from collections import namedtuple
from lxml import etree
from ana_wn import *
import sys


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

def imgnet_synset(categ='clothing'):
    #wnIdToSynset = get_all_synsets()
    imagenet_wnids = read_wnids(r'E:\Data\imagenet_22K_raw_data\winds.txt')
    
    entity = get_all_entity_synsets(categ)
    entity = prune_entity_tree(entity, imagenet_wnids)
    
    entity_wnid_set = set([entity.synset.offset()])
    get_child_wnids(entity, entity_wnid_set)
    print("%d wnids are ketp after pruning image net"%(len(entity_wnid_set)))
    return entity
    
    
def wnid_imgnet_22k():
    filename = "E:\Data\imagenet_22K_raw_data\winds.txt"
    wnidlist = []
    namelist = []
    with open(filename, 'r') as f:
        for line in f.readlines():
            wnid = str(line).split()[0]
            wnid = int(wnid) # starts from 00xxx
            wnidlist.append(wnid)
            wname = " ".join(str(line).split()[1:])
            namelist.append(wname)
    imdict = dict(zip(wnidlist, namelist))
    return wnidlist, namelist, imdict
    
def name_by_wnid(imdict, wnidlist):
    return [imdict[x] for x in wnidlist]  


def inter():
    wnidlist22k, namelist22k, imdict22k = wnid_imgnet_22k()
    treelist, idlist_wn = getWordNetList('clothing')
    its = set(wnidlist22k).intersection(idlist_wn)
    internames = name_by_wnid(imdict22k, its)
    for ii in range(len(internames)):
        sys.stdout.write(internames[ii]+" || ")
        #if ii % 6 == 5:
        #    sys.stdout.write("\n")
    return internames
    
    