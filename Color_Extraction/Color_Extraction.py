import cv2
import matplotlib.colors as cs
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.model_selection import GridSearchCV
import json

data = {}

PATH = './saved_png/removed_bg_'
FILE_NUM = ''
FILE = '.png'

def read_img(n) :
    path = PATH + str(n) + FILE
    img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
    img = cv2.cvtColor(img, cv2.COLOR_BGRA2RGBA)
    return img

def clustering_1(img) :
    img_data = []
    x = []
    y = []
    for i in range(img.shape[0]) :
        for j in range(img.shape[1]) :
            if img[i][j][3] != 0 :
                img_data.append(img[i][j])
                x.append(i)
                y.append(j)

    clustering = KMeans(n_clusters = 7, init = 'k-means++')
    clustering.fit(img_data)

    labels = np.unique(clustering.labels_)
    hist, _ = np.histogram(clustering.labels_, bins = np.arange(len(labels) + 1))
    n = [0, 0, 0, 0, 0, 0, 0]
    for i in range(len(clustering.labels_)) :
        for j in range(len(labels)) : 
            if (clustering.labels_[i] == labels[j]) :
                n[j] += 1
    p = [0, 0, 0, 0, 0, 0, 0]
    for i in range(len(p)) :
        p[i] = n[i] / len(clustering.labels_)
    main_label = []
    for i in range(len(p)) :
        if p[i] >= 0.08 :
            main_label.append(i)

    main_pixel = []
    x_ = []
    y_ = []
    for i in range(len(img_data)) :
        for j in range(len(main_label)) :
            if (clustering.labels_[i] == main_label[j]) :
                main_pixel.append(img_data[i])
                x_.append(x[i])
                y_.append(y[i]) 
    img_data = main_pixel
    x = x_
    y = y_

    return img_data, x, y

def clustering_2(img_data, x, y) :
    #estimator = KMeans()
    #param_grid = {'n_clusters' : [1, 2, 3, 4, 5, 6, 7]}

    #grid = GridSearchCV(estimator, param_grid = param_grid) 
    #grid.fit(img_data)
  
    #cluster_num = grid.best_params_['n_clusters']

    clustering = KMeans(n_clusters = 7, init = 'k-means++')
    clustering.fit(img_data)

    labels = np.unique(clustering.labels_)
    hist, _ = np.histogram(clustering.labels_, bins = np.arange(len(labels) + 1))
    n = [0, 0, 0, 0, 0, 0, 0]
    for i in range(len(clustering.labels_)):
        for j in range(len(labels)) : 
            if (clustering.labels_[i] == labels[j]) :
                n[j] += 1
    p = [0, 0, 0, 0, 0, 0, 0]
    for i in range(len(p)) :
        p[i] = n[i] / len(clustering.labels_)
    main_label = []
    for i in range(len(p)) :
        if p[i] >= 0.07 :
            main_label.append(i)

    x_ = []
    y_ = []
    main_pixel = []
    for i in range(len(img_data)) :
        for j in range(len(main_label)) :
            if (clustering.labels_[i] == main_label[j]) :
                main_pixel.append(img_data[i])
                x_.append(x[i])
                y_.append(y[i])
    img_data = main_pixel
    x = x_
    y = y_

    return img_data, x, y

def clustering_3(img_data, x, y) :
    #estimator = KMeans()
    #param_grid = {'n_clusters' : [1, 2, 3, 4, 5]}

    #grid = GridSearchCV(estimator, param_grid = param_grid) 
    #grid.fit(img_data)

    #cluster_num = grid.best_params_['n_clusters']

    clustering = KMeans(n_clusters = 5, init = 'k-means++')
    clustering.fit(img_data)

    labels = np.unique(clustering.labels_)
    hist, _ = np.histogram(clustering.labels_, bins = np.arange(len(labels) + 1))

    colors = []
    hexlabels = []

    for i in range(clustering.cluster_centers_.shape[0]) :
        colors.append(tuple(clustering.cluster_centers_[i] / 255))
        hexlabels.append(cs.to_hex(tuple(clustering.cluster_centers_[i] / 255)))

    #plt.pie(hist, labels = hexlabels, colors = colors, autopct = '%1.1f%%')
    #plt.show()
    
    n = [0, 0, 0, 0, 0]
    for i in range(len(clustering.labels_)):
        for j in range(len(labels)) : 
            if (clustering.labels_[i] == labels[j]) :
                n[j] += 1
    
    p = [0, 0, 0, 0, 0]
    for i in range(len(p)) :
        p[i] = n[i] / len(clustering.labels_)
        
    return clustering.cluster_centers_, p, hist, colors, hexlabels

