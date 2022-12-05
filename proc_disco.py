import argparse
import gzip
import json
import re
import sys
import xmltodict


def read_records(filename, tag):

	if   sys.argv[1].endswith('gz'): fp = gzip.open(sys.argv[1], 'rt')
	elif sys.argv[1] == '-':         fp = sys.stdin
	else:                            fp = open(sys.argv[1])

	record = ''
	reading = False
	while True:
		line = fp.readline()
		if line == '': break
		if line.startswith(f'<{tag}'):
			if line.endswith(f'</{tag}>\n'):
				yield xmltodict.parse(line)[tag]
				record = ''
				reading = False
			record = line
			reading = True
		elif line.endswith(f'</{tag}>\n'):
			record += line
			yield xmltodict.parse(record)[tag]
			record = ''
			reading = False
		elif reading:
			record += line

def display(data, stuff=[]):
	if type(data) == dict:
		for key in data:
			if key.startswith('@'): continue
			if key.startswith('#'): continue
			stuff.append(key)
			display(data[key])
			
	

parser = argparse.ArgumentParser(
	description='XML reader for discogg files')
parser.add_argument('xml', type=str, metavar='<xml>',
	help='path to xml file, gzip okay')
parser.add_argument('tag', type=str, metavar='<tag>',
	help='tag to look for (e.g. release)')
arg = parser.parse_args()


for record in read_records(arg.xml, arg.tag):
	display(record)


"""

for record in read_records(arg.xml, arg.tag):
	
		print(k1)
		if type(record[k1]) == dict:
			for k2 in record[k1]:
				print(k1, k2)
				if type(record[k1][k2]) == dict:
					for k3 in record[k1][k2]:
						print(k1, k2, k3)
						if type(record[k1][k2][k3]) == dict:
							for k4 in record[k1][k2][k3]:
								print(k1, k2, k3, k4)
								if type(record[k1][k2][k3][k4]) == dict:
									for k5 in record[k1][k2][k3][k4]:
										print(k1, k2, k3, k4, k5)
						elif type(record[k1][k2][k3]) == list:
							print('list at k3')
							break
				elif type(record[k1][k2]) == list:
					print('list at k2')
					break
		elif type(record[k1]) == list:
			print('list at k1')
			break
	#print(json.dumps(record, indent=4))
	#print('--------')
"""