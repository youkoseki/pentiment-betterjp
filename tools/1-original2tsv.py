# coding:utf-8

import pandas as pd
import json
from pandas import json_normalize

dfj = pd.read_json('../original/text_jajp.stringtablebundle')
dfe = pd.read_json('../original/text_enus.stringtablebundle')
dfj = dfj["StringTables"]
dfe = dfe["StringTables"]

english = {}
text_exist = {}

for table in dfe:
	for entry in table["Entries"]:
		english[table["Name"]+","+str(entry["ID"])] = entry["DefaultText"]
		if entry["DefaultText"] not in text_exist:
			text_exist[entry["DefaultText"]] = table["Name"]+","+str(entry["ID"])

with open('../output/Pentiment-init.tsv', 'w') as f:
	print("Name\tUObjectName\tID\tEnglish\tJapanese\tDuplicate\tMachineCorrect\tBetterJP",file=f)
	for table in dfj:
		for entry in table["Entries"]:
			print(table["Name"],end="\t",file=f)
			print(table["UObjectName"],end="\t",file=f)
			print(str(entry["ID"]),end="\t",file=f)
			print(repr(english[table["Name"]+","+str(entry["ID"])]),end="\t",file=f)
			print(repr(entry["DefaultText"]),end="\t",file=f)
			if(text_exist[english[table["Name"]+","+str(entry["ID"])]] != table["Name"]+","+str(entry["ID"])):
				print(text_exist[english[table["Name"]+","+str(entry["ID"])]],end='\n',file=f)
			else:
				print("",file=f)
