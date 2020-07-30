from annoy import AnnoyIndex
import glob
from os.path import join
import numpy
import os
import json
import yaml
import argparse    # 1. argparseをインポート

############

# 初期設定
with open('../../.env.yml') as file:
    yml = yaml.load(file, Loader=yaml.SafeLoader)

skip_flg = False

############

parser = argparse.ArgumentParser(description='このプログラムの説明（なくてもよい）')    # 2. パーサを作る

# 3. parser.add_argumentで受け取る引数を追加していく
parser.add_argument('collections', help='カンマで')    # 必須の引数を追加

args = parser.parse_args()    # 4. 引数を解析

collections = args.collections.split(",")

if collections[0] == "all":
    collections = os.listdir(yml["thumb_dir"] + "/")
print(collections)

############

# 次元
dims = 2048

# 検索対象数
n_nearest_neighbors = 200
n_nearest_neighbors = n_nearest_neighbors + 1

t = AnnoyIndex(dims, metric='angular')
t.load('data/index.ann')

# インデックスマップの読み込み（Annoyのインデックス内のIDと特徴ベクトルの対応）

map_path = "data/file_index_map.json"
file_index_map = {}
max = 0
with open(map_path) as f:
    data = json.load(f)
    index_id_map = {}
    id_index_map = {}
    for index in data:
        index_id_map[int(index)] = data[index]
        id_index_map[data[index]] = int(index)
        max += 1

# 予測

count = 0
for id in sorted(id_index_map):

    if "rmda-" not in id:
        continue

    count += 1
    print(str(count)+"/" + str(max) + "\t" + id)

    collection_id = id.split("-")[0]

    if collection_id not in collections:
        continue

    dir = yml["json_dir"] + "/similar_images/" + collection_id
    os.makedirs(dir, exist_ok=True)

    opath = dir + "/" + id + ".json"
    if os.path.exists(opath) and skip_flg:
        continue

    query_index = id_index_map[id]
    nearest_neighbors = t.get_nns_by_item(
        query_index, n_nearest_neighbors, include_distances=False)  # True)

    indexes = nearest_neighbors  # [0]

    # scores = nearest_neighbors[1]

    similar_images = []

    for i in range(1, len(indexes)):

        target_index = indexes[i]

        target_id = index_id_map[target_index]
        '''

        similarity = scores[i]

        rounded_similarity = int((similarity * 10000)) / 10000.0

        
        data.append({
            "id" : target_id,
            "score" : rounded_similarity
        })
        '''
        similar_images.append(target_id)

    fw = open(opath, 'w')
    json.dump(similar_images, fw, ensure_ascii=False, indent=4,
              sort_keys=True, separators=(',', ': '))
