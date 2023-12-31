# coding:utf-8
import pandas as pd
import json
import sys
from pandas import json_normalize
import re

jpjp = {}#表記揺れの修正 誤→正
enjp = {}#共通の言い回し


dict_switch = 0
with open("machinecorrect.tsv") as f:
	for s_line in f:
		s_line = s_line.rstrip()
		if re.match("#ENJP",s_line):#ENJPに切り替え
			dict_switch = 1
			continue
		elif re.match("#",s_line):#コメントを無視
			continue
		elif s_line == "":#空行を無視
			continue
		else:
			keys = s_line.split("\t")
			if len(keys) == 1:#キーが一つの時は二つめは空に置き換え
				keys.append("")
			if dict_switch == 0:
				jpjp[keys[0]] = keys[1]
			else:
				enjp[keys[0]] = keys[1]


do = pd.read_table('../output/Pentiment-init.tsv')

with open('../output/Pentiment-machinecorrect.tsv', 'w') as a,open('../output/Pentiment-machinecorrect-simple.tsv', 'w') as s:
#	print("Name\tUObjectName\tID\tEnglish\tJapanese\tDuplicate\tAutoUpdate\tBetterJP",file=f)
	print("N\tName\tID\tMachineCorrect",file=a)#全項目版
	print("MachineCorrect",file=s)#翻訳のみ版-Googleシート用

	for index, row in do.iterrows():
		skip = 0
		if row["English"] == row["Japanese"]:#英語と日本語が同じなら翻訳の必要なし
			skip = 1

		for word in enjp.keys():#定型文ならそのまま利用
			if row["English"] == "'"+word+"'":
				row["MachineCorrect"] = "'"+enjp[word]+"'"
				skip = 1
		
		if pd.notnull(row["Duplicate"]):#重複があるならスキップ
			skip = 1
		
		if skip == 0: #何もなければ自動翻訳
			jp = row["Japanese"]
			dt = ""
			idx = jp.find("<dt>")#二ヶ国語の文章の場合
			if idx > 0:
				dt = jp[:idx]#先の言語はそのままに
				jp = jp[idx:]#後半の言語は日本語なので置き換え

			for jpkey in jpjp.keys():
				jp=jp.replace(jpkey,jpjp[jpkey])
			#!と?の扱い
			jp=re.sub('^\'！','\'!',jp)
			jp=re.sub('！　','！',jp)
			jp=re.sub('！ ','！',jp)
			jp=re.sub('！','！ ',jp)
			jp=re.sub('？　','？',jp)
			jp=re.sub('？ ','？',jp)
			jp=re.sub('？','？ ',jp)
			jp=re.sub('！ ？','！？',jp)
			jp=re.sub('？ ！','？！',jp)
			jp=re.sub('？ ？','？？',jp)
			jp=re.sub('？ ？','？？',jp)
			jp=re.sub('！ ！','！！',jp)

			jp=re.sub('。 ','。',jp)
			jp=re.sub('、 ','、',jp)

			jp=re.sub('…','...',jp)
			jp=re.sub('\.\.\. ','...',jp)

			#文頭、文末、タグ最後から空白を除く
			jp=re.sub('^\' +','\'',jp)
			jp=re.sub('^\'　+','\'',jp)
			jp=re.sub('　+\</','</',jp)
			jp=re.sub(' +\</','</',jp)
			jp=re.sub(' +\<dt','<dt',jp)
			jp=re.sub('　+\'$','\'',jp)
			jp=re.sub(' +\'$','\'',jp)
			jp=re.sub(' +」','」',jp)
			if dt != "":#二ヶ国語の言語の場合、原文をくっつけて戻す
				jp = dt+jp
			if jp != row["Japanese"]:#アップデートされたなら
				row["MachineCorrect"] = jp

		print(row["N"],end="\t",file=a)
		print(row["Name"],end="\t",file=a)
#		print(row["UObjectName"],end="\t",file=f)
		print(row["ID"],end="\t",file=a)
#		print(row["English"],end="\t",file=f)
#		print(row["Japanese"],end="\t",file=f)
#		if pd.notnull(row["Duplicate"]):
#			print(row["Duplicate"],end="\t",file=f)
#		else:
#			print("",end="\t",file=f)
		if pd.notnull(row["MachineCorrect"]):
			print(row["MachineCorrect"],file=a)
			print("'"+row["MachineCorrect"],file=s)#Spreadsheetにコピーできるようカンマを追加
		else:
			print("",file=a)
			print("",file=s)
