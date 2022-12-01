from lex import *
import re

variablesList = []

# remove comments from lexeme table
def removeComments(lexTable):
    lexemes_list2 = []          # store lexemes that are not comments 
    
    for lexeme in lexTable: 
        # if description of lexeme is related to comments, ignore it 
        if (str(lexeme[1]) not in ["Single-Line Comment Delimiter", "Comment Literal", "Multi-Line Comment Delimiter"]):
            lexemes_list2.append(lexeme)

    return lexemes_list2

def assign(lexemesList, varName):
    lexemesList.pop(0)

    # SUM OF, DIFF OF, PRODUKT OF, QUOSHUNT OF, MOD OF, BIGGR OF, SMALLR OF
    if (lexemesList[0][1] in arithmeticKeywords):              
        addVariable(varName, arithmeticOp(lexemesList))

    # BOTH OF, EITHER OF, WON OF, NOT, ALL OF, ANY OF 
    elif (lexemesList[0][1] in boolKeywords):
        print("im here")
        addVariable(varName, booleanOperations(lexemesList))
        # print(booleanOperations(lexemesList))

    # BOTH SAEM, DIFFRINT
    elif (lexemesList[0][1] in compareKeywords): 
        addVariable(varName, comparisonOperators(lexemesList))

    # if value is an integer/numbr, float/numbar, or boolean/troof literal
    elif (lexemesList[0][1] in ["NUMBR Type Literal", "NUMBAR Type Literal", "TROOF Type Literal"]):
        addVariable(varName, lexemesList.pop(0)[0])

    # if value is a string/yarn literal
    elif (lexemesList[0][1] == "String Delimiter"):
        lexemesList.pop(0)           # pop starting double quote 
        value = lexemesList.pop(0)[0]    # pop string literal 
        lexemesList.pop(0)           # pop ending double quote 
        addVariable(varName, value)
    
    elif (lexemesList[0][1] in "Variable Identifier"):
        addVariable(varName, findVar(lexemesList.pop(0)[0]))

    elif (lexemesList[0][1] == "Typecast Keyword"):
        addVariable(varName, typecast(lexemesList))

def arithmeticOperations(operations, op1, op2):
    # determine data type of operands 
    if (("." in str(op1)) or ("." in str(op2))):
        op1 = float(op1)
        op2 = float(op2)
    else: 
        op1 = int(op1)
        op2 = int(op2)

    # determine operators
    if (operations[1] == "Addition Operator"):
        return op1 + op2

    elif (operations[1] == "Subtraction Operator"):
        return op1 - op2

    elif (operations[1] == "Multiplication Operator"):
        return op1 * op2

    elif (operations[1] == "Quotient Operator"):
        return op1 // op2

    elif (operations[1] == "Modulo Operator"):
        return op1 % op2

    elif (operations[1] == "Max Operator"):
        return max(op1, op2)

    elif (operations[1] == "Min Operator"):
        return min(op1, op2)

def arithmeticOp(lexemesList):
    operations = []

    # for (nested) operations
    while (lexemesList[0][1] in arithmeticKeywords): 
        operations.append(lexemesList.pop(0))
    
    # GET FIRST OPERAND
    # if value is an integer/numbr, float/numbar, or boolean/troof literal
    if (lexemesList[0][1] in ["NUMBR Type Literal", "NUMBAR Type Literal", "TROOF Type Literal"]):
        firstOp = lexemesList.pop(0)[0]

    # if value is a string/yarn literal
    elif (lexemesList[0][1] == "String Delimiter"):
        lexemesList.pop(0)           # pop starting double quote 
        firstOp = lexemesList.pop(0)[0]    # pop string literal 
        lexemesList.pop(0)           # pop ending double quote 

    # if operand is a variable 
    elif (lexemesList[0][1] == "Variable Identifier"):
        temp = lexemesList.pop(0)

        # find variable name 
        firstOp = findVar(temp[0])

    # if operand is a typecast keyword
    elif(lexemesList[0][1] == "Typecast Keyword"):
        firstOp = typecast(lexemesList)

    # PERFORM OPERATIONS 
    while operations: 
        result = arithmeticOperations(operations.pop(0), firstOp, getSecondOp(lexemesList))
    
    return result 

