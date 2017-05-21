
import re

class DataPatterns:
    opt_pattern_format = "({})?"

    row_pattern_base = r"""^(?P<level>\d{1,3})\s+(?P<name>\S+)"""
    row_pattern_ini = r"""\s+\("""
    row_pattern_attrib = r"""(?P<type>[ABCDFILNPT])((?P<length>\d+)(\,(?P<scale>\d+))?)?"""
    row_pattern_occurs = r"""/?\d+\:(?P<occurs>\d+)"""
    row_pattern_two_dimension = r"""\,\d+\:(?P<two_dimension>\d+)"""
    row_pattern_end = r"""\)"""
    row_pattern_init = r"""\s+INIT\s*<(?P<init>.+)>"""

    row_pattern = re.compile(row_pattern_base +
                             opt_pattern_format.format(row_pattern_ini) +
                             opt_pattern_format.format(row_pattern_attrib) +
                             opt_pattern_format.format(row_pattern_occurs) +
                             opt_pattern_format.format(row_pattern_two_dimension) +
                             opt_pattern_format.format(row_pattern_end) +
                             opt_pattern_format.format(row_pattern_init))

    row_pattern_redefine = re.compile(r'^(?P<level>\d{1,3})\s+REDEFINE\s+(?P<redefine>\S+)')
    pic_pattern_repeats = re.compile(r'(?P<constant>.)\((?P<repeat>\d+)\)')
    pic_pattern_float = re.compile(r'S?9*V9+')
    pic_pattern_float_edit = re.compile(r'S?[9Z]*[,][9Z]+')
    pic_pattern_integer = re.compile(r'S?9+(?!V)9+$')

    row_pattern_value = re.compile(r'\s+VALUE(S)?\s+(IS\s+)?(ARE\s+)?(?P<value>\S+)')

    row_pattern_mask = re.compile(r'\s{0,12}\d{1,13}[,]\d{2}')

    row_pattern_reinpt = r"""^REINPUT\s+\'(?P<msg>.*)\'"""
    row_pattern_mark = r"""\s+MARK\s+\*(?P<mark>\S+)"""
    row_pattern_reinput = re.compile(row_pattern_reinpt +
                                     opt_pattern_format.format(row_pattern_mark))
    row_pattern_if = re.compile(r"""^(IF|AND|OR)\s+(?P<operando1>\S+)?""" +
                                r"""\s+(?P<operator>EQ|NE|GT|GE|LT|LE|NO|NOT)\s+(?P<operando2>.+)""")
    row_pattern_for = re.compile(r"""^FOR\s+(?P<operando1>\S+)\s+(?P<start>\S+)\s+(TO\s+)?(?P<stop>\S+)""")