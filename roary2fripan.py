#!/usr/bin/env python3
# Script by Jason Kwong
# Script to format Roary output for FriPan

# Usage
import argparse
from argparse import RawTextHelpFormatter
import os
import sys
import csv

# Log a message to stderr
def msg(*args, **kwargs):
	print(*args, file=sys.stderr, **kwargs)

# Log an error to stderr and quit with non-zero error code
def err(*args, **kwargs):
	msg(*args, **kwargs)
	sys.exit(1);

# Check file exists
def check_file(f):
	if os.path.isfile(f) == False:
		err('ERROR: Cannot find "{}". Check file exists in the specified directory.'.format(f))

parser = argparse.ArgumentParser(
	formatter_class=RawTextHelpFormatter,
	description='Script to format Roary output for FriPan',
	usage='\n  %(prog)s [OPTIONS] <OUTPUT-PREFIX>')
parser.add_argument('output', metavar='PREFIX', help='Specify output prefix')
parser.add_argument('--input', metavar='FILE', default='gene_presence_absence.csv', help='Specify Roary output (default = "gene_presence_absence.csv")')
parser.add_argument('--version', action='version', version='v0.3-beta')
args = parser.parse_args()

porthoFILE = str(args.output) + '.proteinortho'
descFILE = str(args.output) + '.descriptions'
strainsFILE = str(args.output) + '.strains'
# In development - generate json file for ordering genes
#jsonFILE = str(args.output) + '.json'

portho = []
desc = []
head = []
temp = []

# Parse CSV
check_file(args.input)
with open(args.input) as csvfile:
	genes = csv.reader(csvfile, delimiter=',', quotechar='"')
	header = next(csvfile)
	for row in genes:
		del row[6:14]
		del row[0:2]
		proteins = row[4:]
		for p in proteins:
			if p:
				p = p.replace("\t",",")			# Fix paralogs separated by tab space
				desc.append([p, str(row[0])])
		row = [x.replace("\t",",") if x != "" else '*' for x in row]
		portho.append(row[1:])

# Fix header
	header = header.replace('"','').strip()
	header = header.split(',')
	del header[6:14]
	del header[0:3]
	header[0] = '# Species'
	header[1] = 'Genes'
	header[2] = 'Alg.-Conn.'
	portho.insert(0,header)

# Setup strains file
	strains = sorted(header[3:])
	b = str(len(str(len(strains))))
	a = "%0" + b + "d"
	strains = [(s + '\t' + str(a % (strains.index(s)+1))) for s in strains]
	strains.insert(0,'ID\tOrder')
	strains = ('\n'.join(map(str, strains)))

# Write proteinortho, descriptions and strains files
with open(porthoFILE, 'w') as outfile:
	out = csv.writer(outfile, delimiter='\t', lineterminator='\n')
	out.writerows(portho)
msg('Writing {} ... '.format(porthoFILE))

desc = sorted(desc)
with open(descFILE, 'w') as outfile:
	out = csv.writer(outfile, delimiter='\t', lineterminator='\n')
	out.writerows(desc)
msg('Writing {} ... '.format(descFILE))

with open(strainsFILE, 'w') as outfile:
	outfile.write(strains)
msg('Writing {} ... '.format(strainsFILE))

msg('Done.')
