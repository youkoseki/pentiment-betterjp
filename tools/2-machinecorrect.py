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
	"ドラッカーリン":"ドラッカリン",
	"ドラケリン":"ドラッカリン",
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
		if row["English"] == row["Japanese"]:#英語と日本語が同じなら翻訳の必要なし
			pass
		elif pd.isnull(row["Duplicate"]): #重複がないなら
			jp = row["Japanese"]
			dt = ""
			idx = jp.find("<dt>")#二ヶ国語の文章の場合
			if idx > 0:
				dt = jp[:idx]#先の言語はそのままに
				jp = jp[idx:]#後半の言語は日本語なので置き換え

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
			jp=re.sub('？ ？','？？',jp)
			jp=re.sub('？ ？','？？',jp)
			jp=re.sub('！ ！','！！',jp)

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
