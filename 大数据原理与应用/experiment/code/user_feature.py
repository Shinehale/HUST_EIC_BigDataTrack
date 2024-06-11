# coding=utf-8
# 特征选取与计算

from copy import copy
from tmall import *

# 特征计算
# 基于逻辑回归的推荐需要划分训练集与预测集
# 将前2个月的交互划分为训练集 train
# 将后2个月的交互划分为
# 通过参数classify进行判断，不处理与当前类型不符合的数据。
def generateFeature(classify, data):
    F = {}
    user_brand_interaction = {}

    item = {
        'click': 0,  # 点击次数
        'buy': 0,  # 购买次数
        'fav': 0,  # 加入收藏夹次数
        'cart': 0,  # 加入购物车次数
        'diff_day': 1000,  # 相差天数初始化
        'click_decay': 0,  # 点击时间衰减特征
        'buy_decay': 0,  # 购买时间衰减特征
        'fav_decay': 0,  # 收藏时间衰减特征
        'cart_decay': 0,  # 加入购物车时间衰减特征
        'interaction_frequency': 0,  # 用户与品牌的交互频率
        'historical_activity': 0,  # 用户历史活跃度
    }
    


    feature_names = ['click', 'buy', 'fav', 'cart', 'diff_day', 'click_decay',
                     'buy_decay', 'fav_decay', 'cart_decay', 'interaction_frequency', 'historical_activity']

    for uid, bid, action_type, month, day in data:
        if classify != getClassify(month, day):
            continue

        F.setdefault(uid, {})
        F[uid].setdefault(bid, copy(item))
        user_brand_interaction.setdefault(uid, set()).add(bid)

        e = F[uid][bid]

        diff_day = getDiffDayByClass(classify, (month, day))
        if diff_day < e['diff_day']:
            e['diff_day'] = diff_day

        # 基础特征计算并引入时间衰减
        delay = (1.0 / (1 + diff_day)) 
        if action_type == 0:
            e['click'] += 1
            e['click_decay'] += delay
        elif action_type == 1:
            e['buy'] += 1
            e['buy_decay'] += delay
        elif action_type == 2:
            e['fav'] += 1
            e['fav_decay'] += delay
        elif action_type == 3:
            e['cart'] += 1
            e['cart_decay'] += delay

    # 计算额外的特征
    for uid, bid_list in F.items():
        for bid, e in bid_list.items():
            e['interaction_frequency'] = len(user_brand_interaction[uid])
            e['historical_activity'] = e['click'] + e['buy'] + e['fav'] + e['cart']

    return F, feature_names