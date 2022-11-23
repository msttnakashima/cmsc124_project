# contains all regular expressions

import re

# ==== IDENTIFIERS ====  

# Variable Identifier
varident = re.compile("^[A-Za-z]+[A-Za-z0-9_]*$")


# ==== LITERALS ==== 

# NUMBR Literal
numbr = re.compile("^\-?[0-9]+$")

# NUMBAR Literal
numbar = re.compile("^\-?[0-9]+\.[0-9]+$")

# YARN Literal
yarn = re.compile("^\"[^\"]*\"$")

# TROOF Literal
troof = re.compile("^(WIN|FAIL)$")

# TYPE Literal
type_literal = re.compile("^(YARN|NUMBR|NUMBAR|TROOF|NOOB)$")


list_literals = [numbr, numbar, yarn, troof, type_literal]

# ==== KEYWORDS ====

# start and end of the program
HAI = re.compile("^HAI$")               # start of program       
KTHXBYE = re.compile("KTHXBYE$")        # end of program 

# comments (single-line and muti-line)
BTW = re.compile("^BTW$")               # single-line comment
OBTW = re.compile("^OBTW$")             # multi-line comment 
TLDR = re.compile("^TLDR$")             # multi-line comment 

# declaration
I_HAS_A = re.compile("^I HAS A$")       # uninitialized variable
ITZ = re.compile("^ITZ$")               # initialized
R = re.compile("^R$")                   # initialized 

# arithmetic / mathematical operations
AN = re.compile("^AN$")                     # separate operands for arithmetic operations
SUM_OF = re.compile("^SUM OF$")             # addition
DIFF_OF = re.compile("^DIFF OF$")           # subtraction
PRODUKT_OF = re.compile("^PRODUKT OF$")     # multiplication
QUOSHUNT_OF = re.compile("^QUOSHUNT OF$")   # division (quotient)
MOD_OF = re.compile("^MOD OF$")             # division (remainder)
BIGGR_OF = re.compile("^BIGGR OF$")         # max value
SMALLR_OF = re.compile("^SMALLR OF$")       # min value 

# boolean operations
BOTH_OF = re.compile("^BOTH OF$")           # and
EITHER_OF = re.compile("^EITHER OF$")       # or 
WON_OF = re.compile("^WON OF$")             # xor 
NOT = re.compile("^NOT$")                   # not 
ANY_OF = re.compile("^ANY OF$")             # infinite arity and 
ALL_OF = re.compile("^ALL OF$")             # infinite arity or 

# comparison operations 
BOTH_SAEM = re.compile("^BOTH SAEM$")       # equal ("==")
DIFFRINT = re.compile("^DIFFRINT$")         # not equal ("!=")

# concatenation
SMOOSH = re.compile("^SMOOSH$")             # string concatenation

# casting
MAEK = re.compile("^MAEK$")                 # explicit typecasting                 
A = re.compile("^A$")                       
IS_NOW_A = re.compile("^IS NOW A$")         

# input / output
VISIBLE = re.compile("^VISIBLE$")           # prints to terminal
GIMMEH = re.compile("^GIMMEH$")             # accepts input

# flow control statements: if-then
O_RLY = re.compile("^O RLY\\?$")            # start of if-then
YA_RLY = re.compile("^YA RLY$")             # if-clause
MEBBE = re.compile("^MEBBE$")               # else-if clause
NO_WAI = re.compile("^NO WAI$")             # else-clause
OIC = re.compile("^OIC$")                   # end of if-then

# flow control statements: switch-case
WTF = re.compile("^WTF\\?$")                # start of switch-case
OMG = re.compile("^OMG$")                   # denotes each case
OMGWTF = re.compile("^OMGWTF$")             # default case
GTFO = re.compile("^GTFO$")                 # break

# loops
IM_IN_YR = re.compile("^IM IN YR$")         # start of loop
UPPIN = re.compile("^UPPIN$")               # increment 
NERFIN = re.compile("^NERFIN$")             # decrement
YR = re.compile("^YR$")                     
TIL = re.compile("^TIL$")                   # loop termination (for)
WILE = re.compile("^WILE$")                 # loop termination (while)
IM_OUTTA_YR = re.compile("^IM OUTTA YR$")   # end of loop

list_keywords = [HAI, KTHXBYE, BTW, OBTW, TLDR, I_HAS_A, ITZ, R, 
SUM_OF, DIFF_OF, PRODUKT_OF, QUOSHUNT_OF, MOD_OF, BIGGR_OF, SMALLR_OF,
BOTH_OF, EITHER_OF, WON_OF, NOT, ANY_OF, ALL_OF, BOTH_SAEM, DIFFRINT, SMOOSH,
MAEK, A, IS_NOW_A, VISIBLE, GIMMEH, O_RLY, YA_RLY, MEBBE, NO_WAI, OIC,
WTF, OMG, OMGWTF, IM_IN_YR, UPPIN, NERFIN, YR, TIL, WILE, IM_OUTTA_YR]