def getSecondOp(lexemesList):
    if lexemesList[0][1] != "Operator Delimiter":           # AN
        return 
        
    else: 
        lexemesList.pop(0)   # pop "AN" (operator delimiter)

        # if value is an integer/numbr, float/numbar, or boolean/troof literal
        if (lexemesList[0][1] in ["NUMBR Type Literal", "NUMBAR Type Literal", "TROOF Type Literal"]):
            return(lexemesList.pop(0)[0])

        # if value is a string/yarn literal
        elif (lexemesList[0][1] == "String Delimiter"):
            lexemesList.pop(0)           # pop starting double quote 
            value = lexemesList.pop(0)[0]    # pop string literal 
            lexemesList.pop(0)           # pop ending double quote 
            return(value)

        # if operand is a variable 
        elif (lexemesList[0][1] == "Variable Identifier"):
            temp = lexemesList.pop(0)

            # find variable name 
            for variable in variablesList:
                if (variable[0] == temp[0]):
                    return (variable[1])

        elif (lexemesList[0][1] in arithmeticKeywords):
            return (arithmeticOp(lexemesList))

        elif (lexemesList[0][1] in boolKeywords):
            return (booleanOperations(lexemesList))

        elif (lexemesList[0][1] in compareKeywords):
            return (comparisonOperators(lexemesList))

        elif(lexemesList[0][1] == "Typecast Keyword"):
            return (typecast(lexemesList))

    return("Invalid syntax: invalid second operator")

def booleanOperations(lexemesList):
    operations = []

    # for (nested) operations
    while (lexemesList[0][1] in boolKeywords): 
        operations.append(lexemesList.pop(0))
    
    # GET FIRST OPERAND
    # if operand is a literal 
    if (lexemesList[0][1] == "TROOF Type Literal"):
        firstOp = lexemesList.pop(0)[0]

    # if operand is a variable 
    elif (lexemesList[0][1] == "Variable Identifier"):
        temp = lexemesList.pop(0)

        # find variable name 
        firstOp = findVar(temp[0])

    # if operand is a typecast keyword
    elif (lexemesList[0][1] == "Typecast Keyword"):
        firstOp = typecast(lexemesList)

    elif (lexemesList[0][1] in compareKeywords):
        firstOp = comparisonOperators(lexemesList)

    return boolProcess(operations, firstOp, lexemesList)

def boolProcess (operations, x, lexemesList):
    x = lolToBool(x)

    if operations[0][1] == "Infinite Arity And Operator":             # ALL OF 
        while lexemesList[0][1] == "Operator Delimiter":
            y = getSecondOp(lexemesList)
            x = x and lolToBool(y)
        return boolToLol(x)

    elif operations[0][1] == "Infinite Arity Or Operator":          # ANY OF 
        while lexemesList[0][1] == "Operator Delimiter":
            y = getSecondOp(lexemesList)
            x = x or lolToBool(y)
        return boolToLol(x)

    else: 
        while operations:
            currOperation = operations.pop(0)
            y = getSecondOp(lexemesList)

            if currOperation[1] == "And Operator":
                x = x and lolToBool(y)

            elif currOperation[1] == "Or Operator":
                x = x or lolToBool(y)

            elif currOperation[1] == "Xor Operator":
                x = x ^ lolToBool(y)

            elif currOperation[1] == "Boolean Not Operator":
                x = not x
        return boolToLol(x)

def lolToBool(x):
    if x == "WIN":
        return True
    elif x == "FAIL": 
        return False

def boolToLol(x):
    if x == True:
        return "WIN"
    elif x == False: 
        return "FAIL"

