import math, random
import pandas as pd
from matplotlib import pyplot as plt
'''
Density-based scan
epsilon - радиус окрестности объекта
N - число соседей в окрестности для присвоения объекту статуса основного
Число кластеров определяется алгоритмом в ходе работы
'''
'''
Метрика = евклидово расстояние
'''
def DBSCAN(X, epsilon, N, target = None):
    '''Удаление таргета, если нужно'''
    if (target != None):
        X = X.drop(columns = [target])
    '''Заготовка под метки кластеров'''
    clusters = [None for i in range(0, X.shape[0])]
    major_objs, border_objs, noise_objs = [], [], []
    major_indexes, border_indexes, noise_indexes = [], [], []
    total_objects = [(list(X.iloc[i]),i) for i in range(0, X.shape[0])]
    def distance(sample_1, sample_2):
        return math.sqrt(sum(list(map(lambda x, y: (x-y)**2, sample_1[0], sample_2[0]))))
    def get_neighbours(sample):
        return [obj for obj in total_objects if obj != sample and distance(obj,sample) <= epsilon]
    def find_index(objects_array, index):
        for obj in objects_array:
            if (obj[1] == index):
                return True
        return False
    def deploy_cluster(obj, cluster_mark, processed_objects, noise_objs):
        objs = [obj]
        clusters[obj[1]] = cluster_mark
        while True:
            neighbours = []
            for obj_ in objs:
                neighbours += [o for o in get_neighbours(obj_) if o not in processed_objects and o not in noise_objs]
            if (len(neighbours) == 0):
                break
            for n in neighbours:
                processed_objects.append(n)
                clusters[n[1]] = cluster_mark
            objs = neighbours
        return processed_objects
    '''Классификация объектов на основные/пограничные/шумовые'''
    '''Выделение основных'''
    for sample_index, sample in enumerate(total_objects):
        neighbours = get_neighbours(sample)
        if (len(neighbours) >= N):
            major_objs.append(sample)
            major_indexes.append(sample_index)
    '''Выделение пограничных и шумовых объектов'''
    for sample_index, sample in enumerate(total_objects):
        border = False
        if (major_indexes.count(sample_index) == 0):
            neighbours = get_neighbours(sample)
            for index in major_indexes:
                if (find_index(neighbours, index) == True and border == False):
                    border_objs.append(sample)
                    border_indexes.append(sample_index)
                    border = True
            if (border == False):
                noise_objs.append(sample)
                noise_indexes.append(sample_index)
    '''Выделение связных компонент на основных объектах'''
    processed_objects = []
    cluster_mark = 0
    for obj in major_objs:
        if (obj in processed_objects):
            continue
        processed_objects.append(obj)
        while (cluster_mark in clusters):
            cluster_mark += 1
        processed_objects = deploy_cluster(obj, cluster_mark, processed_objects, noise_objs)
    '''Присоединение граничных точек к компонентам'''
    for obj in border_objs:
        neighbours = get_neighbours(obj)
        for n in neighbours:
            if (major_objs.count(n) != 0):
                clusters[obj[1]] = clusters[n[1]]
    check_sum = (clusters.count(0) + clusters.count(1) + clusters.count(2) + clusters.count(None))
    print(check_sum)
    print(len(clusters))
    if (check_sum != len(clusters)):
        print(clusters)
    return clusters
'''Сгенерируем случайную выборку для трёх кластеров на плоскости'''
center_1, center_2, center_3 = [1,1], [5,20], [33, 10]
x_1 = [center_1[0] + random.randint(-5,5) for i in range(0,25)]
x_2 = [center_2[0] + random.randint(-7,7) for i in range(0,30)]
x_3 = [center_3[0] + random.randint(-9,9) for i in range(0,28)]

y_1 = [center_1[1] + random.randint(-5,5) for i in range(0,25)]
y_2 = [center_2[1] + random.randint(-7,7) for i in range(0,30)]
y_3 = [center_3[1] + random.randint(-9,9) for i in range(0,28)]

x = x_1 + x_2 + x_3
y = y_1 + y_2 + y_3

# Без кластеризации:
#fig, axes = plt.subplots()
#axes.scatter(x, y, color = 'grey')

test_df = pd.DataFrame({'x': x, 'y':y})
clusters_marks = DBSCAN(X = test_df, epsilon = 5.2, N = 4)
x1, x2, x3, x_noise = [], [], [], []
y1, y2, y3, y_noise = [], [], [], []
for index, mark in enumerate(clusters_marks):
    if (mark == 0):
        x1.append(x[index])
        y1.append(y[index])
    elif (mark == 1):
        x2.append(x[index])
        y2.append(y[index])
    elif (mark == 2):
        x3.append(x[index])
        y3.append(y[index])
    elif (mark == None):
        x_noise.append(x[index])
        y_noise.append(y[index])

# С кластеризацией:
fig1, axes1 = plt.subplots()
axes1.scatter(x1, y1, c = 'blue')
axes1.scatter(x2, y2, c = 'red')
axes1.scatter(x3, y3, c = 'green')
axes1.scatter(x_noise, y_noise, c = 'lightgrey')
                
    
    