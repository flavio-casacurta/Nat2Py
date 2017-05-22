#IMPORTS
from datetime import date
from datetime import time
from decimal import *


#GLOBAL
gda = {"#TAB-TXT-TELA": ["TELA DE INCLUSAO DE DADOS",
                  "TELA DE CONSULTA DE DADOS" ,
                  "TELA DE ALTERACAO DE DADOS",
                  "TELA DE EXCLUSAO DE DADOS"
                 ]
      }


#PARAMETER
pda = {      }


#LOCAL
lda = {"F255":{
        "CAMPO-ALFA": "",
        "CAMPO-NUMERICO": 0.0,
        "CAMPO-PACK": 0.0,
        "CAMPO-BINARIO": 0,
        "CAMPO-NUMERICO-DATA": 0.0,
        "CAMPO-DATE-DATA": date(1, 1, 1),
        "CAMPO-NUMERICO-HORA": 0.0,
        "CAMPO-TIME-HORA": time(1, 1, 1),
        "CAMPO-MULTIPLO": [0],
        "GP-SEM-MULTIPLO":{
                           "CAMPO-PE-ALFA": [""],
                           "CAMPO-PE-NUM": [0],
                          },
        "GP-COM-MULTIPLO":{
                           "CAMPO-PE2-MULTIPLO": [[0]],
                           "CAMPO-PE2-ALFA": [""],
                           "CAMPO-PE2-NUM": [0]
                          },
       },
       "#ATR": '',
       "#ATR1": [''],
       "#ATR2": [['']],
       "#ATR3": '',
       "#ATR4": '',
       "#ATR5": '',
       "#ATR6": '',
       "#TELA": {
                 "#CAMPO-ALFA": '',
                 "#CAMPO-NUM": '',
                 "#CAMPO-NUM-R1": {
                                   "FILLER_01": '',
                                   "#CAMPO-R-NU-TOT": Decimal(0),
                                   "#CAMPO-R-NU-TOT-R1": {
                                                          "#CAMPO-R-NU-DEC": Decimal(0),
                                                         },
                                  },
            "#CAMPO-PACK": '',
            "#CAMPO-PACK-R1": {
                               "FILLER_02": '',
                               "#CAMPO-R-PACK-TOT": Decimal(0),
                               "#CAMPO-R-PACK-TOT-R1": {
                                                        "#CAMPO-R-PACK-DEC": Decimal(0),
                                                       },
                              },
      "#CAMPO-BIN": '',
      "#CAMPO-BIN-R1": {
                        "#CAMPO-BIN-N": Decimal(0),
                       },
      "#CAMPO-DATA-TELA": '',
      "#CAMPO-DATA-TELA-R1": {
                              "#CAMPO-DT-NUM-ANO": '',
                              "#CAMPO-DT-NUM-MES": '',
                              "#CAMPO-DT-NUM-DIA": '',
                             },
      "#CAMPO-DATA-TELA-R2": {
                              "#CAMPO-DATA-TELA-N": Decimal(0),
                             },
      "#CAPO-HORA-TELA": '',
      "#CAPO-HORA-TELA-R1": {
                             "#COMPO-HORA-HO": '',
                             "#COMPO-HORA-MM": '',
                             "#COMPO-HORA-SS": '',
                            },
      "#CAPO-HORA-TELA-R2": {
                             "#COMPO-HORA-HO-N": Decimal(0),
                            },
      "#CAMPO-MULTIPLO": [''],
      "#CAMPO-MULTIPLO-R1": {
                             "#CAMPO-MULTIPLO-R": [Decimal(0)],
                            },
      "#CAMPO-PE-1": {
                      "#CAMPO-PE-ALFA": '',
                      "#CAMPO-PE-NUM": '',
                      "#CAMPO-PE-NUM-R1": {
                                           "#CAMPO-PE-NUM-R": Decimal(0),
                                          },
                     },
 "#CAMPO-PE-2": {
                 "#CAMPO-PE2-MULTIPLO": [''],
                 "#CAMPO-PE2-MULTIPLO-R1": {
                                            "#CAMPO-PE2-MULTIPLO-R": [Decimal(0)],
                                           },
                 "#CAMPO-PE2-ALFA": '',
                 "#CAMPO-PE2-NUM": '',
                 "#CAMPO-PE2-NUM-R1": {
                                       "#CAMPO-PE2-NUM-R": Decimal(0),
                                      },
                },
                 "#TL-CONFIRMA": '',
                },
                 "#IND1": Decimal(0),
                 "#IND2": Decimal(0),
                 "#IND-TL": Decimal(0),
                 "#TL-TX-CONF": 'CONFIRMA S/N:',
                 "#TL-TX-REGISTRO": 'REGISTRO ISN   :',
                 "#TL-REGISTRO": Decimal(0),
                 "#TL-TX-DATE": 'DATA DATE:',
                 "#TL-DT-DATE": '',
                 "#TL-TX-TIME": 'HORA TIME:',
                 "#TL-HO-TIME": '',
                 "#TX-PFS": 'PF8 - AVANCA',
                 "#CAMPO-RETORNA": '',
                 "#TB-RETORNA": [''],
                 "#IND-TB": Decimal(0),
      }


