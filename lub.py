import spacy
import docx
import json
import re
from spacy.lang.ru import Russian

shifr_dict = {'acomp': 'дополнение',
              'ncomp': 'дополнение',
              'xcomp': 'дополнение',
              'amod': 'определение',
              'nmod': 'определение',
              'advmod': 'обстоятельство',
              'aux': 'вспомогательный глагол',
              'compound': 'составное слово',
              'dative': 'дательный падеж',
              'det': 'определитель',
              'dobj': 'прямое дополнение',
              'nsubj': 'подлежащее',
              'iobj': 'дополнение',
              'obj': 'дополнение',
              'pobj': 'дополнение',
              'obl': 'обстоятельство',
              'conj': 'conj'

              }


def read_from_doc(doc_name, main_dict):  # с docx считать все обзацы
    doc = docx.Document(doc_name)
    text = []
    for paragraph in doc.paragraphs:
        for i in re.split("\.|!|\?", paragraph.text):
            if len(i) < 2:
                continue
            text.append(i)
    print(text)
    save_dict(add_dict(text, main_dict))
    return text


def save_dict(data):  # храним в json, надеюсь так можно
    with open('dict.json', 'w') as file:
        json.dump(data, file)


def read_dict():
    with open('dict.json', 'r') as file:
        dict = json.load(file)
        return dict


def add_dict(text, dict):
    for sent in text:
        nlp = spacy.load("ru_core_news_sm")
        doc = nlp(sent)
        all_tokens = []
        for token in doc:
            if token.dep_ not in shifr_dict.keys():
                continue
            token_info = [token.head.text, token.text, shifr_dict[token.dep_]]
            all_tokens.append(token_info)
            # print(f"{token_text:<12}{token_dep:<10}{token_head:<12}")
        for toc in all_tokens:
            if toc[2] == 'conj':
                flag = False
                for toc_1 in all_tokens:
                    if toc[0] == toc_1[1]:
                        toc[0] = toc_1[0]
                        toc[2] = toc_1[2]
                        flag = True
                if not flag:
                    all_tokens.remove(toc)
        dict[sent] = all_tokens
    return dict


def find_sent_in_dict(main_dict, word):
    for sent in main_dict.keys():
        if word in sent:
            return [sent, main_dict[sent]]


def delete_from_dict(main_dict, our_sent):
    for sent in main_dict.keys():
        if our_sent == sent:
            main_dict.pop(sent)
            return main_dict


def search_rel(main_dict, our_sent):
    for sent in main_dict.keys():
        if our_sent == sent:
            return main_dict[sent]


def change_analiz(main_dict, our_sent, param_list, new_par):
    for sent in main_dict.keys():
        if our_sent == sent:
            for tokens in main_dict[sent]:
                if tokens == param_list:
                    tokens[2] = new_par
                    return main_dict



