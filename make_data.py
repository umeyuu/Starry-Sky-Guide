import pandas as pd
import numpy as np

# ピクセルの緯度経度を返す関数
def pixel_to_latlng(pixel_x, pixel_y,zoom = 7):
    L = 85.05112878
    longitude = 180*(pixel_x/(2**(zoom+7))-1)
    latitude = 180*(np.arcsin(np.tanh(-np.pi*pixel_y/(2**(zoom+7))+np.arctanh(np.sin(np.pi*L/180)))))/np.pi
    return latitude,longitude

# タイル画像の緯度経度、標高のデータフレームを返す関数
def get_hyoko(x, y, z):
    
    # 任意のタイル画像の1ピクセルの標高を256×256のデータフレームで取得
    url = "https://cyberjapandata.gsi.go.jp/xyz/demgm/{z}/{x}/{y}.txt".format(z=z,x=x,y=y)
    df = pd.read_csv(url, header=None).replace("e",0)
    ind = []
    col = []
    
    # 取得した画像のピクセルの緯度経度を取得
    for i in range(256):
        a, b = pixel_to_latlng(x*256 + i, y*256 + i,zoom = z)
        ind.append(a)
        col.append(b)

    # データフレームの列を経度に、行を緯度に変換
    df.index = ind
    df.columns = col
    
    # 標高の値をflaat型に変換
    df = df.astype(float)

    # 標高が0より高い地点の緯度経度と標高のデータフレームを返す
    latlon = []
    for k in df.columns:
        ind = df[df[k]>0][k].index
        hyoko = df[df[k]>0][k].values
        for i, h in zip(ind, hyoko):
            latlon.append([h, i, k])

    return pd.DataFrame(latlon, columns = ['標高', '緯度', '経度'])

def get_latlon_height():
    # zoom率　5で日本があるタイル画像の緯度経度、標高を取得
    h1 = get_hyoko(29,11,5)
    h2 = get_hyoko(28,11,5)
    h3 = get_hyoko(28,12,5)
    h4 = get_hyoko(27,12,5)
    h5 = get_hyoko(27,13,5)

    # 韓国、ロシア等の不要な所を削除
    h2 = h2[h2['緯度']<45.583289]
    h2 = h2[h2['経度']>138.339843]
    h3_1 = h3[(h3['緯度']<33.961586)&(h3['経度']>128.397216)]
    h3_2 = h3[(h3['経度']>130.198974)&(h3['緯度']>33.961586)]
    h3 = pd.concat([h3_1, h3_2])
    h1 = h1[h1['経度']<149.161376]
    ans = pd.concat([h5,h4,h3,h2,h1])
    ans = ans[~((ans['緯度']>34.786739)&(ans['経度']<131.022949))]
    ans = ans[~((ans['緯度']>33.491016)&(ans['経度']<128.979492))]
    ans = ans[~((ans['緯度']>32.768800)&(ans['経度']<127.199707))]

    ans.to_pickle('jp.pickle')

if __name__ == '__main__':
    # 緯度経度データとその地点の標高データ
    data = pd.read_pickle('jp.pickle')
    # NO2とCOのデータ
    air_df = pd.read_pickle('air.pickle')
    # 夜間光データ
    light_df = pd.read_pickle('light.pickle')

    # 緯度経度、標高データに合わせてNO2、CO、夜間光データを合体する
    from tqdm import tqdm

    ans=[]

    for x,y,h in tqdm(zip(data['経度'], data['緯度'], data['標高'])):
        z1 = air_df[(air_df['x_min']<x) & (x < air_df['x_max']) & (air_df['y_min']<y) & (y < air_df['y_max'])]
        z2 = z1['no2'].values.mean()
        z3 = z1['co'].values.mean()
        z4 = light_df[(light_df['x_min']<x) & (x < light_df['x_max']) & (light_df['y_min']<y) & (y < light_df['y_max'])]
        z4 = z4['light'].values.mean()
        ans.append([z2,z3,z4,h,x,y])
            

    ans = pd.DataFrame(ans,columns=['NO2','CO','light','標高','緯度','経度'])