#PROCEDURE
 SET KEY ALL
lda['#ATR'] = [('writable', False)]
lda['#ATR1'][*] = [('writable', False)]
lda['#ATR2'][*,*] = [('writable', False)]
lda['#ATR6'] = [('writable', False)]
lda['#ATR4'] = [('writable', False), ('dark', True)]
lda['#ATR3'] = [('writable', False), ('dark', True)]
lda['#ATR5'] = [('writable', False)]
lda['#IND-TL'] = 3
 READ (3) F255
 END-READ
if *COUNTER[0870] == 0
   INPUT WITH TEXT 'NAO EXISTE REGISTROS A SEREM ALTERADOS'  USING MAP 'T11111IN'
if *PF-KEY == 'PF3'
or *PF-KEY == 'PF15'
      STOP
else:
if *PF-KEY != 'ENTR'
return False, 'TECLA INVALIDA'
    END-IF
   END-IF
 END-IF
 READ F255 BY ISN
   RESET #TELA
   PERFORM FORMATAR-TELA
lda['#TL-REGISTRO'] = *ISN
lda['#ATR'] = [('writable', True)]
lda['#ATR1'][*] = [('writable', True)]
lda['#ATR2'][*,*] = [('writable', True)]
lda['#ATR4'] = [('writable', True)]
lda['#ATR6'] = [('writable', False)]
lda['#ATR3'] = [('writable', False)]
lda['#ATR5'] = [('writable', False)]
   INPUT USING MAP 'T11111IN'
if *PF-KEY == 'PF3'
or *PF-KEY == 'PF15'
      STOP
else:
if *PF-KEY == 'ENTR'
or *PF-KEY == 'PF8'
continue
else:
return False, 'TECLA INVALIDA'
     END-IF
   END-IF
if lda['#TELA']['#TL-CONFIRMA'] != 'S'
       ESCAPE TOP
   END-IF
   PERFORM CRITICA-CAMPOS
   PERFORM ALTERAR-REGISTRO
lda['#ATR'] = [('writable', False)]
lda['#ATR1'][*] = [('writable', False)]
lda['#ATR2'][*,*] = [('writable', False)]
lda['#ATR4'] = [('writable', False)]
   INPUT WITH TEXT 'ALTERACAO EFETUADA' USING MAP 'T11111IN'
if *PF-KEY == 'PF3'
or *PF-KEY == 'PF15'
      STOP
else:
if *PF-KEY != 'ENTR'
return False, 'TECLA INVALIDA'
     END-IF
   END-IF
 END-READ
 DEFINE SUBROUTINE FORMATAR-TELA
