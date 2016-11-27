
import re

class DataPatterns:
    opt_pattern_format = "({})?"

    row_pattern_base = r'^(?P<level>\d{1,3})\s+(?P<name>\S+)'
    row_pattern_attrib = r'\s+\((?P<attrib>.\d+(\,\d+)?)'
    row_pattern_occurs = r'\/\d+\:(?P<occurs>\d+)'
    row_pattern_end = r'\)'


    row_pattern = re.compile(row_pattern_base +
                             opt_pattern_format.format(row_pattern_attrib) +
                             opt_pattern_format.format(row_pattern_occurs) +
                             row_pattern_end)

    row_pattern_redefine = re.compile(r'^(?P<level>\d{1,3})\s+REDEFINE\s+(?P<redefine>\S+)')
    pic_pattern_repeats = re.compile(r'(?P<constant>.)\((?P<repeat>\d+)\)')
    pic_pattern_float = re.compile(r'S?9*V9+')
    pic_pattern_float_edit = re.compile(r'S?[9Z]*[,][9Z]+')
    pic_pattern_integer = re.compile(r'S?9+(?!V)9+$')

    row_pattern_value = re.compile(r'\s+VALUE(S)?\s+(IS\s+)?(ARE\s+)?(?P<value>\S+)')

    row_pattern_mask = re.compile(r'\s{0,12}\d{1,13}[,]\d{2}')
