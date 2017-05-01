# Constantes Figurativas
CONSTANTES_FIGURATIVAS = { 'ZERO' : 0
                         , 'ZEROS' : 0
                         , 'ZEROES' : 0
                         , 'SPACE' : ' '
                         , 'SPACES' : ' '
                         , 'HIGH-VALUE' : '\xFF'
                         , 'HIGH-VALUES' : '\xFF'
                         , 'LOW-VALUE' : '\x00'
                         , 'LOW-VALUES' : '\x00'}


DDA = { 'GLOBAL': 'gda'
      , 'LOCAL': 'lda'
      , 'PARAMETER': 'pda'}


DATATYPES_NATURAL = {'A': {'type': 'str', 'init': "''", 'import': ''},
                     'N': {'type': 'Decimal', 'init': 'Decimal(0)', 'import': 'from decimal import *\n'},
                     'P': {'type': 'Decimal', 'init': 'Decimal(0)', 'import': 'from decimal import *\n'},
                     'I': {'type': 'int', 'init': 0, 'import': ''},
                     'F': {'type': 'Decimal', 'init': 'Decimal(0.0)', 'import': 'from decimal import *\n'},
                     'B': {'type': 'int', 'init': 0, 'import': ''},
                     'C': {'type': 'str', 'init': "''", 'import': ''},
                     'D': {'type': 'date', 'init': 'date(1, 1, 1)', 'import': 'from datetime import date\n'},
                     'T': {'type': 'time', 'init': 'time(1, 1, 1)', 'import': 'from datetime import time\n'},
                     'L': {'type': 'boolean', 'init': False}}


LINEFEED = ('ADD', 'AND', 'CALL', 'CALLNAT', 'COMPRESS', 'COMPUTE', 'DECIDE', 'DEFINE',
            'DELETE', 'DIVIDE', 'ELSE', 'END', 'END-DECIDE', 'END-FIND', 'END-FOR', 'END-IF',
            'END-NOREC', 'END-READ', 'END-REPEAT', 'END-SELECT', 'END-SUBROUTINE', 'ESCAPE',
            'EXAMINE', 'FIND', 'FOR', 'IF', 'IGNORE', 'INPUT', 'MOVE', 'OR', 'PERFORM', 'READ',
            'REINPUT', 'REPEAT', 'RESET', 'SELECT', 'SET', 'STOP', 'STORE', 'SUBTRACT', 'UPDATE',
            'WHEN', 'WRITE')

COMMANDS_NATURAL = ('ADD', 'AND', 'CALL', 'CALLNAT', 'COMPRESS', 'COMPUTE', 'DECIDE', 'DEFINE',
                    'DELETE', 'DIVIDE', 'ELSE', 'ESCAPE', 'EXAMINE', 'FIND', 'FOR', 'IF', 'IGNORE',
                    'INPUT', 'MOVE', 'OR', 'PERFORM', 'READ', 'REINPUT', 'REPEAT', 'RESET', 'SELECT',
                    'SET', 'STORE', 'SUBTRACT', 'UPDATE', 'WHEN', 'WRITE')
