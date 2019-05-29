############ ! /usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np 
import pandas as pd
#读取数据
rawdata = []
file_path = "/Users/Ekko/Desktop/python/rawdata/data/201501/2015010104.raw"

rawData = open(file_path,'rb').read()
# print(rawData)

for ind,raw in enumerate(rawData):
	# if(ind>1000): break
	hexstr =  "%s" % raw.encode('hex')

	# rawdata.append(int(hexstr, 16))
	rawdata.append(hexstr)
# print(rawdata)


def HeaderOrNot(ind, vec):
	L = len(vec)
	if (L - ind < 5):
		return(False)
	else:
		if(vec[ind] == 'aa' and vec[ind+1] == '44' and vec[ind+2] == '12'and vec[ind+3] == '1c'):
			return(True)
		else:
			return(False)

vec_tmp = []
group_dic = {}
start, end = 0, 0
header = ""
# tranverse
for ind, ele in enumerate(rawdata):
	boolhead = HeaderOrNot(ind, rawdata)
	if boolhead == True:
		if len(vec_tmp) > 0:
			if header in group_dic.keys():
				group_dic[header].append(vec_tmp)
			else:
				group_dic[header] = [vec_tmp]
			vec_tmp = []
		header = rawdata[ind+4] + rawdata[ind+5]
	vec_tmp.append(ele)
if header in group_dic.keys():
	group_dic[header].append(vec_tmp)
else:
	group_dic[header] = [vec_tmp]

# print(group_dic.keys())
for key in group_dic.keys():
	print(key, len(group_dic[key]))
# print(group_dic)

for l in group_dic['0700']:
	print(l)