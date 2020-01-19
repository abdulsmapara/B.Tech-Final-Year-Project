import spacy
from spacy import displacy


nlp = spacy.load("en_core_web_sm")
f = open('doc2.txt', 'r')
content = f.read()
doc = nlp(content)

chunks_dict = dict()

for token in doc:
    #print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_, token.shape_, token.is_alpha, token.is_stop)
    if token.dep_ == 'ROOT':
        print(token.text + '\t' + token.pos_ + '\t' + token.dep_)
        '''
        for  child in token.children:
            print(child.text + '\t' + child.dep_)
        '''

print('\n\n')
print('Noun Chunks')
for chunk in doc.noun_chunks:
    print(chunk.text + '\t' +  chunk.root.dep_, chunk.root.head.text)
    chunks_dict[chunk.root.text] = chunk.text
displacy.serve(doc, style="dep")
sub = ''
obj = ''
new_sub = ''
fact_list = []
for token in doc:
    if token.dep_ == 'ROOT':
        print('Root is ' + token.text)
        for child in token.children:
            if child.dep_ == 'nsubj':
                sub = child.text
                for chunk in doc.noun_chunks:
                    if chunk.root.text == sub:
                        new_sub = chunk.text 
            if child.dep_ == 'prep':
                for more_child in child.children:
                    if more_child.dep_ == 'pobj' or more_child.dep_ == 'dobj':
                        obj = more_child.text
                        for another_child in more_child.children:
                            obj = another_child.text + ' ' + obj
                new_str = new_sub + '|' + token.text + '|' + obj
                fact_list.append(new_str)
            if child.dep_ == 'dobj' or child.dep_ == 'pobj':
                obj = child.text
                if obj in chunks_dict:
                    obj = chunks_dict[obj]
                new_str = new_sub + '|' + token.text + '|' + obj
                fact_list.append(new_str)
        #print(new_sub + '\t' + token.text + '\t' + obj)

print('FACTS:')
for s in fact_list:
    print(s) 
'''
for sent in doc.sents:
    print(sent.text)

for text in doc:
    #subject would be
    if text.dep_ == "nsubj":
        subject = text.orth_
    #iobj for indirect object
    if text.dep_ == "iobj":
        indirect_object = text.orth_
    #dobj for direct object
    if text.dep_ == "dobj":
        direct_object = text.orth_

print(subject)
print(direct_object)
#print(indirect_object)
'''