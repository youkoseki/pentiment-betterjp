# coding:utf-8

import pandas as pd
import json
from pandas import json_normalize
import re
import zipfile
import shutil
import datetime

dt_now = datetime.datetime.now()

p1 = re.compile('^\'+')
p2 = re.compile('\'+$')

df = pd.read_table('../output/Pentiment-BetterJP - out.tsv')
#df = df.query('BetterJP.notnull() or Duplicate.notnull() or MachineCorrect.notnull()')

da = pd.read_table('../output/Pentiment-machinecorrect.tsv')
da = da.query('MachineCorrect.notnull()')

dj = {}
dj["StringTables"]  = []
name = ''
table = {}

existing_translation = {}
machine_translation = {}

for index, row in da.iterrows():
	if pd.notnull(row["MachineCorrect"]): #自動翻訳がある場合は、それを使う
		existing_translation[row["Name"]+","+str(row["ID"])] = row["MachineCorrect"]
		machine_translation[row["Name"]+","+str(row["ID"])] = row["MachineCorrect"]

for index, row in df.iterrows():
	if pd.notnull(row["BetterJP"]): #手動翻訳が存在する場合は上書きする
		existing_translation[row["Name"]+","+str(row["ID"])] = row["BetterJP"]

n = 0

for index, row in df.iterrows():
	if row["Japanese"] == "\'Xbox ネットワークにログイン\'":#MODの表示
		row["BetterJP"] = "\'Xbox ネットワークにログイン"+"(日本語改善MOD-v"+dt_now.strftime('%y%m%d')+")\'"
	if pd.isnull(row["BetterJP"]): #手動翻訳が存在しない
		if pd.notnull(row["Duplicate"]): #存在しない場合は同じ翻訳が使えるか確認
			if row["Duplicate"] in existing_translation: #既訳があるか確認
				row["BetterJP"] = existing_translation[row["Duplicate"]]
		if pd.isnull(row["BetterJP"]): #既訳が存在しないなら自動翻訳をチェック
			if (row["Name"]+","+str(row["ID"])) in machine_translation:
				row["BetterJP"] = machine_translation[row["Name"]+","+str(row["ID"])]
		if pd.isnull(row["BetterJP"]): #結局、翻訳が存在しないなら
			continue
	if row["Japanese"] == row["BetterJP"]:#旧訳と新約が同じならスキップ
		continue
	if name != row["Name"]:#新しいシーンなら、シーンを追加する
		name = row["Name"]
		table = {"Name" : row["Name"], "UObjectName" : row["UObjectName"], "Entries" : [] }
		dj["StringTables"].append(table)
	row["BetterJP"] = p1.sub("",row["BetterJP"])
	row["BetterJP"] = p2.sub("",row["BetterJP"])
	entry = {"ID" : row["ID"], "DefaultText" : row["BetterJP"]}
	table["Entries"].append(entry)
	n+=1


with open('../mods/betterJP/localized/jajp/betterjp.stringtablebundle', 'w') as f:
	json.dump(dj,f,ensure_ascii=False, indent=4)

shutil.make_archive('../Pentiment-betterJP', format='zip', root_dir='../', base_dir='mods')

print("corrected:"+str(n))