lda['#TELA']['#CAMPO-ALFA'] = lda['F255']['CAMPO-ALFA']
lda['#TELA']['#CAMPO-NUM'] = lda['F255']['CAMPO-NUMERICO']
# removido >>>lda['#TELA']['#CAMPO-NUM'] = lda['#TELA']['#CAMPO-NUM']
lda['#TELA']['#CAMPO-PACK'] = lda['F255']['CAMPO-PACK']
# removido >>>lda['#TELA']['#CAMPO-PACK'] = lda['#TELA']['#CAMPO-PACK']
lda['#TELA']['#CAMPO-BIN-R1']['#CAMPO-BIN-N'] = lda['F255']['CAMPO-BINARIO']
lda['#TELA']['#CAMPO-DATA-TELA-R2']['#CAMPO-DATA-TELA-N'] = lda['F255']['CAMPO-NUMERICO-DATA']
lda['#TL-DT-DATE'] = lda['F255']['CAMPO-DATE-DATA']
lda['#TELA']['#CAPO-HORA-TELA-R2']['#COMPO-HORA-HO-N'] = lda['F255']['CAMPO-NUMERICO-HORA']
lda['#TL-HO-TIME'] = lda['F255']['CAMPO-TIME-HORA']
lda['#TELA']['#CAMPO-MULTIPLO-R1']['#CAMPO-MULTIPLO-R'][*] = lda['F255']['CAMPO-MULTIPLO'][*]
lda['#TELA']['#CAMPO-PE-1']['#CAMPO-PE-ALFA'][*] = lda['F255']['GP-SEM-MULTIPLO']['CAMPO-PE-ALFA'][*]
lda['#TELA']['#CAMPO-PE-1']['#CAMPO-PE-NUM-R1']['#CAMPO-PE-NUM-R'][*] = lda['F255']['GP-SEM-MULTIPLO']['CAMPO-PE-NUM'][*]
lda['#TELA']['#CAMPO-PE-2']['#CAMPO-PE2-MULTIPLO-R1']['#CAMPO-PE2-MULTIPLO-R'][*,*] = lda['F255']['GP-COM-MULTIPLO']['CAMPO-PE2-MULTIPLO'][*,*]
lda['#TELA']['#CAMPO-PE-2']['#CAMPO-PE2-ALFA'][*] = lda['F255']['GP-COM-MULTIPLO']['CAMPO-PE2-ALFA'][*]
lda['#TELA']['#CAMPO-PE-2']['#CAMPO-PE2-NUM-R1']['#CAMPO-PE2-NUM-R'][*] = lda['F255']['GP-COM-MULTIPLO']['CAMPO-PE2-NUM'][*]
 END-SUBROUTINE
 DEFINE SUBROUTINE CRITICA-CAMPOS
# removido >>>lda['#TELA']['#CAMPO-ALFA'] = lda['#TELA']['#CAMPO-ALFA']
if lda['#TELA']['#CAMPO-ALFA'] == '                          '
return False, lda['#TELA']['#CAMPO-ALFA'] ,'PREENCHIMENTO OBRIGATORIO'
   END-IF
# removido >>>lda['#TELA']['#CAMPO-NUM'] = lda['#TELA']['#CAMPO-NUM']
if lda['#TELA']['#CAMPO-NUM'] == '            '
return False, lda['#TELA']['#CAMPO-NUM'] ,'PREENCHIMENTO OBRIGATORIO'
   END-IF
