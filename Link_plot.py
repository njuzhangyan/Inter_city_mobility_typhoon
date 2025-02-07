import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.colors import ListedColormap
from matplotlib.path import Path
import matplotlib.patches as patches
import numpy as np

# 设置全局字体为Arial
plt.rcParams['font.family'] = 'Arial'

# 读取CSV数据
data = pd.read_csv('Link_index.csv')

# 读取shapefile文件
shp1 = gpd.read_file('shp/shibianjie.shp').to_crs('EPSG:4326')

# 创建NetworkX图 (无方向)
G = nx.Graph()

# 计算 MPR_B 和 Baseline 的比值，并添加边及属性
for _, row in data.iterrows():
    ratio = row['MPO_B'] / row['Baseline']
    G.add_edge(
        (row['start_lon'], row['start_lat']),
        (row['end_lon'], row['end_lat']),
        weight=ratio
    )

# 定义分级函数
def classify_ratio(value):
    if value < -0.4:
        return 1
    elif value < -0.3:
        return 2
    elif value < -0.2:
        return 3
    elif value < -0.1:
        return 4
    elif value < 0:
        return 5
    elif value < 0.1:
        return 6
    elif value < 0.2:
        return 7
    elif value < 0.3:
        return 8
    elif value < 0.4:
        return 9
    else:
        return 10

# 定义每个等级的颜色和线条粗细
edge_colors = {
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

edge_widths = {
    1: 6, 2: 5, 3: 3.5, 4: 3.0, 5: 2.5,
    6: 2.5, 7: 3.0, 8: 3.5, 9: 5, 10: 6
}

# 绘制简单的弧线
def draw_simple_curve(G, pos, ax, level, edge_list, edge_color, edge_width):
    for u, v in edge_list:
        x0, y0 = pos[u]
        x1, y1 = pos[v]

        # 计算简单的弧形控制点
        mid_x, mid_y = (x0 + x1) / 2, (y0 + y1) / 2
        offset = 0.05  # 控制弧度大小
        rotation = np.arctan2(y1 - y0, x1 - x0) + np.pi / 2
        control_x = mid_x + offset * np.cos(rotation)
        control_y = mid_y + offset * np.sin(rotation)

        # 创建单向弧线的 Path
        path_data = [
            (Path.MOVETO, (x0, y0)),
            (Path.CURVE3, (control_x, control_y)),
            (Path.CURVE3, (x1, y1))
        ]
        path = Path([p[1] for p in path_data], [p[0] for p in path_data])
        patch = patches.PathPatch(path, color=edge_color, linewidth=edge_width)  # 去掉透明度
        ax.add_patch(patch)

# 设置绘图参数
fig, ax = plt.subplots(figsize=(10, 10))
shp1.boundary.plot(ax=ax, linewidth=1, color='black')

# 获取节点位置
pos = {node: node for node in G.nodes()}

# 按等级从低到高分层绘制简单弧形边
# for level in range(10,0,-1):
for level in range(1, 11):
    edges = [(u, v) for u, v, d in G.edges(data=True) if classify_ratio(d['weight']) == level]
    color = edge_colors[level]
    width = edge_widths[level]

    # 绘制简单的弧形边
    draw_simple_curve(G, pos, ax, level, edges, color, width)

# 添加图例并自定义大小、标签和字号
cmap = ListedColormap([edge_colors[i] for i in range(1, 11)])
sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin=-0.5, vmax=0.5))
sm.set_array([])

# 定制图例
cbar = plt.colorbar(sm, ax=ax, ticks=np.linspace(-0.5, 0.5, 11))
cbar.ax.tick_params(labelsize=26)  # 设置图例刻度的字号大小
cbar.set_label('P(mpo)-Bl / Bl', fontsize=28)  # 设置图例标签字号
cbar.ax.set_yticklabels([f'{x:.1f}' for x in np.linspace(-0.5, 0.5, 11)])  # 自定义标签格式

# 设置标题和其他字体大小
title = "MPO of Contact Strength "
plt.title(title, fontsize=28)

plt.xticks(fontsize=24)  # x轴刻度字号
plt.yticks(fontsize=24)  # y轴刻度字号

# 设置经度区间从 110 到 130 度，纬度区间从 20 到 50 度
ax.set_xlim(114.5, 123)
ax.set_ylim(26.5, 36)

# 设置经纬度刻度
x_ticks = np.arange(115, 124, 2)  # 经度每4度一个
y_ticks = np.arange(27, 36, 2)    # 纬度每4度一个

ax.set_xticks(x_ticks)
ax.set_yticks(y_ticks)

# 设置 x 和 y 轴刻度标签，旋转 x 轴刻度并减小字体大小
ax.set_xticklabels([f"{tick}°E" for tick in x_ticks], fontsize=22, rotation=45)
ax.set_yticklabels([f"{tick}°N" for tick in y_ticks], fontsize=22)

# 保存图片，文件名为标题
plt.savefig(f"{title}.png", bbox_inches='tight', dpi=300)

plt.show()
