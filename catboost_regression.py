import pandas as pd
from catboost import CatBoostRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import LabelEncoder
import numpy as np
import shap

# 1. 读取数据
data = pd.read_csv('regression_data.csv')  # 替换为你的文件名

# 2. 划分特征和目标变量
X = data[['wind','typhoon', 'rainfall',  'distance', 'highwayden', 'transport', 'GDP', 'urban', 'popout', 'car', 'search']]
y = data['realtravelres']  # 因变量

# 3. 计算相关性矩阵
correlation_matrix = X.corr().abs()


# 4. 筛选高共线性特征
threshold = 0.7
to_drop = set()
for i in range(len(correlation_matrix.columns)):
    for j in range(i):
        if abs(correlation_matrix.iloc[i, j]) > threshold:  # 高于阈值
            colname = correlation_matrix.columns[i]
            to_drop.add(colname)

# 保留7个特征
to_keep = list(set(X.columns) - to_drop)

# 确保至少保留7个特征
selected_features = to_keep[:7] if len(to_keep) >= 7 else to_keep

X = X[selected_features]

# 5. 拆分训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 6. 创建 CatBoost 回归模型
model = CatBoostRegressor(iterations=1000, depth=6, learning_rate=0.1, loss_function='RMSE', verbose=100)

# 7. 训练模型
model.fit(X_train, y_train, eval_set=(X_test, y_test))

# 8. 预测
predictions = model.predict(X_test)

# 9. 评估模型
mse = mean_squared_error(y_test, predictions)
r_squared = r2_score(y_test, predictions)

# 防止除以零
if X_test.shape[1] > 1:
    adjusted_r_squared = 1 - (1 - r_squared) * (len(y_test) - 1) / (len(y_test) - X_test.shape[1] - 1)
else:
    adjusted_r_squared = np.nan  # 如果没有特征则设置为NaN

print(f'Mean Squared Error: {mse}')
print(f'R²: {r_squared}')

# 10. 计算 SHAP 值
explainer = shap.Explainer(model)
shap_values = explainer(X_test)

# 11. 可视化 SHAP 值
shap.summary_plot(shap_values, X_test)
