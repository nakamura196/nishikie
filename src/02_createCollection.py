import json
import bs4
import os
from PIL import Image


files = ["isin1cvr.htm", "fushi2.html", "fushi4.htm"]

labels = {
    "isin1cvr.htm" : "維新前後諷刺画　一",
    "fushi2.html" : "維新前後諷刺画　二",
    "fushi4.htm" : "維新前後諷刺画　四"
}

prefix = "https://nakamura196.github.io/nishikie/iiif"
prefix2 = "https://www.hi.u-tokyo.ac.jp/personal/yokoyama/nishikie"

top = {
    "@context": "http://iiif.io/api/presentation/2/context.json",
    "@id": prefix + "/top.json",
    "@type": "sc:Collection",
    "label": "東京大学史料編纂所錦絵コレクション",
    "description" : "このページは、東京大学史料編纂所画像史料解析センターの９７年度事業として所が所蔵する錦絵を紹介するために作られました。今後は、データベースからのイメージリンクという影写本で確立した方法を目指しますが、とりあえずカラーイメージによる『維新前後諷刺画』をギャラリーとして常設します。錦絵コレクション全体をざっと見る場合は、こちらのギャラリーのほうが便利だと思いますので、ご利用ください。\nイメージは、直接画像を見ていただければわかりますが、色補正などは行なっておりません。また、圧縮は多少強めにかけてあります。JPEGフルカラーですが、適当なビューワを御使いになり、256色まで減色すると画像としては見やすくなるようです。しかし、サーバの画像としては、軽さやさまざまな需要に対応するという理由から、現状のような形式を採用してあります。\n96年度特定研究経費「幕末維新期の対外関係史料の収集・分析」によって、史料編纂所が所蔵する主要な錦絵コレクション約1000葉が撮影・データ処理されました。これらの多くは維新史料編纂会引継本です。\nフィルムを必要とする方は、図書部までお問い合わせください。",
    "attribution" : "1997(C)東京大学史料編纂所",
    "thumbnail" : "http://www.hi.u-tokyo.ac.jp/personal/yokoyama/nishikie/title.jpg",
    "vhint": "use-thumb"
}

collections = []
top["collections"] = collections

for id in files:
    file = "../data/html/"+id


    collection = {
        "@type": "sc:Collection",
        "label": labels[id],
    }
    collections.append(collection)

    soup = bs4.BeautifulSoup(open(file), 'html.parser')

    trs = soup.find_all("tr")
    print(len(trs))

    manifests = []
    collection["manifests"] = manifests



    for tr in trs:
        aas= tr.find_all("a")
        if len(aas) > 0:
            href = aas[0].get("href")

            id2 = href.split(".")[0]

            mpath = "../docs/iiif/"+id2+"/manifest.json"
            
            with open(mpath) as f:
                manifest = json.load(f)
                manifests.append(manifest)


fw = open("../docs/iiif/top.json", 'w')
json.dump(top, fw, ensure_ascii=False, indent=4,
          sort_keys=True, separators=(',', ': '))