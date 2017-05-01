from HOFsGenericas import *
l480 = lambda line: line[4:80].rstrip()
isRem = lambda line: truth(re.match(r'^.{4}\s*[*]', line, re.UNICODE))
isNotRem = lambda line: not isRem(line)

defineRe = re.compile(r'^DEFINE\s+DATA', re.UNICODE)
isDefine = lambda line : truth(defineRe.match(line.strip()))
endDefineRe = re.compile(r'^END-DEFINE', re.UNICODE)
isEndDefine = lambda line : truth(endDefineRe.match(line.strip()))
x23 = lambda arg: arg.replace('#','X23_').replace('-', '_').lower()
