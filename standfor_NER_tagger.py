from nltk.tag import StanfordNERTagger
from nltk import pos_tag
from nltk.chunk import conlltags2tree
from nltk.tree import Tree
from nltk.corpus import stopwords
import re

def stopFunc(text):
    stop = stopwords.words('english')
    temp = []
    temp += [i for i in text.split() if i not in stop]
  #  print temp
    return temp

def cleanse_data(text):

##
    ##  Remove all non relevent symbols and get the text
    ## that can be used to clean our data with noise
##
  #  print text
    temp = text #.lower()
    temp = re.sub(r"[\r\n\t ]+"," ",temp)
    temp = re.sub(r'[\w\.-]+@[\w\.-]+',"EMAIL",temp)
    temp = re.sub(r'((\+91( |-)?)?\d{10})','MOBILE',temp)
  #  print temp
    temp = re.sub(r'[^\w.]+',' ',temp)
  #  print temp
    lstemp = stopFunc(temp)
    fp = open("stop_temp.txt","w")
    for item in lstemp:
        fp.write("%s\n" % item)
#    fp.write(lstemp)
    fp.close()
    return ' '.join(lstemp)

def stanfordNE2BIO(tagged_sent):
    bio_tagged_sent = []
    prev_tag = "O"
    for token, tag in tagged_sent:
        if tag == "O": #O
            bio_tagged_sent.append((token, tag))
            prev_tag = tag
            continue
        if tag != "O" and prev_tag == "O": # Begin NE
            bio_tagged_sent.append((token, "B-"+tag))
            prev_tag = tag
        elif prev_tag != "O" and prev_tag == tag: # Inside NE
            bio_tagged_sent.append((token, "I-"+tag))
            prev_tag = tag
        elif prev_tag != "O" and prev_tag != tag: # Adjacent NE
            bio_tagged_sent.append((token, "B-"+tag))
            prev_tag = tag

    return bio_tagged_sent


def stanfordNE2tree(ne_tagged_sent):
    bio_tagged_sent = stanfordNE2BIO(ne_tagged_sent)
    sent_tokens, sent_ne_tags = zip(*bio_tagged_sent)
    sent_pos_tags = [pos for token, pos in pos_tag(sent_tokens)]

    sent_conlltags = [(token, pos, ne) for token, pos, ne in zip(sent_tokens, sent_pos_tags, sent_ne_tags)]
    ne_tree = conlltags2tree(sent_conlltags)
    return ne_tree


def main():
    

    # training standford NER tagger

    st = StanfordNERTagger('/home/viswanath/Downloads/stanford-ner-2014-08-27/classifiers/english.conll.4class.distsim.crf.ser.gz','/home/viswanath/Downloads/stanford-ner-2014-08-27/stanford-ner.jar',encoding='utf-8')

    fname = "/home/viswanath/data/resume/test_data/01.txt"
    fp = open(fname,"r")
    text = fp.read()
  #  print text
    lstemp = cleanse_data(text)
    list_ner_out = st.tag(lstemp.split())
 #   list_ner_out = st.tag(text.split())
 #   print list_ner_out
    #list_out = st.tag('Rami Eid is studying at Stony Brook University in NY'.split())

    fp = open("ner_temp.txt","w")
#    fp.write(list_ner_out)
    for item in list_ner_out:
        fp.write("{0}\n".format(item))
    fp.close()


    ne_tagged_sent = list_ner_out

    ne_tree = stanfordNE2tree(ne_tagged_sent)

    print ne_tree

    ne_in_sent = []
    for subtree in ne_tree:
        if type(subtree) == Tree: # If subtree is a noun chunk, i.e. NE != "O"
            ne_label = subtree.label()
            ne_string = " ".join([token for token, pos in subtree.leaves()])
            ne_in_sent.append((ne_string, ne_label))
    print ne_in_sent

if __name__ == '__main__': main()