def comparisonOperators(lexemesList):
    operations = []

    # for (nested) operations
    while (lexemesList[0][1] in compareKeywords): 
        operations.append(lexemesList.pop(0))
    
    curr = lexemesList.pop(0)
    # GET FIRST OPERAND
    # if operand is a literal 
    if (curr[1] in ["NUMBR Type Literal", "NUMBAR Type Literal"]):
        firstOp = lexemesList.pop(0)[0]

    # if operand is a variable 
    elif (curr[1] == "Variable Identifier"):
        temp = lexemesList.pop(0)

        # find variable name 
        firstOp = findVar(temp[0])

    # boolean operations 
    elif (curr[1] in boolKeywords):
        firstOp = booleanOperations(lexemesList)

    # arithmetic operations
    elif (curr[1] in arithmeticKeywords):
        firstOp = arithmeticOp(lexemesList)

    # if operand is a typecast keyword
    elif (curr[1] == "Typecast Keyword"):
        firstOp = typecast(lexemesList)

    return compareProcess(operations, firstOp, lexemesList)

def compareProcess(operations, x, lexemesList):
    while operations:
        if operations[0][1] == "Equal Operator":            # BOTH SAEM
            result = (x == getSecondOp(lexemesList))

        elif operations[0][1] == "Not Equal Operator":      # DIFFRINT
            result = (int(x) != int(getSecondOp(lexemesList)))
        operations.pop(0)

    return boolToLol(result)

def typecast(lexemesList):
    value = lexemesList.pop(0)
    explicitCast = 0

    # MAEK var1 A NUMBAR 
    if (value[0] == "MAEK"):
        value = lexemesList.pop(0)
        explicitCast = 1
    
    # CHECK IF IT IS A VARIABLE OR LITERAL
    # if value is a variable 
    if (value[1] == "Variable Identifier"):
        value = findVar(value[0])

    # if value is an integer/numbr, float/numbar, or boolean/troof literal
    elif (value[1] in ["NUMBR Type Literal", "NUMBAR Type Literal", "TROOF Type Literal"]):
        value = lexemesList.pop(0)[0]

    # if value is a string/yarn literal
    elif (value[1] == "String Delimiter"):
        lexemesList.pop(0)           # pop starting double quote 
        value = lexemesList.pop(0)[0]    # pop string literal 
        lexemesList.pop(0)           # pop ending double quote 

    if (lexemesList[0][0] in ["IS NOW A", "A"]):
        lexemesList.pop(0)

    # PROCESS TYPECASTING 

    # typecast to int/numbr (allowable from bool/troof, uninit/noob, float/numbar, string/yarn)
    if (lexemesList[0][1] == "NUMBR Type Literal"):
        lexemesList.pop(0)
        if (value == "WIN"):
            return(1)
        elif ((value == "FAIL") or ((explicitCast == 1) and (value == "NULL"))):
            return(0)
        elif ("." in value):
            return(int(value))
        elif (bool(re.match(r"[-+]?\d+(\.0*)?$", value))):
            return(int(value))
        
    # typecast to float/numbar (allowable from bool/troof, uninit/noob, int/numbr, string/yarn)
    if (lexemesList[0][1] == "NUMBAR Type Literal"):
        lexemesList.pop(0)
        if (value == "WIN"):
            return(1.0)
        elif ((value == "FAIL") or ((explicitCast == 1) and (value == "NULL"))):
            return(0.0)
        elif(isinstance(value, int)):
            return(float(value))
        elif(bool(re.match(r"[-+]?\d+(\.0*)?$", value))):
            return(float(value))

    # typecast to bool/troof (allowable from uninit/noob, string/yarn, int/numbr, float/numbar)
    if (lexemesList[0][1] == "TROOF Type Literal"):
        lexemesList.pop(0)
        if (value in ["NULL", "", 0, 0.0]):
            return("FAIL")
        else: 
            return("WIN")

    # typecast to string/yarn
    if (lexemesList[0][1] == "YARN Type Literal"):
        if ("." in value):
            return(str(round(value, 2)))
        elif (value == "NULL"):
            return("")
        else:
            return(str(value))


