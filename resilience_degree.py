import pandas as pd
import networkx as nx

# 读取数据
data = pd.read_csv('Reallink_typhoon.csv')

# 确保 data 成功加载为 DataFrame
if not isinstance(data, pd.DataFrame):
    raise TypeError("数据未成功加载为 DataFrame，请检查 CSV 文件。")

# 权重列
weight_columns = ['Baseline', 'MPR', 'MI', 'MPO']

# 初始化结果存储 DataFrame
result_df = pd.DataFrame()

# 遍历每个权重列，分别计算加权度中心性和加权聚类系数
for weight_column in weight_columns:
    # 创建无向图
    G = nx.Graph()

    # 添加边并累加相反方向边的权重
    for _, row in data.iterrows():
        start = row['StartCity']
        end = row['EndCity']
        weight = row[weight_column]

        # 如果边已经存在（无向图），累加权重
        if G.has_edge(start, end):
            G[start][end]['weight'] += weight
        else:
            G.add_edge(start, end, weight=weight)

    # 计算加权度中心性
    weighted_degree_centrality = {
        node: sum(data['weight'] for _, _, data in G.edges(node, data=True))
        for node in G.nodes
    }

    # 计算加权聚类系数
    weighted_clustering = nx.clustering(G, weight='weight')

    # 将结果存入临时 DataFrame
    temp_df = pd.DataFrame({
        'City': list(G.nodes),
        f'{weight_column}_Weighted_Degree_Centrality': [weighted_degree_centrality.get(node, 0) for node in G.nodes],
        f'{weight_column}_Weighted_Clustering_Coefficient': [weighted_clustering.get(node, 0) for node in G.nodes]
    })

    # 合并结果到最终 DataFrame
    if result_df.empty:
        result_df = temp_df
    else:
        result_df = pd.merge(result_df, temp_df, on='City', how='outer')

# 保存最终结果到 CSV 文件
result_df.to_csv('weighted_degree_clustering_undirected.csv', index=False, encoding='utf-8')

print("加权度中心性和加权聚类系数计算完成，结果已保存到 'weighted_degree_clustering_undirected.csv'")
