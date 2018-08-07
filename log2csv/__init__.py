# -*- coding: utf-8 -*-
import regex as re
import os
import csv
import sys
import pkg_resources
import logging
from optparse import OptionParser

def expand_pattern(pattern_map, expression):
    regex = re.compile(r'%{\W*(?P<pattern_name>\w+)(?::\W*)?(?P<field_name>\w+)?\W*}')
    fields = []
    def replace_pattern(m):
        if not m.group('pattern_name'):
            return ''
        pattern = pattern_map.get(m.group('pattern_name'), '')
        field_name = m.group('field_name')
        if not field_name:
            return pattern
        else:
            fields.append(field_name)
            return '(?P<%s>%s)' % (field_name, pattern)
    n = 1
    while n > 0:
        expression, n = regex.subn(replace_pattern, expression)
    return re.compile(expression), fields

def load_patterns(pattern_file_list):
    patterns_map = {}
    for file_name in pattern_file_list:
        patterns = load_patterns_from_file(file_name)
        for k in patterns:
            patterns_map[k] = patterns[k]
    return patterns_map

def load_patterns_from_file(file_name):
    patterns = {}
    with open(file_name, 'r') as file:
        lines = file.readlines()
        for i in range(len(lines)):
            line = lines[i].rstrip('\r\n').lstrip(' ')
            if not line or line[0] == '#':
                continue
            tokens = line.split(' ', 1)
            if len(tokens) != 2:
                raise SyntaxError('pattern definition error at line %d' % (i + 1))
            patterns[tokens[0]] = tokens[1]
    return patterns


def get_all_files(dir):
    return [os.path.join(dp, f) for dp, dn, fn in os.walk(dir) for f in fn]

def main():
    parser = OptionParser()
    parser.add_option('-p', '--pattern', dest='pattern')
    parser.add_option('-e', '--expr', dest='expression')
    parser.add_option('-o', '--output', dest='output')
    #parser.add_option("-v", "--verbose", action="store_true", dest="verbose")
    #parser.add_option("-q", "--quiet", action="store_false", dest="verbose")
    options, log_files = parser.parse_args()

    pattern_files = get_all_files(pkg_resources.resource_filename(__name__, 'patterns'))
    if options.pattern:
        if os.path.isdir(options.pattern):
            custom_patterns = get_all_files(options.pattern)
            pattern_files = pattern_files + custom_patterns
        else:
            pattern_files.append(options.pattern)
    pattern_map = load_patterns(pattern_files)
    expression = options.expression
    regex, fields = expand_pattern(pattern_map, expression)


    if not options.output:
        output = sys.stdout
    else:
        output = open(options.output, 'w')

    if not log_files:
        inputs = [sys.stdin]
    else:
        inputs = [open(f, 'r') for f in log_files]

    try:
        csv_writer = csv.DictWriter(output, fieldnames=fields, lineterminator='\n')
        csv_writer.writeheader()
        for i in inputs:
            lines = i.readlines()
            ms = []
            for line in lines:
                m = regex.match(line)
                if m:
                    ms.append(m.groupdict())
            csv_writer.writerows(ms)
    except:
        pass
    finally:
        output.close()
        for i in inputs:
            i.close()

if __name__ == '__main__':
    main()