def euclidean_distance(array1, array2):
    return np.sqrt(np.sum((array1 - array2)**2))

def color_mapping(file, cluster_centers_rgb) :
    data = pd.read_csv(file, sep = ',', encoding = 'utf-8')
    colors = data['color_mapped']
    rgb = data[['R', 'G', 'B']].values
    
    distances = []
    color_mapped_list = []
    color_mapped = []
    color_list = []
    for i in range(len(cluster_centers_rgb)) :
        for j in range(len(rgb)) :
            distances.append(euclidean_distance(cluster_centers_rgb[i], rgb[j]))
        min_dist = min(distances)
        index = distances.index(min_dist)
        color_list.append(colors[index])
        color_mapped = rgb[index].tolist()
        color_mapped_list.append(color_mapped)
        color_mapped = []
        distances = []
 
    return np.array(color_mapped_list), color_list

def rgb_to_hex(r, g, b) :
    #r, g, b = int(r), int(g), int(b)
    return '#' + hex(r)[2:].zfill(2) + hex(g)[2:].zfill(2) + hex(b)[2:].zfill(2)

def save_result(data, cluster_centers, p, n) :
    file_name = 'removed_bg_' + str(n) + '.png'
    data[file_name] = {}
    data[file_name]['colors'] = cluster_centers.tolist()
    data[file_name]['ratio'] = p
    with open('result.json', 'w') as f : 
        json.dump(data, f, indent = 4)

if __name__ == '__main__' :

    n = 0 # 테스트하고 싶은 이미지의 번호
    img = read_img(n)
    img_data, x, y = clustering_1(img)
    img_data, x, y = clustering_2(img_data, x, y)
    cluster_centers, p, hist, colors, hexlabels = clustering_3(img_data, x, y)
    index = p.index(max(p))
    cluster_centers_rgb = cluster_centers[:, 0:3]
    color_mapped, color_list = color_mapping('./color_matching_list.csv', cluster_centers_rgb)
    color_label = color_list[index]
    hex_labels = []
    for i in range(len(color_mapped)) :
        hex_labels.append(rgb_to_hex(color_mapped[i][0], color_mapped[i][1], color_mapped[i][2]))
    print(color_label)
    fig, ax = plt.subplots(2, 1, figsize=(5, 5))
    ax[0].pie(hist, labels = hexlabels, autopct = '%.1f%%', colors = colors)
    ax[0].set_title('Before')
    ax[1].pie(p, labels = hex_labels, autopct = '%.1f%%', colors = hex_labels)
    ax[1].set_title('After')
    plt.show()
    hexlabels = []
    colors = []

    # 샘플 이미지 830장에 대해 모두 실행
    # for j in range(100) :
    #     img = read_img(j)
    #     img_data, x, y = clustering_1(img)
    #     img_data, x, y = clustering_2(img_data, x, y)
    #     cluster_centers, p, hist, colors, hexlabels = clustering_3(img_data, x, y)
    #     index = p.index(max(p))
    #     cluster_centers_rgb = cluster_centers[:, 0:3]
    #     color_mapped, color_list = color_mapping('./color_matching_list.csv', cluster_centers_rgb)
    #     color_label = color_list[index]
    #     hex_labels = []
    #     for i in range(len(color_mapped)) :
    #         hex_labels.append(rgb_to_hex(color_mapped[i][0], color_mapped[i][1], color_mapped[i][2]))
    #     print(color_label)
    #     fig, ax = plt.subplots(2, 1, figsize=(5, 5))
    #     ax[0].pie(hist, labels = hexlabels, autopct = '%.1f%%', colors = colors)
    #     ax[0].set_title(f'{j} : Before'.format(j))
    #     ax[1].pie(p, labels = hex_labels, autopct = '%.1f%%', colors = hex_labels)
    #     ax[1].set_title(f'{j} : After'.format(j))
    #     plt.show()
    #     hexlabels = []
    #     colors = []
        
    #     #save_result(data, cluster_centers, p, i)
    #     #save_result(data, color_mapped, p, i)