# removido >>>lda['#TELA']['#CAMPO-NUM'] = lda['#TELA']['#CAMPO-NUM']
if  re.match((                \d,\d\d),lda['#TELA']['#CAMPO-NUM'])
or  re.match((               \d\d,\d\d),lda['#TELA']['#CAMPO-NUM'])
or  re.match((              \d\d\d,\d\d),lda['#TELA']['#CAMPO-NUM'])
or  re.match((             \d\d\d\d,\d\d),lda['#TELA']['#CAMPO-NUM'])
or  re.match((            \d\d\d\d\d,\d\d),lda['#TELA']['#CAMPO-NUM'])
or  re.match((           \d\d\d\d\d\d,\d\d),lda['#TELA']['#CAMPO-NUM'])
or  re.match((          \d\d\d\d\d\d\d,\d\d),lda['#TELA']['#CAMPO-NUM'])
or  re.match((         \d\d\d\d\d\d\d\d,\d\d),lda['#TELA']['#CAMPO-NUM'])
or  re.match((        \d\d\d\d\d\d\d\d\d,\d\d),lda['#TELA']['#CAMPO-NUM'])
or  re.match((       \d\d\d\d\d\d\d\d\d\d,\d\d),lda['#TELA']['#CAMPO-NUM'])
or  re.match((      \d\d\d\d\d\d\d\d\d\d\d,\d\d),lda['#TELA']['#CAMPO-NUM'])
or  re.match((     \d\d\d\d\d\d\d\d\d\d\d\d,\d\d),lda['#TELA']['#CAMPO-NUM'])
or  re.match((    \d\d\d\d\d\d\d\d\d\d\d\d\d,\d\d),lda['#TELA']['#CAMPO-NUM'])
or  re.match((   \d\d\d\d\d\d\d\d\d\d\d\d\d\d,\d\d),lda['#TELA']['#CAMPO-NUM'])
or  re.match((  \d\d\d\d\d\d\d\d\d\d\d\d\d\d\d,\d\d),lda['#TELA']['#CAMPO-NUM'])
or  re.match(( \d\d\d\d\d\d\d\d\d\d\d\d\d\d\d\d,\d\d),lda['#TELA']['#CAMPO-NUM'])
or  re.match((\d\d\d\d\d\d\d\d\d\d\d\d\d\d\d\d\d,\d\d),lda['#TELA']['#CAMPO-NUM'])
      EXAMINE FULL #CAMPO-NUM FOR ' ' REPLACE '0'
else:
return False, lda['#TELA']['#CAMPO-NUM'] ,'PREENCHER CAMPO COM NUMEROS E NO MINIMO DUAS CASAS DECIMAIS.'
   END-IF
# removido >>>lda['#TELA']['#CAMPO-PACK'] = lda['#TELA']['#CAMPO-PACK']
if lda['#TELA']['#CAMPO-PACK'] == '            '
return False, lda['#TELA']['#CAMPO-PACK'] ,'PREENCHIMENTO OBRIGATORIO'
   END-IF
# removido >>>lda['#TELA']['#CAMPO-PACK'] = lda['#TELA']['#CAMPO-PACK']
if  re.match((            \d,\d\d),lda['#TELA']['#CAMPO-PACK'])
or  re.match((           \d\d,\d\d),lda['#TELA']['#CAMPO-PACK'])
or  re.match((          \d\d\d,\d\d),lda['#TELA']['#CAMPO-PACK'])
or  re.match((         \d\d\d\d,\d\d),lda['#TELA']['#CAMPO-PACK'])
or  re.match((        \d\d\d\d\d,\d\d),lda['#TELA']['#CAMPO-PACK'])
or  re.match((       \d\d\d\d\d\d,\d\d),lda['#TELA']['#CAMPO-PACK'])
or  re.match((      \d\d\d\d\d\d\d,\d\d),lda['#TELA']['#CAMPO-PACK'])
or  re.match((     \d\d\d\d\d\d\d\d,\d\d),lda['#TELA']['#CAMPO-PACK'])
or  re.match((    \d\d\d\d\d\d\d\d\d,\d\d),lda['#TELA']['#CAMPO-PACK'])
or  re.match((   \d\d\d\d\d\d\d\d\d\d,\d\d),lda['#TELA']['#CAMPO-PACK'])
or  re.match((  \d\d\d\d\d\d\d\d\d\d\d,\d\d),lda['#TELA']['#CAMPO-PACK'])
or  re.match(( \d\d\d\d\d\d\d\d\d\d\d\d,\d\d),lda['#TELA']['#CAMPO-PACK'])
or  re.match((\d\d\d\d\d\d\d\d\d\d\d\d\d,\d\d),lda['#TELA']['#CAMPO-PACK'])
      EXAMINE FULL #CAMPO-PACK FOR ' ' REPLACE '0'
