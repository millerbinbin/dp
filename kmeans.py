# -*- coding:utf-8 -*-
import numpy as np  # 科学计算包
import matplotlib.pyplot as plt  # python画图包

from sklearn.cluster import KMeans  # 导入K-means算法包
from sklearn.datasets import make_blobs
from db import tasks
import json

plt.figure(figsize=(12, 12))

''''' 
make_blobs函数是为聚类产生数据集 
产生一个数据集和相应的标签 
n_samples:表示数据样本点个数,默认值100 
n_features:表示数据的维度，默认值是2 
centers:产生数据的中心点，默认值3 
cluster_std：数据集的标准差，浮点数或者浮点数序列，默认值1.0 
center_box：中心确定之后的数据边界，默认值(-10.0, 10.0) 
shuffle ：洗乱，默认值是True 
random_state:官网解释是随机生成器的种子 
更多参数即使请参考：http://scikit-learn.org/dev/modules/generated/sklearn.datasets.make_blobs.html#sklearn.datasets.make_blobs 
'''
random_state = 170
shops = tasks.get_all_shops_location()

data = []
idx = 0
for shop in tasks.get_customize_shops():
    data.append({"name": shop[0], "lng": float(shop[1]), "lat": float(shop[2]), "avg_price": float(shop[3]),
                 "taste_score": float(shop[4]), "category": shop[5]})
    idx += 1
    if idx == 300: break
print json.dumps(data, ensure_ascii=False).encode("utf-8")
exit(1)

X = np.array([[shop[1], shop[2]] for shop in shops])
clf = KMeans(n_clusters=10, random_state=random_state).fit(X)
centers = clf.cluster_centers_
print centers
labels = clf.labels_
groups = {}
for i in range(len(shops)):
    group_id = labels[i]
    groups[group_id] = 1 if groups.get(group_id) is None else groups.get(group_id) + 1
    #print shops[i], labels[i]
print groups



# n_samples = 10
# random_state = 170
# X, y = make_blobs(n_samples=n_samples, random_state=random_state)
y_pred = KMeans(n_clusters=10, random_state=random_state).fit_predict(X)


plt.subplot(221)  #在2图里添加子图1
plt.scatter(X[:, 0], X[:, 1], c=y_pred) #scatter绘制散点
plt.title("Incorrect Number of Blobs")   #加标题
#plt.show()

