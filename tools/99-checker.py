# coding:utf-8

import pandas as pd
import json
from pandas import json_normalize
import re

p1 = re.compile('^\'+')
p2 = re.compile('\'+$')

df = pd.read_table('../output/Pentiment-BetterJP - out.tsv')
df = df.query('Duplicate.isnull()')

da = pd.read_table('../output/Pentiment-machinecorrect.tsv')
da = da.query('MachineCorrect.notnull()')


machine_translation = {}

for index, row in da.iterrows():
	if pd.notnull(row["MachineCorrect"]): #自動翻訳がある場合は利用
		machine_translation[row["Name"]+","+str(row["ID"])] = row["MachineCorrect"]

n = 0

print("# changes")

for index, row in df.iterrows():	
	if (row["Name"]+","+str(row["ID"])) in machine_translation:#機械翻訳がある
#		print("AA")
		if (pd.notnull(row["BetterJP"])): #手動訳もある
			if( machine_translation[row["Name"]+","+str(row["ID"])] != row["BetterJP"]): #両者が違う
				print("#"+str(row["N"]))
				print(machine_translation[row["Name"]+","+str(row["ID"])])
				print(row["BetterJP"])

print()
print("# same w/machine translation")

for index, row in df.iterrows():	
	if (row["Name"]+","+str(row["ID"])) in machine_translation:#機械翻訳がある
		if (pd.notnull(row["BetterJP"])): #手動訳もある
			if( machine_translation[row["Name"]+","+str(row["ID"])] == row["BetterJP"]): #両者が同じ
				print("#"+str(row["N"]))
				print(row["BetterJP"])


print()
print("# same w/original")

for index, row in df.iterrows():	
	if (pd.notnull(row["BetterJP"])): #手動訳がある
		if(row["Japanese"] == row["BetterJP"]): #もとと同じ
			print("#"+str(row["N"]))
			print(row["BetterJP"])


