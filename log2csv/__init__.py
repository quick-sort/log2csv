# -*- coding: utf-8 -*-
import regex as re
import os
import csv
import sys
import pkg_resources
import logging
import signal
import threading
import multiprocessing
from optparse import OptionParser

BATCH_SIZE=1000000

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

def parse_process(regex, in_q, out_q):
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    while True:
        if in_q.empty():
            pass
        try:
            lines = in_q.get()
            if not lines:
                out_q.put(None)
                return
            rows = []
            for line in lines:
                m = regex.match(line)
                if m:
                    rows.append(m.groupdict())
            out_q.put(rows)
        except:
            pass

def read_thread(inputs, in_q, worker_count):
    for i in inputs:
        lines = i.readlines(BATCH_SIZE)
        while lines:
            while in_q.full():
                pass
            in_q.put(lines)
            lines = i.readlines(BATCH_SIZE)

    for i in range(worker_count):
        in_q.put(None)

def write_thread(writer, out_q, worker_count):
    count = 0
    while count < worker_count:
        while out_q.empty():
            pass
        rows = out_q.get()
        if not rows:
            count += 1
        else:
            writer.writerows(rows)

def parallel_process(regex, inputs, writer, worker_count):
    in_q = multiprocessing.Queue(maxsize=worker_count * 10)
    out_q = multiprocessing.Queue()
    workers = []
    for i in range(worker_count):
        worker = multiprocessing.Process(target=parse_process, args=(regex, in_q, out_q))
        worker.start()
        workers.append(worker)

    def handle_sigint(signal, frame):
        for worker in workers:
            worker.terminate()
            worker.join()
        sys.exit(1)
    signal.signal(signal.SIGINT, handle_sigint)

    read_worker = threading.Thread(target = read_thread, args=(inputs, in_q, worker_count))
    read_worker.start()
    write_worker = threading.Thread(target = write_thread, args=(writer, out_q, worker_count))
    write_worker.start()

    read_worker.join()
    for worker in workers:
        worker.join()
    write_worker.join()

def serialize_process(regex, inputs, writer):
    for i in inputs:
        lines = i.readlines(BATCH_SIZE * 10)
        while lines:
            rows = []
            for line in lines:
                m = regex.match(line)
                if m:
                    rows.append(m.groupdict())
            writer.writerows(rows)
            lines = i.readlines(BATCH_SIZE * 10)

def main():
    parser = OptionParser()
    parser.add_option('-p', '--pattern', dest='pattern')
    parser.add_option('-e', '--expr', dest='expression')
    parser.add_option('-o', '--output', dest='output')
    #parser.add_option("-v", "--verbose", action="store_true", dest="verbose")
    #parser.add_option("-q", "--quiet", action="store_false", dest="verbose")
    options, inputs = parser.parse_args()

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

    CPU = multiprocessing.cpu_count()

    if not inputs:
        inputs = [sys.stdin]
    else:
        for i in range(len(inputs)):
            inputs[i] = open(inputs[i], 'r')

    output = options.output
    if not output:
        output = sys.stdout
    else:
        output = open(output, 'w')

    try:
        csv_writer = csv.DictWriter(output, fieldnames=fields, lineterminator='\n')
        csv_writer.writeheader()
        if CPU == 1:
            serialize_process(regex, inputs, csv_writer)
        else:
            parallel_process(regex, inputs, csv_writer, CPU - 1)
    except:
        pass
    finally:
        output.close()
        for i in inputs:
            i.close()

if __name__ == '__main__':
    main()
