# coding=utf-8
#
# 定义通用函数
# 

import time
import datetime

import numpy as np
import pandas as pd
import statsmodels.api as sm

import sys
sys.dont_write_bytecode = True

import warnings
warnings.filterwarnings("ignore")


# 加载数据
def loadData():
	f = open("./data/data.csv", "r")
	data = []

	line = f.readline()
	while line:
		user_id, brand_id, action_type, month, day = line.strip().split(',')

		# 转换格式
		action_type = int(action_type)
		month = int(month)
		day = int(day)

		data.append( (user_id, brand_id, action_type, month, day) )
		line = f.readline()

	f.close()
	return data


# 对推荐进行检验
def printF1Score(recommend):

	predict_num = 0
	hit_num = 0
	brand = 0

	# 读取实际的购买情况
	f = open("./data/result.txt", "r")
	result = {}
	lines = f.readlines()
	for index, item in enumerate(lines):
		uid, bid = item.strip("\n").split("\t")
		result[uid] = set(bid.split(","))
		brand += len(result[uid])
	f.close()

	# 调整预测结果格式
	R = {}
	for uid, bid in recommend:
		R.setdefault(uid, [])
		if bid not in R[uid]:
			R[uid].append(bid)

	# 计算推荐数量以及命中数量
	for uid, bid_list in R.items():
		predict_num += len(bid_list)

		if uid in result:
			for bid in bid_list:
				if bid in result[uid]:
					hit_num += 1

	# 输出结果
	print ("执行时间:\t %s" % datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))
	print ("预测总数:\t %d" % predict_num)
	print ("命中数量:\t %d" % hit_num)
	
	if brand == 0 or hit_num == 0:
	 	print ("F1得分:\t 0")
	else:
		precision = float(hit_num)/predict_num
		recall = float(hit_num)/brand
		print ("精确度:\t %.2f%%" % round(100*precision, 2))
		print ("召回率:\t %.2f%%" % round(100*recall, 2))

		print ("F1得分:\t %.2f%%" % round(100*2*precision*recall/(precision+recall), 2))
		

# 返回两个日期相差的天数(d2-d1)
def getDiffDay(d1, d2):
	d1 = datetime.date(2013, d1[0], d1[1])
	d2 = datetime.date(2013, d2[0], d2[1])
	day = (d2-d1).days
	return day


# 针对训练集或预测集，返回两个日期相差的天数(d2-d1)
def getDiffDayByClass(c, d1):
	if c == 'train':
		d2 = (6, 15)
	else:
		d2 = (7, 15)

	d1 = datetime.date(2013, d1[0], d1[1])
	d2 = datetime.date(2013, d2[0], d2[1])
	day = (d2-d1).days
	return day


# 判断数据属于训练集或者预测集
def getClassify(month, day):
	if month == 4 or month == 5 or (month == 6 and day < 15):
		return 'train'
	elif month == 6 or month == 7 or (month == 5 and day >= 15):
		return 'predict'


# 获取逻辑回归模型
def getModelByLogistic(feature, feature_name):
	# 将训练集的特征加上标志位
	
	# 读取6月份的购买情况
	f = open("./data/buy-in-6.txt", "r")
	buy = {}
	lines = f.readlines()
	for index, item in enumerate(lines):
		uid, bid = item.strip("\n").split("\t")
		buy[uid] = set(bid.split(","))
	f.close()

	# 将训练集写入到文件中
	f = open("./data/train.txt", "w")
	column_name = 'uid,bid,flag,'+','.join(feature_name)
	f.write(column_name + '\n')

	for uid, bid_list in feature.items():
		for bid, e in bid_list.items():
			# 这边的属性需要都转为str类型
			item = [str(uid), str(bid)]
			if uid in buy and bid in buy[uid]:
				item.append(str(1))
			else:
				item.append(str(0))

			for x in feature_name:
				item.append(str(e[x]))

			f.write(','.join(item) + '\n')

	f.close()

	# 开始执行训练
	train = pd.read_csv("./data/train.txt")
	train_data = train[feature_name]
	train_data['intercept'] = 1.0

	logit = sm.Logit(train['flag'], train_data)
	model = logit.fit()

	return model


# 根据模型获取推荐结果
def getRecommendByLogistic(model, feature, feature_name):

	# 将预测集写入到文件中
	f = open("./data/predict.txt", "w")
	column_name = 'uid,bid,'+','.join(feature_name)
	f.write(column_name + '\n')

	for uid, bid_list in feature.items():
		for bid, e in bid_list.items():
			# 这边的属性需要都转为str类型
			item = [str(uid), str(bid)]

			for x in feature_name:
				item.append(str(e[x]))

			f.write(','.join(item) + '\n')

	f.close()

	predict = pd.read_csv("./data/predict.txt")
	predict_data = predict[feature_name]
	predict_data['intercept'] = 1.0
	predict['flag'] = model.predict(predict_data)

	# 对预测分数进行排序
	pick = []
	for term in predict.values:
		uid, bid, flag = str(int(term[0])), str(int(term[1])), term[-1]
		pick.append((uid, bid ,flag))

	pick.sort(key = lambda x:x[2], reverse = True)

	# 取前1400个作为推荐
	recommend = []
	for item in pick[0:1400]:
		recommend.append( (item[0], item[1]) )


	# print ("\n所使用的特征: ", feature_name)

	return recommend