def findVar(variableName):
    # find variable name 
    for variable in variablesList:
        if (variable[0] == variableName):
            value = variable[1]
            break
    return value 

def variableAssignment(lexemesList):
    lexeme = lexemesList.pop(0)

    # check if next lexeme is a valid variable name (uninitialized)
    if (lexeme[1] == "Variable Identifier"):
        variableName = lexeme[0]

        # check if next lexeme in the list is "ITZ" (intiialization)
        if (lexemesList[0][1] == "Variable Assignment"):
            lexemesList.pop(0)           # pop "ITZ" keyword and proceed 
            
            # LITERALS
            # if value is an integer/numbr, float/numbar, or boolean/troof literal
            if (lexemesList[0][1] in ["NUMBR Type Literal", "NUMBAR Type Literal", "TROOF Type Literal"]):
                temp = lexemesList.pop(0)
                value = temp[0]
                return (variableName, value)

            # if value is a string/yarn literal
            elif (lexemesList[0][1] == "String Delimiter"):
                lexemesList.pop(0)           # pop starting double quote 
                temp = lexemesList.pop(0)    # pop string literal 
                value = str(temp[0])
                lexemesList.pop(0)           # pop ending double quote 
                return (variableName, value)

            # TYPECAST KEYWORD 
            elif(lexemesList[0][1] == "Typecast Keyword"):
                typecast(lexemesList)

            # VALUE OF ANOTHER VARIABLE 
            # if value is a variable 
            elif (lexemesList[0][1] == "Variable Identifier"):
                temp = lexemesList.pop(0)

                value = findVar(temp[0])
                return (variableName, value)  
                            
            # RESULT OF AN EXPRESSION
            elif (lexemesList[0][1] in arithmeticKeywords):
                value = arithmeticOp(lexemesList)

                return (variableName, value)

            else: 
                return("Invalid syntax: variable initialization")
        else: 
            return((variableName, "NULL"))

    else:
        return ("Invalid syntax: variable declaration")

def addVariable(variableName, newVal):
    temp = 0
    for i in range(len(variablesList)):
        if (variablesList[i][0] == variableName):
            variablesList.pop(i)
            # variablesList[i][1] = newVal[0]
            break
        temp += 1
    variablesList.insert(temp, (variableName, newVal))

def ifThenState(lexemesList):
    isMatch = False

    while lexemesList: 
        if lexemesList[0][1] == "If Keyword":               # YA RLY
            lexemesList.pop(0)
            if (findVar("IT") == "WIN"):
                foundCond(lexemesList)
                isMatch = True 
            
            else: 
                while lexemesList:
                    if(lexemesList[0][1] in ["Else Keyword", "End of If-then"]):
                        break
        
        if ((lexemesList[0][1] == "Else Keyword") and isMatch == False): 
            lexemesList.pop(0)
            foundCond(lexemesList)
            isMatch = True 
        
        if isMatch == True:
            while lexemesList[0][1] == "End of If-then":
                lexemesList.pop(0)
            lexemesList.pop(0)
            break                   # exit while loop
        lexemesList.pop(0)

def foundCond(lexemesList):
    ifThenStatements = []

    while lexemesList[0][1] not in ["Else Keyword", "End of If-then"]:
        ifThenStatements.append(lexemesList.pop(0))
    
    getStatements(ifThenStatements)


