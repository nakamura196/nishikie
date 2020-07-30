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

for manifest in manifests:
    uri = manifest["@id"]
    id = uri.split("/")[-2]
    print("id", id)

    path = "data/json/similar_images/"+id+".json"

    if os.path.exists(path):
        with open(path) as f:
            data = json.load(f)

        images = []
        max = 20
        if len(data) < max:
            max = len(data)
        for i in range(0, max):
            images.append(uri.replace("/"+id+"/", "/"+data[i]+"/"))
        manifest["images"] = images

        path = "../docs/iiif/"+id+"/manifest.json"

        with open(path, 'w') as outfile:
            json.dump(manifest, outfile, ensure_ascii=False,
                        indent=4, sort_keys=True, separators=(',', ': '))