# coding=utf-8
# 基于规则的推荐

# 主要有如下几个步骤：
# 1. 加载数据；
# 2. 根据推荐规则生成推荐结果；
# 3. 对推荐结果进行检验。
# 只需要修改rule.py里的getRecommendByRule函数就可以

from tmall import *
from user_rule import *


# 1. 加载数据
data = loadData()

# 2. 根据推荐规则生成推荐结果
recommend = getRecommendByRule(data)

# 3. 对推荐结果进行检验
printF1Score(recommend)


