# coding:utf-8
import os

with open("peoples.tsv") as f:
	for s_line in f:
		s_line = s_line.rstrip()
		keys = s_line.split("\t")
		print("# "+keys[1])
		rt = os.system('grep "'+keys[0]+'" "../output/Pentiment-BetterJP - out.tsv" | grep -v '+keys[1]) >> 8
		print(rt)


