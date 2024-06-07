#coding=utf-8
# 基于逻辑回归的推荐

# 主要有如下几个步骤：
# 1. 加载数据；
# 2. 生成特征；
# 3. 对训练集进行训练，建立推荐模型；
# 4. 将模型应用于验证集，生成推荐结果；
# 5. 对推荐结果进行检验；

from tmall import *
from user_feature import *


# 1. 加载数据
data = loadData()

# 2. 生成训练集特征
feature, feature_name = generateFeature('train', data)

# 3. 对训练集进行训练，建立推荐模型
model = getModelByLogistic(feature, feature_name)

# 4. 生成预测集特征
feature, feature_name = generateFeature('predict', data)

# 5. 将模型应用于验证集，生成推荐结果
recommend = getRecommendByLogistic(model, feature, feature_name)

# 6. 对推荐结果进行检验
printF1Score(recommend)
