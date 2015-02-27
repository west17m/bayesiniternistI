import numpy as np
import pandas as pd
from pandas import *
import re

findings = open('data/Findings_for_2015_decision_support_exercise_v03.txt')
diseases = open('data/Diseases_for_2015_decision_support_exercise_v03.txt')

sx_map = {} 
IM_TY = {}
for line in findings:
	line = line.rstrip('\r\n')
	if (re.match('MX', line)):
		line_list = line.split(None, 2)
		sx_map[line_list[1]] = line_list[2]
	else:
		line_list = line.split(None, 4)
		IM_TY[line_list[0]] = {line_list[1]:line_list[2],
			line_list[3]:line_list[4]}
dz_map = {}
dz_mx = []
dz_lk = []
for line in diseases:
	line = line.rstrip('\r\n')
	if (re.match('DX', line)):
		line_list = line.split(None, 2)
		dz_map[line_list[1]] = line_list[2]
		dz_set = line_list[1]
	elif (re.match('MX', line)):
		line_list = line.split(None, 3)
		dz_mx.append(
				{
				'DX':dz_set,
				'MX':line_list[2],
				'PPV':list(line_list[1])[0],
				'NPV':list(line_list[1])[1]
				}
				)
	elif (re.match('LINK', line)):
		line_list = line.split(None, 4)
		dz_lk.append(
				{
				'DX':dz_set,
				'LINK':line_list[3],
				'LINK_t':line_list[1],
				'PPV':list(line_list[2])[0],
				'NPV':list(line_list[2])[1]
				}
				)
		dz_map[line_list[3]] = line_list[4]

findings.close()
diseases.close()

IM_TY_df = DataFrame(IM_TY)
#print IM_TY_df.T.loc['391']
#sx_map_df = DataFrame(sx_map.items(), columns=['mx_code', 'mx_def']) 
sx_map_df = DataFrame(sx_map.values(),index=sx_map.keys(), columns=['mx']) 
#print sx_map_df.loc['190']
dz_mx_df = DataFrame(dz_mx)
#print dz_mx_df
dz_lk_df = DataFrame(dz_lk)
#print dz_lk_df
#dz_map_df = DataFrame(dz_map.items(), columns=['dx_code', 'dx_def])
dz_map_df = DataFrame(dz_map.values(),index=dz_map.keys(), columns=['dx'])
#print dz_map_df.loc['60']
