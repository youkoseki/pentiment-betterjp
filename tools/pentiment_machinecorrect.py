# coding:utf-8
import pandas as pd
import json
from pandas import json_normalize
import re

names = {#表記揺れの修正 誤→正
	"ピーター":"ペテロ",
	"ポール":"パウロ",
	"フォルクバート":"ヴォルクベルト",
	"ローレンツ":"ロレンツ",
	"マーティン":"マルティン",
	"フィレンツ":"フェレンツ",
	"フェレンツェ":"フィレンツェ",#フィレンツをフェレンツにすると変わってしまうので
	"エスター":"エステル",
	"マグダレン":"マグダレネ",
	"ハイルヴィッヒ":"ハイルヴィヒ",
	"タシング":"タッシング",
	"ヨルク":"ヨルグ",
	"オーガスト":"アウグスト",
	"キアラウ":"キアサウ",
	"クロイスター":"回廊",
	"?":"？",
	"!":"！",
	"amp;":"",
	"[嘘をつく]":"[嘘]",
	"[嘘を吐く]":"[嘘]",
	"[ウソ]":"[嘘]",
	"[うそ]":"[嘘]",
	"。]":"]"
	}

do = pd.read_table('../output/Pentiment-init.tsv',usecols=[0,1,2,3,4,5,6])

with open('../output/Pentiment-machinecorrect.tsv', 'w') as f:
#	print("Name\tUObjectName\tID\tEnglish\tJapanese\tDuplicate\tAutoUpdate\tBetterJP",file=f)
	print("MachineCorrect",file=f)

	for index, row in do.iterrows():
		if pd.isnull(row["Duplicate"]): #重複がないなら
			jp = row["Japanese"]
			for name in names.keys():
				jp=jp.replace(name,names[name])
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
			jp=re.sub('！ ！','！！',jp)

			jp=re.sub('…','...',jp)
			jp=re.sub('\.\.\. ','...',jp)

			#文頭、文末、タグ最後から空白を除く
			jp=re.sub('^\' ','\'',jp)
			jp=re.sub('^\'　','\'',jp)
			jp=re.sub('　\</','</',jp)
			jp=re.sub(' \</','</',jp)
			jp=re.sub('　\'$','\'',jp)
			jp=re.sub(' \'$','\'',jp)
			if jp != row["Japanese"]:#アップデートされたなら
				row["MachineCorrect"] = jp

#		print(row["Name"],end="\t",file=f)
#		print(row["UObjectName"],end="\t",file=f)
#		print(row["ID"],end="\t",file=f)
#		print(row["English"],end="\t",file=f)
#		print(row["Japanese"],end="\t",file=f)
#		if pd.notnull(row["Duplicate"]):
#			print(row["Duplicate"],end="\t",file=f)
#		else:
#			print("",end="\t",file=f)
		if pd.notnull(row["MachineCorrect"]):
			print("'"+row["MachineCorrect"],file=f)
		else:
			print("",file=f)
