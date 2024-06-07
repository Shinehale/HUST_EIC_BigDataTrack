# coding=utf-8
# 自定义的推荐规则

from copy import copy
from tmall import getDiffDay


# 推荐规则
# 函数可分为两部分
# 1. 计算用户特征
# 2. 根据规则进行筛选
#
# 参数 data: 数组，数组元素为 (user_id, brand_id, action_type, month, day)
# 返回值 R : 数组，数组元素为 (user_id, brand_id)
def getRecommendByRule(data):
	# 设置推荐阈值，这个值可能需要根据实验结果进行调整
	threshold = 0.5
	F = {}		# 存储用户特征
	R = []		# 存储推荐结果

	# 所有要进行统计的特征，在这里进行声明并赋予初始值
	item = {
		'click': 0,		# 点击次数
		'buy': 0,		# 购买次数
		'fav': 0,		# 加入收藏夹次数
		'cart': 0,		# 加入购物车次数
		'diff_day': 1000,	# 因为是要推测下一个月的购买情况
				# 显然在最近一段时间有交互的，购买可能性越大
				# 因此将最后一次交互的相差天数也作为一个特征
				# 如我们推测7月15-8月15这一个月的购买情况，用户在7月8号跟7月12号均有交互记录
				# 则diff_day为3（取最近的7月12，计算跟7月15的相差天数）
		'total_activity': 0,  # 用户活跃度，总活动次数
	}


	# 1. 计算用户特征
	for uid, bid, action_type, month, day in data:
		# 初始化
		F.setdefault(uid, {})
		F[uid].setdefault(bid, copy(item))

		# 新建一个引用，简化代码
		e = F[uid][bid]

		# 基础特征计算
		if action_type == 0:
			e['click'] += 1
			e['total_activity'] += 0.4  # 用户对该商品的活跃度
		elif action_type == 1:
			e['buy'] += 1
			e['total_activity'] += 3.5
		elif action_type == 2:
			e['fav'] += 1
			e['total_activity'] += 1.5
		elif action_type == 3:
			e['cart'] += 1
			e['total_activity'] += 2.5

		# 时间特征
		diff_day = getDiffDay((month, day), (7, 15))
		if diff_day < e['diff_day']:
			e['diff_day'] = diff_day


	# 2. 根据特征进行筛选
	for uid, bid_list in F.items():
		for bid, e in bid_list.items():
			# 综合得分计算，可以根据需要调整各项的权
			score = (e['click'] * 0.4 + e['buy'] * 3.5 + e['fav'] * 1.5 + e['cart'] * 2.5) * (1 / (e['diff_day'] + 1))
			# 综合得分高于某个阈值，并且diff_day小于30，并且用户活跃度大于1.5
			if score > threshold and e['diff_day'] < 30 and e['total_activity']>1.5:
				R.append((uid, bid))

	return R
