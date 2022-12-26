# Starry-Sky-Guide

機械学習と衛星データを用いることによって、｢どこが、どのくらい星空が綺麗か」が客観的に分かる星空マップを作成した。星空マップは「星空の案内人」というwebサイトを作成して、公開した。

星空の案内人のリンク → http://spacetech.snowycat.info/

<img width="846" alt="image" src="https://user-images.githubusercontent.com/91179464/209533227-59cc3bae-db39-4c62-ac21-9795e35d7266.png">

`make_data.py` : データセットを作成するpythonファイル

`analize.ipynb` : 特徴量を解析したnotebook

`make_map.ipynb` : 星空のキレイ度を予測した結果を星空マップとして表示するためにgeojsonファイルを作成したnotebook

## DATA
星空のキレイ度 : [[環境省] 星空を見よう](https://www.env.go.jp/air/life/hoshizorakansatsu/index.html)

NO2, CO, 夜間光 : [google earth engine](https://www.google.com/intl/ja_ALL/earth/education/tools/google-earth-engine/)

標高 : [国土地理院](https://www.gsi.go.jp/)