def switchCase(lexemesList):
    caseCond = 0
    isMatch = False 

    while lexemesList[0][1] != "End of If-then":            # OIC keyword
        if (lexemesList[0][1] == "Case Delimiter"):                        # case keyword 
            lexemesList.pop(0)                  
        
            # CHECK CONDITION OF EACH CASE (literal or variable)
            if (lexemesList[0][1] in literalKeywords):
                caseCond = lexemesList.pop(0)[0]
            elif (lexemesList[0][1] == "Variable Identifier"):
                temp = lexemesList.pop(0)
                caseCond = findVar(temp[0])

            # check if IT variable matches case conditon 
            if (caseCond == findVar("IT")):
                foundCase(lexemesList)
                isMatch = True 
            
        elif (lexemesList[0][1] == "Default Case Keyword"):
            isMatch = True 
            foundCase(lexemesList)

        if isMatch == True:
            while lexemesList[0][1] != "End of If-then":
                lexemesList.pop(0)
            lexemesList.pop(0)          # pop "OIC" keyword
            break                       # break while loop
        lexemesList.pop(0)

def foundCase(lexemesList):
    caseStatements = []

    while lexemesList[0][1] not in ["Case Delimiter", "Default Case Keyword", "End of If-then"]:
        caseStatements.append(lexemesList.pop(0))
    
    getStatements(caseStatements)

# parse lexemes 
def parse(lexTable, userInput):
    startFlag = False       # flag if the start of the program has been detected 
    cleanLex = []
    variablesList.clear()

    # CHECK FOR COMMENTS (not considered as statements)
    cleanLex = removeComments(lexTable)         # remove comments since it will only be ignored 

    # CHECK FOR "HAI"
    if (cleanLex[0][1] == "Start of Program"):         # if the first element in the list is the "HAI" keyword (start of program)
        cleanLex.remove(cleanLex[0])                                # remove "HAI" from list 
        if (cleanLex[0][1] in ["NUMBR Type Literal", "NUMBAR Type Literal"]):                           # check if "HAI" keyword contains a version number 
            cleanLex.remove(cleanLex[0])                            # remove "HAI" version from list 
    else: 
        return("Invalid Syntax: no HAI keyword")

    # CHECK FOR "KTHXBYE"
    if (cleanLex[len(cleanLex) - 1][1] == "End of Program"):        # if the last element in the list is the "KTHXBYE" keyword (end of program) 
        cleanLex.remove(cleanLex[len(cleanLex) - 1])                # remove "KTHXBYE" from list 
    else: 
        return("Invalid Syntax: no KTHXBYE keyword")

    return getStatements(cleanLex)

def getStatements(cleanLex):
    # iterate over statements in the code 
    while cleanLex: 
        lexeme = cleanLex.pop(0)
        token = lexeme[0]
        tokenDesc = lexeme[1]

        # if statement is a variable declaration
        if (tokenDesc == "Variable Declaration"):           # I HAS A
            variablesList.append(variableAssignment(cleanLex))

        elif (token == "MAEK"):                             # MAEK
            addVariable("IT", typecast(cleanLex))
        
        # IF-THEN STATEMENTS 
        elif (tokenDesc == "Start of If-then Delimiter"):    # O RLY?
            ifThenState(cleanLex)

        # SWITCH CASES
        elif (tokenDesc == "Start of Switch-case"):         # WTF?
            switchCase(cleanLex)

        elif (token == "GTFO"):                              # GTFO
            break

        else: 
            if (cleanLex):
                if (cleanLex[0][1] == "Assignment Operation"):          # R
                    assign(cleanLex, token)

                # SUM OF, DIFF OF, PRODUKT OF, QUOSHUNT OF, MOD OF, BIGGR OF, SMALLR OF
                if (tokenDesc in arithmeticKeywords):              
                    addVariable("IT", arithmeticOp(cleanLex))

                # BOTH OF, EITHER OF, WON OF, NOT, ALL OF, ANY OF 
                elif (tokenDesc in boolKeywords):
                    cleanLex.insert(0, (token, tokenDesc))
                    addVariable("IT", booleanOperations(cleanLex))

                # BOTH SAEM, DIFFRINT
                elif (tokenDesc in compareKeywords): 
                    cleanLex.insert(0, (token, tokenDesc))
                    addVariable("IT", comparisonOperators(cleanLex))

                elif (cleanLex[0][0] == "IS NOW A"):
                    addVariable("IT", typecast(cleanLex))

    print(variablesList)

    return variablesList