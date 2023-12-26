# coding:utf-8

import pandas as pd
import json
from pandas import json_normalize
import re
import zipfile
import shutil

p1 = re.compile('^\'')
p2 = re.compile('\'$')

df = pd.read_table('../output/Pentiment-BetterJP - out.tsv',usecols=[0,1,2,4,5,6,7])
df = df.query('BetterJP.notnull() or Duplicate.notnull()')

dj = {}
dj["StringTables"]  = []
name = ''
table = {}

existing_translation = {}

for index, row in df.iterrows():
	if pd.notnull(row["BetterJP"]): #すでに翻訳が存在する場合はそのまま、既訳を加える
		existing_translation[row["Name"]+","+str(row["ID"])] = row["BetterJP"]
	elif pd.notnull(row["AutoUpdate"]): #自動翻訳がある場合は、それを使う
		existing_translation[row["Name"]+","+str(row["ID"])] = row["AutoUpdate"]

for index, row in df.iterrows():
	if pd.isnull(row["BetterJP"]): #翻訳が存在しない
		if pd.notnull(row["Duplicate"]): #存在しない場合は同じ翻訳が使えるか確認
			if row["Duplicate"] in existing_translation: #既訳があるか確認
				row["BetterJP"] = existing_translation[row["Duplicate"]]
		elif pd.notnull(row["AutoUpdate"]): #それでも存在しない場合は自動翻訳が使えるか確認
			row["BetterJP"] = row["AutoUpdate"]
		if pd.isnull(row["BetterJP"]): #結局、翻訳が存在しないなら
			continue
	if row["Japanese"] == row["BetterJP"]:#旧訳と新約が同じならスキップ
		continue
	if name != row["Name"]:#新しいシーンなら、シーンを追加する
		name = row["Name"]
		table = {"Name" : row["Name"], "UObjectName" : row["UObjectName"], "Entries" : [] }
		dj["StringTables"].append(table)
	jp = row["BetterJP"]
	jp = p1.sub("",jp)
	jp = p2.sub("",jp)
	entry = {"ID" : row["ID"], "DefaultText" : jp}
	table["Entries"].append(entry)


with open('../mods/betterJP/localized/jajp/betterjp.stringtablebundle', 'w') as f:
	json.dump(dj,f,ensure_ascii=False, indent=4)

shutil.make_archive('../Pentiment-betterJP', format='zip', root_dir='../', base_dir='mods')