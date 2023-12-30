# coding:utf-8
import os

duplicate = {}
with open("dictionary.tsv") as f:
	for s_line in f:
		s_line = s_line.rstrip()
		keys = s_line.split("\t")
		if keys[0] in duplicate:
			print("DUPLICATE- "+keys[1])
			continue
		duplicate[keys[0]] = keys[1]

		print("# "+keys[1])
		rt = os.system('grep "'+keys[0]+'" "../output/Pentiment-BetterJP - out.tsv" | grep -v '+keys[1]) >> 8
		print(rt)
		print()

