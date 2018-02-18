import os

dir = os.path.join('..', 'textdocs')
f1 = open(os.path.join(dir, 'instructionlist.txt'))
f2 = open(os.path.join(dir, 'programming-the-VM', 'SBTCVM-asm.txt'))

instrs = []
for line in f1:
	if '|' in line:
		#print line
		instrs.append(line)

#instrs.append('++++++|missinst.py debug: shouldn\'t find this')
#print instrs

# code = instrs[n][0:6]

asmtxt = f2.read()
badinst = []
for instr in instrs:
	if not '\n'+instr[0:6] in asmtxt:
		badinst.append(instr)

print 'Instructions not found:'
for instr in badinst:
	print instr,
