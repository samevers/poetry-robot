#!/usr/bin/python

import sys,os,re

for line in sys.stdin:
	line = line.strip()
	line = "^" + line + "$"
	print "line = ",line
	line = line.decode("gbk")
	for c in line[:len(line)]:
		print "c = ", c.encode("gbk")
