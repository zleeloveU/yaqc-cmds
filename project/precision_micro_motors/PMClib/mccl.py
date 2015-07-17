"""

	NAME
		mccl.h - motion control command language mnemonics & flags

	DESCRIPTION
		Include this header file in your source code to provide mnemonics
		for MCCL commands, status registers, and memory locations. These
		mnemonics make programming with pmccmd() and pmcrpy() easier. This
		file is NOT required for general MCAPI programming.

		from mccl import *

	RELEASE HISTORY
		Copyright (c) 2015 by Precision Micro Control Corp. All rights reserved.

		$Id: mccl.py 921 2015-06-23 18:16:19Z brian $

		Version 4.4.1		23-Jun-15		Programmer: Brian Gaynor
		  - First release

"""

AA			= 133			#  accumulator add 
AB			=  10			#  abort 
AC			= 140			#  accumulator complement 
AD			= 136			#  accumulator divide 
AE			= 143			#  accumulator exclusive or 
AF			= 235			#  auxiliary encoder find index 
AG			= 226			#  set acceleration feed-forward gain 
AH			= 234			#  auxiliary encoder define home 
AI			= 131			#  load accumulator indirect
AL			= 130			#  load accumulator with constanat 
AM			= 135			#  accumulator multiply 
AN			= 141			#  accumulator and 
AO			= 142			#  accumulator or 
AP			= 110			#  adjust position
AR			= 132			#  copy accumulator to register 
AS			= 134			#  Accumulator Subtract 
AT			= 233			#  Auxiliary encoder Tell position 
AV			= 139			#  Accumulator eValuate 
AX			= 180			#  arc center x
AY			= 181			#  arc center y
AZ			= 236			#  auxiliary encoder tell index 
BC			= 324			#  begin compare
BD			= 208			#  backlash distance
BF			= 207			#  backlash off
BK			= 121			#  break 
BM			=  59			#  binary mode
BN			= 206			#  backlash on
BR			=  30			#  baud rate 
CA			= 180			#  arc center absolute 
CB			= 328			#  capture begin
CC			=  70			#  current count 
CD			= 193			#  contour increment distance 
CE			= 311			#  close file
CF			=  31			#  channel off 
CG			= 329			#  capture count
CH			=  66			#  channel high true 
CI			=  32			#  channel in 
CL			=  67			#  channel low true 
CM			=  27			#  set contouring mode 
CN			=  33			#  channel on 
CP			= 192			#  contour path 
CR			= 181			#  arc center relative 
CS			=  71			#  checksum 
CT			=  34			#  channel out 
CX			=  28			#  contouring count
DA			= 219			#  display recorded auxiliary position
DB			= 118			#  set deadband 
DD			= 256			#  display recorded status
DE			= 127			#  debug (dump memory)
DF			= 107			#  do if channel off 
DG			= 227			#  set deceleration feed-forward gain 
DH			=  35			#  define home 
DI			=  36			#  direction 
DL			= 271			#  directory list
DM			=  60			#  decimal mode 
DN			= 106			#  do if channel on 
DO			= 214			#  display recorded optimal position
DQ			= 189			#  display torque
DR			= 213			#  display recorded actual position
DS			= 117			#  deceleration set 
DT			= 197			#  at target delay 
DY			= 190			#  position capture delay
EA			= 187			#  end angle absolute
EE			= 217			#  encoder fault enable
EF			=  37			#  echo off 
EI			= 124			#  enable interrupts
EL			= 228			#  edge latch
EM			=   1			#  execute macro
EN			=  38			#  echo on 
ER			= 188			#  end angle relative
ES			= 229			#  encoder scaling
ET			= 251			#  escape task 
FC			=  64			#  full current 
FD			= 261			#  format double
FE			=  11			#  find edge 
FF			=  51			#  fail input off 
FG			= 313			#  file get 
FI			=  12			#  find index 
FL			= 337			#  digital filter load
FN			=  50			#  fail input on 
FO			= 270			#  format file system
FP			= 312			#  file put 
FR			=  39			#  set derivative sampling period 
FS			= 314			#  file seek
FT			= 260			#  format text
GA			= 248			#  get analog input reading into accumulator 
GB			= 240			#  get byte
GC			= 325			#  compare count
GD			= 246			#  get device ID
GE			= 169			#  go until edge
GF			= 338			#  get digital filter
GH			=  13			#  go home 
GI			= 168			#  go until index
GL			= 242			#  get long
GM			=   8			#  gain mode 
GN			= 166			#  go until coarse on
GO			=  14			#  go 
GP			= 315			#  file get position
GT			= 250			#  generate task 
GU			= 137			#  get user axis
GW			= 241			#  get word
GX			= 247			#  get auxiliary encoder position into accumulator 
HC			=  65			#  half current 
HE			=  72			#  help 
HF			=  48			#  RS232 module handshake off 
HL			= 211			#  set motion high limit 
HM			=  61			#  hex mode 
HN			=  49			#  RS232 module handshake on 
HO			=  15			#  home
HS			= 232			#  high speed 
IA			=  93			#  index arm 
IB			= 165			#  if accumulator below (less then) 
IC			= 161			#  if bit clear in accumulator 
MC_ID		= 218			#  information display
IE			= 162			#  if accumulator equal 
IF			= 109			#  if channel off then, else skip two 
IG			= 164			#  if accumulator greater than 
II			=  68			#  if intermediate 
IL			=  40			#  set integration limit 
IM			= 114			#  input mode
MC_IN		= 108			#  if channel on ... - WIN32 safe version
IO			= 205			#  integral option
IP			=  96			#  interrupt on absolute position 
IR			=  97			#  interrupt on relative position 
IS			= 160			#  if bit set in accumulator 
IU			= 163			#  if accumulator unequal 
IX			=  95			#  if contouring
JA			=  56			#  jog acceleration 
JB			= 223			#  jog deadband 
JC			=  59			#  jog channel (mfx-eth)
JD			= 221			#  jog derivative gain
JF			=  58			#  jog off 
JG			= 220			#  jog gain 
JN			=  57			#  jog on 
JO			= 222			#  jog offset 
JP			=   6			#  jump to command absolute 
JR			=   7			#  jump to command relative 
JV			=  55			#  jog velocity 
LA			= 330			#  load commutation phase shift A
LB			= 331			#  load commutation phase shift B
LC			= 322			#  load compare
LD			= 333			#  load commutation divisor constant
LE			= 332			#  load commutation prescale constant
LF			=  54			#  limit switch off 
LI			= 111			#  learn incrementing
LL			= 210			#  set motion low limit 
LM			=  52			#  limit switch mode 
LN			=  53			#  limit switch on
LO			= 274			#  load file
LP			= 112			#  learn position 
LR			= 334			#  load commutation repeat count
LS			= 230			#  low speed 
LT			= 113			#  learn target 
LU			= 129			#  look up
MA			=  16			#  move absolute
MC			=   2			#  macro command
MD			=   3			#  macro definition
MF			=  17			#  motor off
MI			=  18			#  move incrementing
MJ			=   5			#  macro jump
MN			=  19			#  motor on 
MP			=  20			#  move to point 
MR			=  21			#  move relative 
MS			= 231			#  medium speed 
MV			= 196			#  set minimum velocity 
NC			= 323			#  compare increment
NF			= 336			#  digital filter off
NO			= 120			#  no operation 
NP			= 252			#  new priority
NS			= 171			#  no syncronization 
OA			= 249			#  output analog value from accumulator 
OB			= 195			#  output deadband (dcx, dc4)
OC			= 320			#  compare output mode
OF			= 310			#  open file
OM			= 216			#  set output mode 
OO			= 203			#  output offset
OP			= 321			#  compare output period
PA			= 217			#  position capture arm
PB			= 243			#  put byte
PC			= 128			#  prompt character 
PD			= 293			#  pen down macro
PE			= 281			#  plot enable
PF			= 280			#  plot file
PH			= 115			#  set phasing 
PI			= 291			#  plotter initialize macro
PK			= 204			#  pwm time constant
PL			= 245			#  put long
PM			=  23			#  position mode 
PP			= 237			#  profile parabolic
PQ			= 290			#  plot quick velocity
PR			= 212			#  position recording
PS			= 238			#  profile s-curve 
PT			= 239			#  profile trapezoidal 
PU			= 292			#  pen up macro
PV			= 288			#  plotter velocity
PW			= 244			#  put word
PX			= 282			#  plotter x axis
PY			= 283			#  plotter y axis
QM			=   9			#  torque mode 
RA			= 131			#  accumulator load with register 
RB			= 150			#  read accumulator Byte 
RC			= 277			#  restore configuration 
RD			= 147			#  read accumulator double (64 bit floating point) 
RF			= 273			#  remove file
RI			= 191			#  position record interval
RL			= 152			#  read accumulator long 
RM			=   4			#  reset macros 
RP			= 100			#  repeat 
RR			= 182			#  arc radius
RT			=  42			#  reset system 
RV			= 146			#  read accumulator float (32 bit floating point) 
RW			= 151			#  read accumulator word 
RX			= 184			#  radius x
RY			= 185			#  radius y
SA			=  43			#  set acceleration 
SB			= 122			#  select bank
SC			= 276			#  save configuration 
SD			=  44			#  set derivative gain 
SE			=  25			#  stop on error 
SF			=  62			#  step full 
SG			=  45			#  set gain 
SH			=  63			#  step Half 
SI			=  46			#  set integral gain 
SL			= 144			#  accumulator shift left 
SM			=  26			#  set master 
SN			= 170			#  syncroniztion on 
SO			= 300			#  set offset of MFX-ETH digital pots
SP			= 294			#  select pen macro
SQ			= 116			#  set torque 
SR			= 145			#  accumulator shift right 
SS			=  29			#  set slave ratio 
ST			=  22			#  stop 
SV			=  47			#  set velocity 
TA			=  73			#  tell a/d 
TB			=  91			#  tell breakpoint position 
TC			=  74			#  tell channel 
TD			=  75			#  tell derivative gain 
TE			=  76			#  tell error
TF			=  77			#  tell following error 
TG			=  78			#  tell position gain 
TI			=  79			#  tell integral gain 
TK			=  92			#  tell velocity constant 
TL			=  80			#  tell integration limit 
TM			=  81			#  tell macros 
TO			=  89			#  tell optimal 
TP			=  82			#  tell position 
TQ			= 209			#  tell torque 
TR			=  87			#  tell register 
TS			=  83			#  tell status 
TT			=  84			#  tell target 
TV			=  85			#  tell velocity 
TX			=  88			#  tell contouring count 
TY			= 272			#  type file
TZ			=  90			#  tell index 
UA			= 156			#  use axis
UC			= 159			#  user command
UK			= 215			#  set user output constant 
UL			= 158			#  user load
UO			= 179			#  set user offset 
UR			= 177			#  set user rate conversion 
US			= 175			#  set user scale 
UT			= 178			#  set user time conversion 
UZ			= 176			#  set user zero 
VA			= 173			#  vector acceleration 
VD			= 174			#  vector deceleration 
VE			=  86			#  tell version 
VG			= 119			#  set velocity gain 
VM			=  24			#  velocity mode 
VO			= 224			#  set velocity override 
VV			= 172			#  vector velocity 
WA			= 101			#  wait (time) 
WB			= 153			#  write accumulator byte 
WD			= 149			#  write accumulator double (64 bit floating point) 
WE			= 102			#  wait edge 
WF			= 103			#  wait for channel off 
WI			=  94			#  wait for index 
WL			= 155			#  write accumulator long 
WN			= 104			#  wait for channel on 
WP			=  98			#  wait for absolute position 
WR			=  99			#  wait for relative position 
WS			= 105			#  wait for stop 
WT			= 198			#  wait for target 
WV			= 148			#  write accumulator float (32 bit floating point) 
WW			= 154			#  write accumulator word 
XF			= 126			#  set xoff character 
XN			= 125			#  set xon character 
XO			= 286			#  plotter x offset
XS			= 284			#  plotter x scale
YF			= 335			#  digital filter on
YH			= 257			#  trajectory rate high
YL			= 259			#  trajectory rate low
YM			= 258			#  trajectory rate medium
YO			= 287			#  plotter y offset
YS			= 285			#  plotter y scale
ZF			= 339			#  zero digital filter
