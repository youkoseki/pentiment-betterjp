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
	"ロートヴォーゲル":"ロスフォーゲル",
	"マーティン":"マルティン",
	"フィレンツ":"フェレンツ",
	"フェレンツェ":"フィレンツェ",#フィレンツをフェレンツにすると変わってしまうので
	"エスター":"エステル",
	"マグダレン":"マグダレネ",
	"ハイルヴィッヒ":"ハイルヴィヒ",
	"タシング":"タッシング",
	"ヨルク":"ヨルグ",
	"オーガスト":"アウグスト",
	"レディ・サロメア":"サロメア婦人",
	"キアラウ":"キアサウ",
	"クロイスター":"回廊",
	"?":"？",
	"!":"！",
	"amp;":"",
	"[嘘をつく]":"[嘘]",
	"[嘘を吐く]":"[嘘]",
	"[ウソ]":"[嘘]",
	"[うそ]":"[嘘]",
	"。]":"]",
	"。」":"」"
	}

do = pd.read_table('../output/Pentiment-init.tsv',usecols=[0,1,2,3,4,5,6])

with open('../output/Pentiment-machinecorrect.tsv', 'w') as a,open('../output/Pentiment-machinecorrect-simple.tsv', 'w') as s:
#	print("Name\tUObjectName\tID\tEnglish\tJapanese\tDuplicate\tAutoUpdate\tBetterJP",file=f)
	print("Name\tID\tMachineCorrect",file=a)#全項目版
	print("MachineCorrect",file=s)#翻訳のみ版-Googleシート用

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
			print("'"+row["MachineCorrect"],file=a)
			print("'"+row["MachineCorrect"],file=s)
		else:
			print("",file=a)
			print("",file=s)