else:
return False, lda['#TELA']['#CAMPO-PACK'] ,'PREENCHER CAMPO COM NUMEROS E NO MINIMO DUAS CASAS DECIMAIS.'
   END-IF
if lda['#TELA']['#CAMPO-BIN'] == '         '
return False, lda['#TELA']['#CAMPO-BIN'] ,'PREENCHIMENTO OBRIGATORIO'
   END-IF
if not mask_full_num(lda['#TELA']['#CAMPO-BIN'],9)
return False, lda['#TELA']['#CAMPO-BIN'] ,'PREENCHER TOTALMENTE O CAMPO COM NUMEROS'
   END-IF
if lda['#TELA']['#CAMPO-DATA-TELA'] == '        '
return False, lda['#TELA']['#CAMPO-DATA-TELA'] ,'PREENCHIMENTO OBRIGATORIO'
   END-IF
if not mask_yyyymmdd(lda['#TELA']['#CAMPO-DATA-TELA'])
return False, lda['#TELA']['#CAMPO-DATA-TELA'] ,'DATA INVALIDA'
   END-IF
if lda['#TELA']['#CAPO-HORA-TELA'] == '        '
return False, lda['#TELA']['#CAPO-HORA-TELA'] ,'PREENCHIMENTO OBRIGATORIO'
   END-IF
if lda['#TELA']['#CAPO-HORA-TELA-R1']['#COMPO-HORA-HO'] == '00'  THRU '23'
and lda['#TELA']['#CAPO-HORA-TELA-R1']['#COMPO-HORA-MM'] == '00'  THRU '59'
and lda['#TELA']['#CAPO-HORA-TELA-R1']['#COMPO-HORA-SS'] == '00'  THRU '59'
continue
else:
return False, lda['#TELA']['#CAPO-HORA-TELA'] ,'HORA INVALIDA'
   END-IF
for lda['#IND1'] in xrange(0, 5):
# removido >>>lda['#TELA']['#CAMPO-MULTIPLO'][lda['#IND1']] = lda['#TELA']['#CAMPO-MULTIPLO'][lda['#IND1']]
if  re.match((  \d),lda['#TELA']['#CAMPO-MULTIPLO'][lda['#IND1']])
or  re.match(( \d\d),lda['#TELA']['#CAMPO-MULTIPLO'][lda['#IND1']])
or  mask_full_num(lda['#TELA']['#CAMPO-MULTIPLO'][lda['#IND1']],3)
continue
else:
if lda['#TELA']['#CAMPO-MULTIPLO'][lda['#IND1']] == '   '
continue
else:
return False, lda['#TELA']['#CAMPO-MULTIPLO'][1] ,'PREENCHIMENTO INVALIDO - DIGITAR SOMENTE NUMEROS OU EM BRANCO'
     END-IF
    END-IF
   END-FOR
   EXAMINE FULL #CAMPO-MULTIPLO(*) FOR ' ' REPLACE '0'
