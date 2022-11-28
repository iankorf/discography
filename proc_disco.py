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
				yield xmltodict.parse(line)
				record = ''
				reading = False
			record = line
			reading = True
		elif line.endswith(f'</{tag}>\n'):
			record += line
			yield xmltodict.parse(record)
			record = ''
			reading = False
		elif reading:
			record += line

parser = argparse.ArgumentParser(
	description='XML reader for discogg files')
parser.add_argument('xml', type=str, metavar='<xml>',
	help='path to xml file, gzip okay')
parser.add_argument('tag', type=str, metavar='<tag>',
	help='tag to look for (e.g. release)')
arg = parser.parse_args()

for record in read_records(arg.xml, arg.tag):
	print(json.dumps(record, indent=4))
	print('--------')
