import unittest
import log2csv
import pkg_resources


TEST_DIR=pkg_resources.resource_filename(__name__, 'patterns')
class TestCase(unittest.TestCase):
    def test_get_all_files(self):
        files = log2csv.get_all_files(TEST_DIR)
        assert len(files) == 1
        assert files[0] == 'test/patterns/test'

    def test_load_patterns_from_file(self):
        files = log2csv.get_all_files(TEST_DIR)
        patterns = log2csv.load_patterns_from_file(files[0])
        assert len(patterns) == 4

    def test_load_patterns(self):
        files = log2csv.get_all_files(TEST_DIR)
        patterns = log2csv.load_patterns(files)
        assert len(patterns.keys()) == 4

    def test_expand_pattern(self):
        files = log2csv.get_all_files(TEST_DIR)
        patterns = log2csv.load_patterns(files)
        test_cases = [
                ('%{USERNAME:user} %{NUMBER: num}', ['Jack 101', 'Test Fail']),
                ('%{T01}', ['Jack 101', 'Test Fail']),
                ('%{T02}', ['Jack 101 Sparrow', 'Test Fail Fail'])
                ]
        for case in test_cases:
            regex, fields = log2csv.expand_pattern(patterns, case[0])
            m = regex.match(case[1][0])
            result = m.groupdict()
            for i in fields:
                assert result[i]
            m = regex.match(case[1][1])
            assert not m