for lda['#IND1'] in xrange(0, 5):
# removido >>>lda['#TELA']['#CAMPO-PE-1']['#CAMPO-PE-NUM'][lda['#IND1']] = lda['#TELA']['#CAMPO-PE-1']['#CAMPO-PE-NUM'][lda['#IND1']]
if  re.match((    \d),lda['#TELA']['#CAMPO-PE-1']['#CAMPO-PE-NUM'][lda['#IND1']])
or  re.match((   \d\d),lda['#TELA']['#CAMPO-PE-1']['#CAMPO-PE-NUM'][lda['#IND1']])
or  re.match((  \d\d\d),lda['#TELA']['#CAMPO-PE-1']['#CAMPO-PE-NUM'][lda['#IND1']])
or  re.match(( \d\d\d\d),lda['#TELA']['#CAMPO-PE-1']['#CAMPO-PE-NUM'][lda['#IND1']])
or  mask_full_num(lda['#TELA']['#CAMPO-PE-1']['#CAMPO-PE-NUM'][lda['#IND1']],5)
continue
else:
if lda['#TELA']['#CAMPO-PE-1']['#CAMPO-PE-NUM'][lda['#IND1']] == '     '
continue
else:
return False, lda['#TELA']['#CAMPO-PE-1']['#CAMPO-PE-NUM'][1] ,'PREENCHIMENTO INVALIDO - DIGITAR SOMENTE NUMEROS OU EM BRANCO'
     END-IF
    END-IF
   END-FOR
   EXAMINE FULL #CAMPO-PE-NUM(*) FOR ' ' REPLACE '0'
