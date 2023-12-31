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
Japanese = {}

for index, row in da.iterrows():
	if pd.notnull(row["MachineCorrect"]): #自動翻訳がある場合は記録
		machine_translation[row["N"]] = row["MachineCorrect"]

n = 0

print("# changes")

for index, row in df.iterrows():	
	if row["N"] in machine_translation:#機械翻訳がある
#		print("AA")
		if (pd.notnull(row["BetterJP"])): #手動訳もある
			if( machine_translation[row["N"]] != row["BetterJP"]): #両者が違う
				print("## "+str(row["N"]))
				print(machine_translation[row["N"]])
				print(row["BetterJP"])

print()
print("# same w/machine translation")

for index, row in df.iterrows():	
	if (row["N"]) in machine_translation:#機械翻訳がある
		if (pd.notnull(row["BetterJP"])): #手動訳もある
			if( machine_translation[row["N"]] == row["BetterJP"]): #両者が同じ
				print("## "+str(row["N"]))
				print(row["BetterJP"])


print()
print("# same w/original")

for index, row in df.iterrows():	
	if (pd.notnull(row["BetterJP"])): #手動訳がある
		if(row["Japanese"] == row["BetterJP"]): #もとと同じ
			print("## "+str(row["N"]))
			print(row["BetterJP"])


dc = pd.read_table('dictionary.tsv')
dictionary = {}

for index, row in dc.iterrows():
	if (pd.notnull(row["English"]) and pd.notnull(row["Japanese"])):
		dictionary[row["English"]] = row["Japanese"]

dict_keys = list(dictionary.keys())
dict_keys.sort()

print()
print("# keywords")

for key in dict_keys:
	print("\n## "+key+"\t"+dictionary[key])
	for index, row in df.iterrows():
		Japanese = ""
		if pd.notnull(row["BetterJP"]): #手動訳があれば利用
			Japanese = row["BetterJP"]
		elif row["N"] in machine_translation: #機械翻訳があれば利用
			Japanese = machine_translation[row["N"]]
		else: #なければ既存訳
			Japanese = row["Japanese"]	
		if Japanese == row["English"]:#日英同じなら無視
			continue
		elif row["English"].find(key) != -1: #キーワードを含む
			if Japanese.find(dictionary[key]) == -1 : #日本語で使われていない
				print("### "+str(row["N"])+"\n"+row["English"]+"\n"+Japanese)
