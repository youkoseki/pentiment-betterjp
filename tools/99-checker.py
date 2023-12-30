# coding:utf-8

import pandas as pd
import json
from pandas import json_normalize
import re

p1 = re.compile('^\'+')
p2 = re.compile('\'+$')

df = pd.read_table('../output/Pentiment-BetterJP - out.tsv')

da = pd.read_table('../output/Pentiment-machinecorrect.tsv')
da = da.query('MachineCorrect.notnull()')


machine_translation = {}

for index, row in da.iterrows():
	if pd.notnull(row["MachineCorrect"]): #自動翻訳がある場合は利用
		machine_translation[row["Name"]+","+str(row["ID"])] = row["MachineCorrect"]

n = 0

for index, row in df.iterrows():
	if pd.notnull(row["Duplicate"]): #重複の場合は無視
		continue
	elif row["Japanese"] == row["BetterJP"]:#旧訳と新約が同じならスキップ
		continue
	
	if (row["Name"]+","+str(row["ID"])) in machine_translation:#機械翻訳がある
#		print("AA")
		if (pd.notnull(row["BetterJP"])): #手動訳もある
			print("#"+str(row["N"]))
			print(machine_translation[row["Name"]+","+str(row["ID"])])
			print(row["BetterJP"])