for lda['#IND1'] in xrange(0, 5):
for lda['#IND2'] in xrange(0, 5):
# removido >>>lda['#TELA']['#CAMPO-PE-2']['#CAMPO-PE2-MULTIPLO'][#IND1,#IND2] = lda['#TELA']['#CAMPO-PE-2']['#CAMPO-PE2-MULTIPLO'][#IND1,#IND2]
if  re.match((  \d),lda['#TELA']['#CAMPO-PE-2']['#CAMPO-PE2-MULTIPLO'][#IND1,#IND2])
or  re.match(( \d\d),lda['#TELA']['#CAMPO-PE-2']['#CAMPO-PE2-MULTIPLO'][#IND1,#IND2])
or  mask_full_num(lda['#TELA']['#CAMPO-PE-2']['#CAMPO-PE2-MULTIPLO'][#IND1,#IND2],3)
continue
else:
if lda['#TELA']['#CAMPO-PE-2']['#CAMPO-PE2-MULTIPLO'][#IND1,#IND2] == '   '
continue
else:
return False, lda['#TELA']['#CAMPO-PE-2']['#CAMPO-PE2-MULTIPLO'][1,1] ,'PREENCHIMENTO INVALIDO - DIGITAR SOMENTE NUMEROS OU EM BRANCO'
      END-IF
     END-IF
    END-FOR
   END-FOR
   EXAMINE FULL #CAMPO-PE2-MULTIPLO(*,*) FOR ' ' REPLACE '0'
for lda['#IND1'] in xrange(0, 5):
# removido >>>lda['#TELA']['#CAMPO-PE-2']['#CAMPO-PE2-NUM'][lda['#IND1']] = lda['#TELA']['#CAMPO-PE-2']['#CAMPO-PE2-NUM'][lda['#IND1']]
if  re.match((    \d),lda['#TELA']['#CAMPO-PE-2']['#CAMPO-PE2-NUM'][lda['#IND1']])
or  re.match((   \d\d),lda['#TELA']['#CAMPO-PE-2']['#CAMPO-PE2-NUM'][lda['#IND1']])
or  re.match((  \d\d\d),lda['#TELA']['#CAMPO-PE-2']['#CAMPO-PE2-NUM'][lda['#IND1']])
or  re.match(( \d\d\d\d),lda['#TELA']['#CAMPO-PE-2']['#CAMPO-PE2-NUM'][lda['#IND1']])
or  mask_full_num(lda['#TELA']['#CAMPO-PE-2']['#CAMPO-PE2-NUM'][lda['#IND1']],5)
continue
else:
if lda['#TELA']['#CAMPO-PE-2']['#CAMPO-PE2-NUM'][lda['#IND1']] == '     '
continue
else:
return False, lda['#TELA']['#CAMPO-PE-2']['#CAMPO-PE2-NUM'][1] ,'PREENCHIMENTO INVALIDO - DIGITAR SOMENTE NUMEROS OU EM BRANCO'
     END-IF
    END-IF
   END-FOR
   EXAMINE FULL #CAMPO-PE2-NUM(*) FOR ' ' REPLACE '0'
if lda['#TELA']['#TL-CONFIRMA'] != 'S'
      ESCAPE TOP
   END-IF
 END-SUBROUTINE
 DEFINE SUBROUTINE  ALTERAR-REGISTRO
  GET F255 #TL-REGISTRO
EXAMINE FULL #CAMPO-NUM FOR ','
DELETE
# removido >>>lda['#TELA']['#CAMPO-NUM'] = lda['#TELA']['#CAMPO-NUM']
 EXAMINE FULL #CAMPO-NUM FOR ' ' REPLACE '0'
EXAMINE FULL #CAMPO-PACK FOR ','
DELETE
# removido >>>lda['#TELA']['#CAMPO-PACK'] = lda['#TELA']['#CAMPO-PACK']
 EXAMINE FULL #CAMPO-PACK FOR ' ' REPLACE '0'
lda['F255']['CAMPO-ALFA'] = lda['#TELA']['#CAMPO-ALFA']
lda['F255']['CAMPO-NUMERICO'] = lda['#TELA']['#CAMPO-NUM-R1']['#CAMPO-R-NU-TOT-R1']['#CAMPO-R-NU-DEC']
lda['F255']['CAMPO-PACK'] = lda['#TELA']['#CAMPO-PACK-R1']['#CAMPO-R-PACK-TOT-R1']['#CAMPO-R-PACK-DEC']
lda['F255']['CAMPO-BINARIO'] = lda['#TELA']['#CAMPO-BIN-R1']['#CAMPO-BIN-N']
lda['F255']['CAMPO-NUMERICO-DATA'] = lda['#TELA']['#CAMPO-DATA-TELA-R2']['#CAMPO-DATA-TELA-N']
lda['F255']['CAMPO-DATE-DATA'][EM=YYYYMMDD] = lda['#TELA']['#CAMPO-DATA-TELA']
lda['F255']['CAMPO-NUMERICO-HORA'] = lda['#TELA']['#CAPO-HORA-TELA-R2']['#COMPO-HORA-HO-N']
lda['F255']['CAMPO-TIME-HORA'][EM=HHIISS] = lda['#TELA']['#CAPO-HORA-TELA']
lda['F255']['CAMPO-MULTIPLO'][*] = lda['#TELA']['#CAMPO-MULTIPLO-R1']['#CAMPO-MULTIPLO-R'][*]
lda['F255']['GP-SEM-MULTIPLO']['CAMPO-PE-ALFA'][*] = lda['#TELA']['#CAMPO-PE-1']['#CAMPO-PE-ALFA'][*]
lda['F255']['GP-SEM-MULTIPLO']['CAMPO-PE-NUM'][*] = lda['#TELA']['#CAMPO-PE-1']['#CAMPO-PE-NUM-R1']['#CAMPO-PE-NUM-R'][*]
lda['F255']['GP-COM-MULTIPLO']['CAMPO-PE2-MULTIPLO'][*,*] = lda['#TELA']['#CAMPO-PE-2']['#CAMPO-PE2-MULTIPLO-R1']['#CAMPO-PE2-MULTIPLO-R'][*,*]
lda['F255']['GP-COM-MULTIPLO']['CAMPO-PE2-ALFA'][*] = lda['#TELA']['#CAMPO-PE-2']['#CAMPO-PE2-ALFA'][*]
lda['F255']['GP-COM-MULTIPLO']['CAMPO-PE2-NUM'][*] = lda['#TELA']['#CAMPO-PE-2']['#CAMPO-PE2-NUM-R1']['#CAMPO-PE2-NUM-R'][*]
  UPDATE (3290)
  END TRANSACTION
 END-SUBROUTINE
 END
