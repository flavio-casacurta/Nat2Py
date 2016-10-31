from HOFsGenericas import *
l472 = lambda line: line[4:72].rstrip()
isRem = lambda line: truth(re.match(r'^.{4}[*]', line, re.UNICODE))
isNotRem = lambda line: truth(re.match(r'^.{6}[\s|-]', line, re.UNICODE))
isRem = lambda line: not isNotRem(line)
isEjectOrSkip = lambda line: truth(re.search(r'\b(EJECT|SKIP)\b', line, re.UNICODE))
isNotEjectOrSkip = lambda line: not isEjectOrSkip(line)

defineRe = re.compile(r'^DEFINE DATA', re.UNICODE)
isDefine = lambda line : truth(defineRe.match(line))
endDefineRe = re.compile(r'^END-DEFINE', re.UNICODE)
isEndDefine = lambda line : truth(endDefineRe.match(line))
x23 = lambda arg: arg.replace('#','X23_').replace('-', '_')
