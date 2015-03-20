import numpy as np
import pandas as pd
from pandas import *
import re

#open data files, including prevelence file created from screenshot of
#pdf provided.  Files must be named as they are below and
#in a directory named "data".
findings = open('data/Findings_for_2015_decision_support_exercise_v03.txt')
diseases = open('data/Diseases_for_2015_decision_support_exercise_v03.txt')
prevelence = open('data/prevalence_decision_support_2015.txt')

#create empty dicts for symptom mapping and import/type info
sx_map = {}
IM_TY = {}
for line in findings: #parse file by line
	#strip any trailing charaters from each line
	line = line.rstrip('\r\n')
	#use regex to match lines with 'MX' at start
	if (re.match('MX', line)):
		#split line by default (whitespace), limit splits to 2
		#save split line in array "line_split"
		line_list = line.split(None, 2)
		#create key-value pair in sx_map using
		#elements 1 and 2 of line_split
		sx_map[line_list[1]] = line_list[2]
	else:   #all other lines split to create import\type dict
		line_list = line.split(None, 4)
		IM_TY[line_list[0]] = {line_list[1]:line_list[2],
			line_list[3]:line_list[4]}

#save strategy as above, used lists of dicts for ppv and sens		
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
				'dx':dz_set,
				'mx':line_list[2],
				'ppv':list(line_list[1])[0],
				'sens':list(line_list[1])[1]
				}
				)
	elif (re.match('LINK', line)):
		line_list = line.split(None, 4)
		dz_lk.append(
				{
				'dx':dz_set,
				'LINK':line_list[3],
				'LINK_t':line_list[1],
				'ppv':list(line_list[2])[0],
				'sens':list(line_list[2])[1]
				}
				)
		dz_map[line_list[3]] = line_list[4]

dz_pv = {}
for line in prevelence:
	line = line.rstrip('\r\n')
	line_list = line.split(None, 2)
	dz_pv[line_list[1]] = line_list[0]
	

#close data files
findings.close()
diseases.close()
prevelence.close()


#create data frames from dicts and lists created above
IM_TY_df = DataFrame(IM_TY)
#sx_map_df = DataFrame(sx_map.items(), columns=['mx_code', 'mx_def'])
sx_map_df = DataFrame(sx_map.values(),index=sx_map.keys(), columns=['mx'])
dz_mx_df = DataFrame(dz_mx)
dz_lk_df = DataFrame(dz_lk)
#dz_map_df = DataFrame(dz_map.items(), columns=['dx_code', 'dx_def])
dz_map_df = DataFrame(dz_map.values(),index=dz_map.keys(), columns=['dx'])
dz_pv_df = DataFrame(dz_pv.values(),index=dz_pv.keys(), columns=['pv'])

#script that prints all dataframe name and first 5 rows
data = [dz_map_df, dz_lk_df, dz_mx_df, sx_map_df, IM_TY_df.T, dz_pv_df]
data_names = ["dz_map_df", "dz_lk_df", "dz_mx_df", "sx_map_df", "IM_TY_df", "dz_pv_df"]

count = 0

for i in data:
	print "Dataframe:", data_names[count]
	count += 1
	print i[:5]
	print '\n'

