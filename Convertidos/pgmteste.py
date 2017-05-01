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
 MOVE (AD=PI)                     TO   #ATR  #ATR1(*)  #ATR2(*,*)  #ATR6
 MOVE (AD=PN)                     TO   #ATR4
 MOVE (AD=PN)                     TO   #ATR3
 MOVE (AD=P)                      TO   #ATR5
 MOVE 3                           TO   #IND-TL
 READ (3) F255
 END-READ
 IF *COUNTER(0870)                EQ   0
   INPUT WITH TEXT 'NAO EXISTE REGISTROS A SEREM ALTERADOS'  USING MAP 'T11111IN'
   IF *PF-KEY                       EQ   'PF3' OR= 'PF15'
      STOP
   ELSE
    IF *PF-KEY                     NE   'ENTR'
       REINPUT  'TECLA INVALIDA'
    END-IF
   END-IF
 END-IF
 READ F255 BY ISN
   RESET #TELA
   PERFORM FORMATAR-TELA
   MOVE *ISN                         TO  #TL-REGISTRO
   MOVE (AD=I)                      TO   #ATR  #ATR1(*)  #ATR2(*,*)  #ATR4
   MOVE (AD=P)                      TO   #ATR6
   MOVE (AD=P)                      TO   #ATR3
   MOVE (AD=P)                      TO   #ATR5
   INPUT USING MAP 'T11111IN'
   IF *PF-KEY                       EQ   'PF3' OR= 'PF15'
      STOP
   ELSE
     IF *PF-KEY                     EQ   'ENTR' OR= 'PF8'
        IGNORE
     ELSE
         REINPUT 'TECLA INVALIDA'
     END-IF
   END-IF
   IF #TL-CONFIRMA                  NE   'S'
       ESCAPE TOP
   END-IF
   PERFORM CRITICA-CAMPOS
   PERFORM ALTERAR-REGISTRO
   MOVE (AD=P)                      TO   #ATR  #ATR1(*)  #ATR2(*,*)  #ATR4
   INPUT WITH TEXT 'ALTERACAO EFETUADA' USING MAP 'T11111IN'
   IF *PF-KEY                       EQ   'PF3' OR= 'PF15'
      STOP
   ELSE
     IF *PF-KEY                     NE   'ENTR'
        REINPUT  'TECLA INVALIDA'
     END-IF
   END-IF
 END-READ
 DEFINE SUBROUTINE FORMATAR-TELA
  MOVE  CAMPO-ALFA                 TO   #CAMPO-ALFA
  MOVE  EDITED CAMPO-NUMERICO(EM=ZZZZZZZZZZZZZZZZ9,99)  TO   #CAMPO-NUM
  MOVE LEFT #CAMPO-NUM             TO   #CAMPO-NUM
  MOVE  EDITED CAMPO-PACK(EM=ZZZZZZZZZZZZ9,99)  TO   #CAMPO-PACK
  MOVE LEFT #CAMPO-PACK            TO   #CAMPO-PACK
  MOVE  CAMPO-BINARIO              TO   #CAMPO-BIN-N
  MOVE  CAMPO-NUMERICO-DATA        TO   #CAMPO-DATA-TELA-N
  MOVE EDITED  CAMPO-DATE-DATA(EM=DD/MM/YYYY)  TO   #TL-DT-DATE
  MOVE  CAMPO-NUMERICO-HORA        TO   #COMPO-HORA-HO-N
  MOVE  EDITED  CAMPO-TIME-HORA(EM=HH:II:SS)  TO   #TL-HO-TIME
  MOVE CAMPO-MULTIPLO(*)           TO   #CAMPO-MULTIPLO-R(*)
  MOVE CAMPO-PE-ALFA(*)            TO   #CAMPO-PE-ALFA(*)
  MOVE CAMPO-PE-NUM(*)             TO   #CAMPO-PE-NUM-R(*)
  MOVE CAMPO-PE2-MULTIPLO(*,*) TO #CAMPO-PE2-MULTIPLO-R(*,*)
  MOVE CAMPO-PE2-ALFA(*)           TO   #CAMPO-PE2-ALFA(*)
  MOVE CAMPO-PE2-NUM(*)            TO   #CAMPO-PE2-NUM-R(*)
 END-SUBROUTINE
 DEFINE SUBROUTINE CRITICA-CAMPOS
   MOVE LEFT #CAMPO-ALFA            TO   #CAMPO-ALFA
   IF #CAMPO-ALFA                   EQ   '                          '
      REINPUT 'PREENCHIMENTO OBRIGATORIO' MARK *#CAMPO-ALFA
   END-IF
   MOVE LEFT #CAMPO-NUM             TO   #CAMPO-NUM
   IF #CAMPO-NUM                    EQ   '            '
      REINPUT 'PREENCHIMENTO OBRIGATORIO' MARK *#CAMPO-NUM
   END-IF
   MOVE RIGHT #CAMPO-NUM            TO   #CAMPO-NUM
   IF #CAMPO-NUM              EQ    MASK ('                'N','NN)  OR=   MASK ('               'NN','NN)  OR=   MASK ('              'NNN','NN)  OR=   MASK ('             'NNNN','NN)  OR=   MASK ('            'NNNNN','NN)  OR=   MASK ('           'NNNNNN','NN)  OR=   MASK ('          'NNNNNNN','NN)  OR=   MASK ('         'NNNNNNNN','NN)  OR=   MASK ('        'NNNNNNNNN','NN)  OR=   MASK ('       'NNNNNNNNNN','NN)  OR=   MASK ('      'NNNNNNNNNNN','NN)  OR=   MASK ('     'NNNNNNNNNNNN','NN)  OR=   MASK ('    'NNNNNNNNNNNNN','NN)  OR=   MASK ('   'NNNNNNNNNNNNNN','NN)  OR=   MASK ('  'NNNNNNNNNNNNNNN','NN)  OR=   MASK (' 'NNNNNNNNNNNNNNNN','NN)  OR=   MASK (NNNNNNNNNNNNNNNNN','NN)
      EXAMINE FULL #CAMPO-NUM FOR ' ' REPLACE '0'
   ELSE
       REINPUT  'PREENCHER CAMPO COM NUMEROS E NO MINIMO DUAS CASAS DECIMAIS.'  MARK *#CAMPO-NUM
   END-IF
   MOVE LEFT #CAMPO-PACK            TO   #CAMPO-PACK
   IF #CAMPO-PACK                   EQ   '            '
      REINPUT 'PREENCHIMENTO OBRIGATORIO' MARK *#CAMPO-PACK
   END-IF
   MOVE RIGHT #CAMPO-PACK           TO   #CAMPO-PACK
   IF #CAMPO-PACK             EQ    MASK ('            'N','NN)  OR=   MASK ('           'NN','NN)  OR=   MASK ('          'NNN','NN)  OR=   MASK ('         'NNNN','NN)  OR=   MASK ('        'NNNNN','NN)  OR=   MASK ('       'NNNNNN','NN)  OR=   MASK ('      'NNNNNNN','NN)  OR=   MASK ('     'NNNNNNNN','NN)  OR=   MASK ('    'NNNNNNNNN','NN)  OR=   MASK ('   'NNNNNNNNNN','NN)  OR=   MASK ('  'NNNNNNNNNNN','NN)  OR=   MASK (' 'NNNNNNNNNNNN','NN)  OR=   MASK (NNNNNNNNNNNNN','NN)
      EXAMINE FULL #CAMPO-PACK FOR ' ' REPLACE '0'
   ELSE
       REINPUT  'PREENCHER CAMPO COM NUMEROS E NO MINIMO DUAS CASAS DECIMAIS.'  MARK *#CAMPO-PACK
   END-IF
   IF #CAMPO-BIN                   EQ   '         '
      REINPUT 'PREENCHIMENTO OBRIGATORIO' MARK *#CAMPO-BIN
   END-IF
   IF #CAMPO-BIN                   NE   MASK (NNNNNNNNN)
      REINPUT 'PREENCHER TOTALMENTE O CAMPO COM NUMEROS' MARK *#CAMPO-BIN
   END-IF
   IF #CAMPO-DATA-TELA             EQ  '        '
      REINPUT 'PREENCHIMENTO OBRIGATORIO' MARK *#CAMPO-DATA-TELA
   END-IF
   IF #CAMPO-DATA-TELA             NE  MASK (YYYYMMDD)
      REINPUT 'DATA INVALIDA'      MARK *#CAMPO-DATA-TELA
   END-IF
   IF #CAPO-HORA-TELA              EQ  '        '
      REINPUT 'PREENCHIMENTO OBRIGATORIO' MARK *#CAPO-HORA-TELA
   END-IF
   IF #COMPO-HORA-HO               EQ '00'  THRU '23' AND  #COMPO-HORA-MM               EQ '00'  THRU '59' AND  #COMPO-HORA-SS               EQ '00'  THRU '59'
      IGNORE
   ELSE
      REINPUT 'HORA INVALIDA'      MARK *#CAPO-HORA-TELA
   END-IF
   FOR #IND1        1              TO  5
    MOVE RIGHT #CAMPO-MULTIPLO(#IND1) TO  #CAMPO-MULTIPLO(#IND1)
    IF #CAMPO-MULTIPLO(#IND1)      EQ  MASK ('  'N)  OR= MASK (' 'NN)  OR= MASK (NNN)
       IGNORE
    ELSE
     IF #CAMPO-MULTIPLO(#IND1)     EQ  '   '
        IGNORE
     ELSE
       REINPUT  'PREENCHIMENTO INVALIDO - DIGITAR SOMENTE NUMEROS OU EM BRANCO'  MARK *#CAMPO-MULTIPLO(1)
     END-IF
    END-IF
   END-FOR
   EXAMINE FULL #CAMPO-MULTIPLO(*) FOR ' ' REPLACE '0'
   FOR #IND1        1              TO  5
    MOVE RIGHT #CAMPO-PE-NUM(#IND1) TO  #CAMPO-PE-NUM(#IND1)
    IF #CAMPO-PE-NUM(#IND1)        EQ  MASK ('    'N)  OR= MASK ('   'NN)  OR= MASK ('  'NNN)  OR= MASK (' 'NNNN)  OR= MASK (NNNNN)
       IGNORE
    ELSE
     IF #CAMPO-PE-NUM(#IND1)     EQ  '     '
        IGNORE
     ELSE
       REINPUT  'PREENCHIMENTO INVALIDO - DIGITAR SOMENTE NUMEROS OU EM BRANCO'  MARK *#CAMPO-PE-NUM(1)
     END-IF
    END-IF
   END-FOR
   EXAMINE FULL #CAMPO-PE-NUM(*) FOR ' ' REPLACE '0'
   FOR #IND1        1              TO  5
    FOR #IND2        1             TO  5
     MOVE RIGHT #CAMPO-PE2-MULTIPLO (#IND1,#IND2)  TO  #CAMPO-PE2-MULTIPLO(#IND1,#IND2)
     IF #CAMPO-PE2-MULTIPLO(#IND1,#IND2)      EQ  MASK ('  'N)  OR= MASK (' 'NN)  OR= MASK (NNN)
         IGNORE
     ELSE
      IF #CAMPO-PE2-MULTIPLO(#IND1,#IND2)     EQ  '   '
         IGNORE
      ELSE
        REINPUT  'PREENCHIMENTO INVALIDO - DIGITAR SOMENTE NUMEROS OU EM BRANCO'  MARK *#CAMPO-PE2-MULTIPLO(1,1)
      END-IF
     END-IF
    END-FOR
   END-FOR
   EXAMINE FULL #CAMPO-PE2-MULTIPLO(*,*) FOR ' ' REPLACE '0'
   FOR #IND1        1              TO  5
    MOVE RIGHT #CAMPO-PE2-NUM(#IND1) TO  #CAMPO-PE2-NUM(#IND1)
    IF #CAMPO-PE2-NUM(#IND1)       EQ  MASK ('    'N)  OR= MASK ('   'NN)  OR= MASK ('  'NNN)  OR= MASK (' 'NNNN)  OR= MASK (NNNNN)
       IGNORE
    ELSE
     IF #CAMPO-PE2-NUM(#IND1)    EQ  '     '
        IGNORE
     ELSE
       REINPUT  'PREENCHIMENTO INVALIDO - DIGITAR SOMENTE NUMEROS OU EM BRANCO'  MARK *#CAMPO-PE2-NUM(1)
     END-IF
    END-IF
   END-FOR
   EXAMINE FULL #CAMPO-PE2-NUM(*) FOR ' ' REPLACE '0'
   IF #TL-CONFIRMA                 NE   'S'
      ESCAPE TOP
   END-IF
 END-SUBROUTINE
 DEFINE SUBROUTINE  ALTERAR-REGISTRO  GET F255 #TL-REGISTRO
 EXAMINE FULL #CAMPO-NUM FOR ',' DELETE
 MOVE RIGHT  #CAMPO-NUM  TO   #CAMPO-NUM
 EXAMINE FULL #CAMPO-NUM FOR ' ' REPLACE '0'
 EXAMINE FULL #CAMPO-PACK FOR ',' DELETE
 MOVE RIGHT #CAMPO-PACK TO #CAMPO-PACK
 EXAMINE FULL #CAMPO-PACK FOR ' ' REPLACE '0'
  MOVE  #CAMPO-ALFA                TO   CAMPO-ALFA
  MOVE  #CAMPO-R-NU-DEC            TO   CAMPO-NUMERICO
  MOVE  #CAMPO-R-PACK-DEC          TO   CAMPO-PACK
  MOVE  #CAMPO-BIN-N               TO   CAMPO-BINARIO
  MOVE  #CAMPO-DATA-TELA-N         TO   CAMPO-NUMERICO-DATA
  MOVE EDITED #CAMPO-DATA-TELA  TO   CAMPO-DATE-DATA(EM=YYYYMMDD)
  MOVE  #COMPO-HORA-HO-N           TO   CAMPO-NUMERICO-HORA
  MOVE  EDITED  #CAPO-HORA-TELA  TO   CAMPO-TIME-HORA(EM=HHIISS)
  MOVE #CAMPO-MULTIPLO-R(*)        TO   CAMPO-MULTIPLO(*)
  MOVE #CAMPO-PE-ALFA(*)           TO   CAMPO-PE-ALFA(*)
  MOVE #CAMPO-PE-NUM-R(*)          TO   CAMPO-PE-NUM(*)
  MOVE #CAMPO-PE2-MULTIPLO-R(*,*)  TO   CAMPO-PE2-MULTIPLO(*,*)
  MOVE #CAMPO-PE2-ALFA(*)          TO   CAMPO-PE2-ALFA(*)
  MOVE #CAMPO-PE2-NUM-R(*)         TO   CAMPO-PE2-NUM(*)
  UPDATE (3290)
  END TRANSACTION
 END-SUBROUTINE
 END
