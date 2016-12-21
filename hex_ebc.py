arqbin = 'ebcdic.txt'
HEX = '0123456789ABCDEF'
with open(arqbin, 'wb') as bin:
    for z in HEX:
        for n in HEX:
            e = chr(int(z + n, 16))
            o = ord(e)
            try:
                a = chr(int(z + n))
            except:
                a = '?'
            bin.write('{:03} - {}{} - ebcdic: {} - ascii: {}\n'.format(o, z, n, e, a))