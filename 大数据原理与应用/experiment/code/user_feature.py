# coding=utf-8
# 特征选取与计算

from copy import copy
from tmall import *
import math

# 引入时间衰减因子函数
def time_decay_factor(days_since_last_action, decay_rate=0.95):
    return decay_rate ** days_since_last_action

# 特征计算
# 基于逻辑回归的推荐需要划分训练集与预测集
# 将前2个月的交互划分为训练集 train
# 将后2个月的交互划分为
# 通过参数classify进行判断，不处理与当前类型不符合的数据。
def generateFeature(classify, data):
    F = {}

    item = {
        'click': 0,  # 点击次数
        'buy': 0,  # 购买次数
        'fav': 0,  # 加入收藏夹次数
        'cart': 0,  # 加入购物车次数
        'diff_day': 1000,  # 相差天数初始化
        'total_activity': 0,  # 活跃度
        'time_decay_click': 0,  # 点击时间衰减特征
        'time_decay_buy': 0,  # 购买时间衰减特征
        'time_decay_fav': 0,  # 收藏时间衰减特征
        'time_decay_cart': 0,  # 车时间衰减特征
    }

    feature_name = ['click', 'buy', 'fav', 'cart', 'diff_day', 'total_activity',
                    'time_decay_click', 'time_decay_buy', 'time_decay_fav', 'time_decay_cart']

    for uid, bid, action_type, month, day in data:
        if classify != getClassify(month, day):
            continue

        F.setdefault(uid, {})
        F[uid].setdefault(bid, copy(item))

        e = F[uid][bid]

        diff_day = getDiffDayByClass(classify, (month, day))
        if diff_day < e['diff_day']:
            e['diff_day'] = diff_day

        # 基础特征计算并引入时间衰减
        if action_type == 0:
            e['click'] += 1
            e['time_decay_click'] += time_decay_factor(diff_day)
        elif action_type == 1:
            e['buy'] += 1
            e['time_decay_buy'] += time_decay_factor(diff_day)
        elif action_type == 2:
            e['fav'] += 1
            e['time_decay_fav'] += time_decay_factor(diff_day)
        elif action_type == 3:
            e['cart'] += 1
            e['time_decay_cart'] += time_decay_factor(diff_day)

    # 综合得分计算，考虑时间衰减
    for uid, bid_list in F.items():
        for bid, e in bid_list.items():
            e['total_activity'] = (e['fav'] * e['time_decay_fav'] + e['cart'] * e['time_decay_cart'])

    return F, feature_name
