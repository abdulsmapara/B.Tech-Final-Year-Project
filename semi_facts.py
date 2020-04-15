from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
import spacy
from spacy import displacy

def convert_pdf_to_txt(ip_file):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = open(ip_file, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos=set()

    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)

    text = retstr.getvalue()

    fp.close()
    device.close()
    retstr.close()
    return text


def preprocessing(ip_file):
    retval = ''
    for line in ip_file:
        input_sentences = list(line.split())
        if(len(input_sentences) >= 6):
            retval = retval + line + '\n'
    return retval

def semi_structured_extraction(ip_file, op_file):
    temp_str1 = convert_pdf_to_txt(ip_file)
    text_lines = temp_str1.splitlines()
    temp_str2 = preprocessing(text_lines)
    
    nlp = spacy.load("en_core_web_sm")
    content = temp_str2
    doc = nlp(content)
    
    chunks_dict = dict()
    for chunk in doc.noun_chunks:
        chunks_dict[chunk.root.text] = chunk.text

    sub = ''
    obj = ''
    new_sub = ''
    fact_list = []
    flag = 0
    for token in doc:
        if token.dep_ == 'ROOT':
            comp_obj = ''
            prep_obj = ''
            extra_sub = ''
            for child in token.children:
                if child.dep_ == 'nsubj':
                    sub = child.text
                    for more_child in child.children:
                        if more_child.dep_ == 'prep':
                            extra_sub = more_child.text
                    for chunk in doc.noun_chunks:
                        if chunk.root.text == sub:
                            new_sub = chunk.text 
                        if chunk.root.head.text == extra_sub:
                            extra_sub_text = chunk.text
                            flag = 1
                    if flag == 1:
                        new_sub = new_sub + ' ' + extra_sub + ' ' + extra_sub_text
                        flag = 0
                        extra_sub = ''
                        extra_sub_text = ''
                if child.dep_ == 'prep':
                    for more_child in child.children:
                        if more_child.dep_ == 'pobj' or more_child.dep_ == 'dobj':
                            obj = more_child.text
                            for another_child in more_child.children:
                                obj = another_child.text + ' ' + obj
                        prep_obj = prep_obj + ' ' + obj
                if child.dep_ == 'dobj' or child.dep_ == 'pobj':
                    obj = child.text
                    if obj in chunks_dict:
                        obj = chunks_dict[obj]
                    comp_obj = comp_obj + ' ' +obj

            if new_sub != '' and token.text != '' and (prep_obj != '' or comp_obj != ''):
                if prep_obj != '':
                    prep_obj = prep_obj.replace('\n', '')
                if comp_obj != '':
                    comp_obj = comp_obj.replace('\n', '')
                if '\n' in new_sub:
                    index = new_sub.find('\n')
                    if index != -1:
                        new_sub = new_sub[index+1:]
                    for c in new_sub:
                        if ord(c) > 256:
                            new_sub = new_sub.replace(c,'')
                    while new_sub[0] == ' ':
                        new_sub = new_sub[1:]
                new_str = new_sub + '|' + token.text + '|' + prep_obj +  comp_obj
                if new_str not in fact_list:
                    fact_list.append(new_str)
            

    o_f = open(op_file, 'w', encoding='utf8')

    for s in fact_list:
        o_f.write(s+'\n')
    
    o_f.close()


ip_file = '../DATA1/SBI-2Aug.pdf'
op_file = 'op_facts_2_aug.txt'
semi_structured_extraction(ip_file, op_file)