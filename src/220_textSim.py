import shutil
import requests
import os
import json
import glob
import yaml
import sys
import urllib
import ssl
import csv
import time


def download_img(url, file_name):
    result = []
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0"
        }
        request = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(request) as web_file:
            data = web_file.read()
            with open(file_name, mode='wb') as local_file:
                local_file.write(data)
            print("--- downloaded", id)
    except urllib.error.URLError as e:
        print(id, url, e)
        result = [id, url, e]
    return result

path = "../docs/iiif/top.json"

def aaa(manifests, collection):
    manifests2 = []
    if "collections" in collection:
        collections = collection["collections"]

        for i in range(len(collections)):
            collection2 = collections[i]
            manifests2 = aaa(manifests2, collection2)

    elif "manifests" in collection:
        manifests2 = collection["manifests"] 
    
    for j in range(len(manifests2)):
        manifests.append(manifests2[j])

    return manifests

with open(path) as f:
    collection = json.load(f)
    
manifests = aaa([], collection)

labels = []
ids = []

for manifest in manifests:
    label = manifest["label"]
    labels.append(label)

    ids.append(manifest["@id"])

# print(collection)

# -*- coding: utf-8 -*-
import numpy as np
 
#わかち書き関数
def wakachi(text):
    from janome.tokenizer import Tokenizer
    t = Tokenizer()
    tokens = t.tokenize(text)
    docs=[]
    for token in tokens:
        docs.append(token.surface)
    return docs
 
#文書ベクトル化関数
def vecs_array(documents):
    from sklearn.feature_extraction.text import TfidfVectorizer
 
    docs = np.array(documents)
    vectorizer = TfidfVectorizer(analyzer=wakachi,binary=True,use_idf=False)
    vecs = vectorizer.fit_transform(docs)
    return vecs.toarray()

from sklearn.metrics.pairwise import cosine_similarity

docs = labels

#類似度行列作成
cs_array = np.round(cosine_similarity(vecs_array(docs), vecs_array(docs)),3)

size = 20

for i in range(len(cs_array)):
    row = cs_array[i]
    
    manifest = manifests[i]

    uri =  manifest["@id"]
    id = uri.split("/")[-2]

    arr = sorted(range(len(row)), key=lambda k: row[k], reverse=True)

    texts = []

    for j in range(0, 1 + size):
        index = arr[j]
        id2 = manifests[index]["@id"]

        if id2 != uri:
            texts.append(id2)

    manifest["texts"] = texts

    

    path = "../docs/iiif/"+id+"/manifest.json"

    with open(path, 'w') as outfile:
        json.dump(manifest, outfile, ensure_ascii=False,
                    indent=4, sort_keys=True, separators=(',', ': '))