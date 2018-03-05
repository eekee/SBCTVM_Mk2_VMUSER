#!/usr/bin/env python
import VMSYSTEM.libbaltcalc as btcalc
import sys

# option maybes:
# -d n	set dot at start, for recursive invocation
# -t	run self-tests [undocumented]

# self-tests:
# warn if instructions are not unique (catch mis-paste)




# constants
WORDSIZE = 9

# major global variables
lino = 0
dot = 0

def lifitri(trits, fill=WORDSIZE, lim=-1, char='0'):
	# limit/fill trits to certain lengths
	if lim == -1:
		lim = fill
	int = btcalc.BTTODEC(trits)
	if abs(int) > btcalc.mpi(lim):
		XXerrorXX
	#return trits.rjust(fill, char)  # obsolete
	return ('{:' + char + '>' + str(fill) + '}').format(trits)

# parse trits, decimal, character, ...
def parsedata(d):
	if d == '':
		return '0'
	c = d[0]
	if c == "'":
		XXcharacterXX
	if c == '$':
		XXdecimalXX
	if c == '~':
		XXtritsXX
	XXsymbolXX

###################################
### data parsing words

def data(d):
	return lifitri(parsedata(d))

def nodata(d):
	if d != '':
		XXerrorXX
	return lifitri('0')

def data6(d):
	return lifitri(parsedata(d), lim=6)

def data2(d):
	return lifitri(parsedata(d), lim=2)

def xy3data(d):
	# xxxyyy

def monodata(d):
	# xxyymm

def xy2data(d):
	# xxyy??

def timedata(d):
	# see ../textdocs/programming-the-VM/SBTCVM-asm.txt:/wait

def databool(d):
	# just 0 or + in the low trit

def offsetlendata(d):


###################################
### tables

symbols = {
	'enter': '000-0-000',
	'space': '000-0-00+',
}

# instruction lookup note:
# compare [tupe[1].__class__ == ''.__class__] to see if it's a string.

instructions = {
	'romread1': ('------', data),
	'romread2': ('-----0', data),
	'IOread1': ('-----+', data),
	'IOread2': ('----0-', data),
	'IOwrite1': ('----00', data),
	'IOwrite2': ('----0+', data),
	'regswap': ('----+-', nodata),
	'copy1to2': ('----+0', nodata),
	'copy2to1': ('----++', nodata),
	'invert1': ('---0--', nodata),
	'invert2': ('---0-0', nodata),
	'add': ('---0-+', nodata),
	'subtract': ('---00-', nodata),
	'multiply': ('---000', nodata),
	'divide': ('---00+', nodata),
	'setreg1': ('---0+-', data),
	'setreg2': ('---0+0', data),
	'setinst': ('---0++', data),
	'setdata': ('---+--', data),
	'continue': ('---+++', nodata),
	'colorpixel': ('--0---', xy3data),
	'setcolorreg': ('--0--0', data6),
	'colorfill': ('--0--+', data6),
	'setcolorvect': ('--0-0-', xy3data),
	'colorline': ('--0-00', xy3data),
	'colorrect': ('--0-0+', xy3data),
	'monopixel': ('--0-+-', monodata),
	'monofill': ('--0-+0', data2),
	'setmonovect': ('--0-++', xy2data),
	'monoline': ('--00--', monodata),
	'monorect': ('--00-0', monodata),
	'stop': ('--000-', nodata),
	'null': ('000000', nodata),
	'gotodata': ('--000+', data),
	'gotoreg1': ('--00+-', nodata),
	'gotodataif': ('--00+0', data),
	'gotoifgreater': ('--0+0-', data),
	'wait': ('--00++', timedata),
	'YNgoto': ('--0+--', data),
	'userwait': ('--0+-0', nodata),
	'TTYclear': ('--0+-+', nodata),
	'gotoa': ('--+---', data),
	'gotoaif': ('--+--0', data),
	'gotob': ('--+--+', data),
	'gotobif': ('--+-0-', data),
	'gotoc': ('--+-00', data),
	'gotocif': ('--+-0+', data),
	'gotod': ('--+-+-', data),
	'gotodif': ('--+-+0', data),
	'gotoe': ('--+-++', data),
	'gotoeif': ('--+0--', data),
	'gotof': ('--+0-0', data),
	'gotofif': ('--+0-+', data),
	'dumpreg1': ('--++0+', nodata),
	'dumpreg2': ('--+++-', nodata),
	'setregset': ('-0-000', data),
	'regset': ('-0-00+', data),
	'TTYwrite': ('--+++0', data),
	'buzzer': ('--++++', data),
	'setkeyint': ('-0-+++', data6),
	'keyint': ('-00---', data),
	'clearkeyint': ('-00--0', databool),
	'offsetlen': ('-0-++0', offsetlendata),
	'ptset': ('-0-0+-', '-+0000000'),
	'ptget': ('-0-0+-', '000000000'),
	'ptinc': ('-0-0+-', '--0000000'),
	'ptdec': ('-0-0+-', '-00000000'),
	'ptadd': ('-0-0+-', '0-0000000'),
	'ptread': ('-0-0+0', nodata),
	'ptwri': ('-0-0++', nodata),
	'ptwrite': ('-0-0++', nodata),
	'ptwridat': ('-0-+--', data),
# threadref threadstart & threadkill
# probably want data2, but i'm not sure
	'threadref': ('--+00-', data),
	'threadstart': ('--+000', data),
	'threadstop': ('--+00+', nodata),
	'threadkill': ('--+0+-', data),
}

#	|tr A-Z a-z
macros = {
	'TTYlinedraw': ttylinedraw,
	'TTYbg': ttybg,
	'textstart': textstart,
}