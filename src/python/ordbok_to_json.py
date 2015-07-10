#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import argparse
import json
import gzip

INPUT_GARBAGE_OFFSET = 26

def read_lines_from_gzipped_file(filename):
    with gzip.open(filename) as file:
        return [line.strip() for line in file.readlines()][INPUT_GARBAGE_OFFSET:]

def read_entries(lines):
    entries = {}

    for line in lines:
        id, gf, ff, mb, pk, np = line.split('\t')

        entries[id] = ( {'grunnform'               : gf,
                         'fullform'                : ff,
                         'morfologisk_beskrivelse' : mb,
                         'paradigmekode'           : pk,
                         'nummer_i_paradigme'      : np} )

    print('Read {} entries'.format(len(entries.keys())))

    return entries

def write_entries_to_json_file(entries, filename):
    filename = filename if filename.endswith('.gz') else filename + '.gz'
    with gzip.open(filename, 'w') as file:
        json.dump(entries, file, indent=2)

parser = argparse.ArgumentParser()
parser.add_argument('input_filename',  help='Input file, gzipped')
parser.add_argument('output_filename', help='Output file name, will be gzipped')

if __name__ == '__main__':
    args = parser.parse_args()
    lines = read_lines_from_gzipped_file(args.input_filename)
    entries = read_entries(lines)
    write_entries_to_json_file(entries, args.output_filename)

