import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.colors import ListedColormap
import numpy as np

# 设置全局字体为Arial
plt.rcParams['font.family'] = 'Arial'

# 读取CSV数据
node_data = pd.read_csv('node_index.csv')  # 替换为您节点数据的文件路径

# 读取shapefile文件
shp1 = gpd.read_file('shp/shibianjie.shp').to_crs('EPSG:4326')

# 创建 NetworkX 图 (无方向)
G = nx.Graph()

# 创建一个从节点数据中获取位置和属性的字典
node_pos = {}
for _, row in node_data.iterrows():
    G.add_node(row['City'], pos=(row['lon'], row['lat']), MPR_DC=row['MI_DC'])

# 定义分级函数
def classify_ratio(value):
    if value < -0.3:
        return 1
    elif value < -0.2:
        return 2
    elif value < -0.1:
        return 3
    elif value < -0.05:
        return 4
    elif value < 0:
        return 5
    elif value < 0.05:
        return 6
    elif value < 0.1:
        return 7
    elif value < 0.2:
        return 8
    elif value < 0.3:
        return 9
    else:
        return 10

# 定义每个等级的颜色
node_colors = {
    1: '#ab5663',  # 深红色
    2: '#d18087',  # 较深的红色
    3: '#fbb7b7',  # 亮红色
    4: '#fbccc8',  # 鲜红色
    5: '#fddad3',  # 浅粉红色
    6: '#b2f0e8',  # 浅绿色
    7: '#8de5db',  # 浅青绿色
    8: '#2fc4b2',  # 亮绿色
    9: '#289c8e',  # 较深的绿色
    10: '#117c6f'  # 深绿色
}

node_size_levels = {
    1: 6, 2: 5, 3: 3.5, 4: 3.0, 5: 2.5,
    6: 2.5, 7: 3.0, 8: 3.5, 9: 5, 10: 6
}

# 为每个节点设置颜色和大小
node_color_map = {}
node_size_map = []
for node, data in G.nodes(data=True):
    MPR_DC = data['MPR_DC']
    level = classify_ratio(MPR_DC)
    node_color_map[node] = node_colors[level]
    node_size_map.append(node_size_levels[level] * 150)  # 放大节点大小


# 设置节点大小（根据MPR_DC值的绝对值大小）
#node_sizes = {node: abs(data['MPR_DC']) * 1400 for node, data in G.nodes(data=True)}  # 使用绝对值，这里MPR不改

# 绘图设置
fig, ax = plt.subplots(figsize=(10, 10))
shp1.boundary.plot(ax=ax, linewidth=1, color='black')

# 获取节点位置
pos = nx.get_node_attributes(G, 'pos')

# 绘制节点
nx.draw_networkx_nodes(G, pos, node_size=node_size_map, node_color=list(node_color_map.values()), alpha=0.9, ax=ax)

# 定制图例并手动设置刻度值
cmap = ListedColormap([node_colors[i] for i in range(1, 11)])
sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin=-3, vmax=3))  # 根据分级设置刻度范围
sm.set_array([])

# 手动设置图例刻度和标签
cbar = plt.colorbar(sm, ax=ax, ticks=np.linspace(-3, 3, 11))  # 自定义刻度
cbar.ax.tick_params(labelsize=26)  # 设置图例刻度的字号大小
cbar.set_label('MI_DC', fontsize=26)  # 设置图例标签的字体大小

# 设置自定义的图例标签
cbar.ax.set_yticklabels([
    '-1', '-0.30', '-0.20', '-0.10', '-0.05', '0', '0.05', '0.10', '0.20', '0.30', '1'
])

# 设置标题和其他字体大小
title = "MI of Degree Centrality"
plt.title(title, fontsize=28)

# 设置坐标轴字体大小
plt.xticks(fontsize=24)
plt.yticks(fontsize=24)

# 设置经度区间从 110 到 130 度，纬度区间从 20 到 50 度
ax.set_xlim(114.5, 123)
ax.set_ylim(26.5, 36)

# 设置经纬度刻度
x_ticks = np.arange(115, 124, 2)  # 经度每2度一个
y_ticks = np.arange(27, 36, 2)    # 纬度每2度一个

ax.set_xticks(x_ticks)
ax.set_yticks(y_ticks)

# 确保显示坐标轴刻度标签
ax.set_xticklabels([f"{tick}°E" for tick in x_ticks], fontsize=22, rotation=45)
ax.set_yticklabels([f"{tick}°N" for tick in y_ticks], fontsize=22)

# 显示经纬度刻度
ax.tick_params(axis='x', which='both', bottom=True, top=False, labelbottom=True)
ax.tick_params(axis='y', which='both', left=True, right=False, labelleft=True)

# 保存图片，文件名为标题
plt.savefig(f"{title}.png", bbox_inches='tight', dpi=300)

plt.show()
