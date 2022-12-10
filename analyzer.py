from lexical import *
import re

variablesList = []
printToTerminal = []

# remove comments from lexeme table
def removeComments(lexTable):
    lexemes_list2 = []          # store lexemes that are not comments 
    
    for lexeme in lexTable: 
        # if description of lexeme is related to comments, ignore it 
        if (str(lexeme[1]) not in ["Single-Line Comment Delimiter", "Comment Literal", "Multi-Line Comment Delimiter"]):
            lexemes_list2.append(lexeme)

    return lexemes_list2

# assign a value 
def assign(lexemesList, varName):
    lexemesList.pop(0)

    # SUM OF, DIFF OF, PRODUKT OF, QUOSHUNT OF, MOD OF, BIGGR OF, SMALLR OF
    if (lexemesList[0][1] in arithmeticKeywords):              
        addVariable(varName, arithmeticOp(lexemesList))

    # BOTH OF, EITHER OF, WON OF, NOT, ALL OF, ANY OF 
    elif (lexemesList[0][1] in boolKeywords):
        # print("im here")
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
    
    # if value is another variable
    elif (lexemesList[0][1] in "Variable Identifier"):
        temp = findVar(lexemesList.pop(0)[0])
        addVariable(varName, temp)

    # if the value is first typecasted 
    elif (lexemesList[0][1] == "Typecast Keyword"):
        addVariable(varName, typecast(lexemesList))

    return ('Invalid Syntax: "' + str(lexemesList[0][0]) + '" is not a valid keyword.')

# prints the output to the terminal 
def printOutput(lexemesList):
    stringToPrint = ""

    while (lexemesList):
        # print(variablesList)
        # VARIABLE ASSIGNMENT USING "R"
        # if (lexemesList[1][0] == "R"):
        #     assign(lexemesList, lexemesList.pop(0))

        # VARIABLE NAME
        if (lexemesList[0][1] == "Variable Identifier"):
            stringToPrint += (str(findVar(lexemesList.pop(0)[0])) + ' ')
            if (len(lexemesList) > 0):
                if (lexemesList[0][1] == "Variable Identifier"):
                    break

        # STRING
        elif (lexemesList[0][1] == "String Delimiter"): 
            # temp = ""

            if lexemesList.pop(0)[0] == '"':
                # print(lexemesList.pop(0)[0])
                stringToPrint += lexemesList.pop(0)[0] + ' '

                if lexemesList.pop(0)[0] != '"':
                    # error
                    print("Error: invalid string in printing")

            # stringToPrint = (str(stringToPrint) + " ")

        # BOOLEAN OPERATIONS
        elif (lexemesList[0][1] in boolKeywords):
            stringToPrint += (str(booleanOperations(lexemesList)) + ' ')

        # ARITHMETIC OPERATIONS
        elif (lexemesList[0][1] in arithmeticKeywords):
            stringToPrint += (str(arithmeticOp(lexemesList)) + ' ')

        # COMPARISON OPERATIONS
        elif (lexemesList[0][1] in compareKeywords):
            stringToPrint += (str(comparisonOperators(lexemesList)) + ' ')

        # TYPECAST 
        elif (lexemesList[0][1] == "Typecast Keyword"):
            stringToPrint += (str(typecast(lexemesList)) + ' ')

        else: 
            break

    # add to output list and assign as "IT"
    printToTerminal.append(stringToPrint)
    # addVariable("IT", stringToPrint)

# function to perform arithmetic operations
def arithmeticOperations(operations, op1, op2):
    # determine data type of operands 

    # FOR FLOATS 
    if (("." in str(op1)) or ("." in str(op2))):
        op1 = float(op1)
        op2 = float(op2)
    
    # FOR INTS 
    else: 
        op1 = int(op1)
        op2 = int(op2)

    # determine operators
    if (operations[1] == "Addition Operator"):
        print("op1 + op2 = " + str(op1+op2))
        return op1+op2

    elif (operations[1] == "Subtraction Operator"):
        print("op1 - op2 = " + str(op1-op2))
        return op1-op2

    elif (operations[1] == "Multiplication Operator"):
        print("op1 * op2 = " + str(op1*op2))
        return op1*op2

    elif (operations[1] == "Quotient Operator"):
        print("op1 // op2 = " + str(op1//op2))
        return op1//op2

    elif (operations[1] == "Modulo Operator"):
        print("op1 % op2 = " + str(op1%op2))
        return op1%op2

    elif (operations[1] == "Max Operator"):
        print("max(op1, op2) = " + str(max(op1, op2)))
        return max(op1, op2)

    elif (operations[1] == "Min Operator"):
        print("min(op1, op2) = " + str(min(op1, op2)))
        return min(op1, op2)

    else: 
        return ('Invalid Syntax: "' + str(operations[1]) + '" is not a valid keyword.')

# find operands for arithmetic operation 
def arithmeticOp(lexemesList):
    operations = []
    result = None

    # print(lexemesList)
    # get operations (including nested ones )
    while (lexemesList[0][1] in arithmeticKeywords): 
        operations.append(lexemesList.pop(0))
    
    # GET FIRST OPERAND
    # if operand is an integer/numbr, float/numbar, or boolean/troof literal
    if (lexemesList[0][1] in ["NUMBR Type Literal", "NUMBAR Type Literal", "TROOF Type Literal"]):
        firstOp = lexemesList.pop(0)[0]

    # if operand is a string/yarn literal
    elif (lexemesList[0][1] == "String Delimiter"):
        lexemesList.pop(0)                  # pop starting double quote 
        firstOp = lexemesList.pop(0)[0]     # pop string literal 
        lexemesList.pop(0)                  # pop ending double quote 

    # if operand is a variable 
    elif (lexemesList[0][1] == "Variable Identifier"):
        temp = lexemesList.pop(0)

        # find variable name 
        firstOp = findVar(temp[0])

    # if operand is first typecasted
    elif(lexemesList[0][1] == "Typecast Keyword"):
        firstOp = typecast(lexemesList)

    else: 
        return ('Invalid Syntax: "' + str(lexemesList[0][0]) + '" is not a valid keyword.')

    # PERFORM OPERATIONS (including nested ones)
    while operations: 
        result = arithmeticOperations(operations.pop(0), firstOp, getSecondOp(lexemesList))

    return result 

# get second, third, ... operand for any operation 
def getSecondOp(lexemesList):

    # delimiter for operands ("AN")
    if lexemesList[0][1] != "Operator Delimiter":        
        return 
        
    else: 
        lexemesList.pop(0)   # pop "AN" (operator delimiter)

        # if value is an integer/numbr, float/numbar, or boolean/troof literal
        if (lexemesList[0][1] in ["NUMBR Type Literal", "NUMBAR Type Literal", "TROOF Type Literal"]):
            return(lexemesList.pop(0)[0])

        # if value is a string/yarn literal
        elif (lexemesList[0][1] == "String Delimiter"):
            lexemesList.pop(0)              # pop starting double quote 
            value = lexemesList.pop(0)[0]   # pop string literal 
            lexemesList.pop(0)              # pop ending double quote 
            return(value)

        # if operand is a variable 
        elif (lexemesList[0][1] == "Variable Identifier"):
            temp = lexemesList.pop(0)

            # find variable name 
            for variable in variablesList:
                if (variable[0] == temp[0]):
                    return (variable[1])

        # NESTED EXPRESSIONS 
        # if operand is an arithmetic operation ("SUM OF", "DIFF OF", "PRODUKT OF", "QUOSHUNT OF", "MOD OF", "BIGGR OF", "SMALLR OF")
        elif (lexemesList[0][1] in arithmeticKeywords):
            return (arithmeticOp(lexemesList))

        # if operand is a boolean operation ("BOTH OF", "EITHER OF", "WON OF", "NOT", "ANY OF", "ALL OF")
        elif (lexemesList[0][1] in boolKeywords):
            return (booleanOperations(lexemesList))

        # if operand is a relational operation ("BOTH SAEM", "DIFFRINT")
        elif (lexemesList[0][1] in compareKeywords):
            return (comparisonOperators(lexemesList))

        elif(lexemesList[0][1] == "Typecast Keyword"):
            return (typecast(lexemesList))

    return ('Invalid Syntax: "' + str(lexemesList[0][0]) + '" is not a valid keyword.')

# function to perform boolean operations
def booleanOperations(lexemesList):
    operations = []

    # for (nested) operations
    while (lexemesList[0][1] in boolKeywords): 
        operations.append(lexemesList.pop(0))
    
    # GET FIRST OPERAND
    # if operand is a boolean literal 
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

    # if operand is a relational expression
    elif (lexemesList[0][1] in compareKeywords):
        firstOp = comparisonOperators(lexemesList)

    else: 
        return ('Invalid Syntax: "' + str(lexemesList[0][0]) + '" is not a valid keyword.')

    return boolProcess(operations, firstOp, lexemesList)

# function to perform the boolean operation 
def boolProcess (operations, x, lexemesList):
    x = lolToBool(x)                    # convert from "WIN"/"FAIL" (lol) to "True"/"False" (python)

    # NESTED OPERATIONS
    # "ALL OF"
    if operations[0][1] == "Infinite Arity And Operator":         
        while lexemesList[0][1] == "Operator Delimiter":
            y = getSecondOp(lexemesList)
            x = x and lolToBool(y)
        return boolToLol(x)

    # "ANY OF"
    elif operations[0][1] == "Infinite Arity Or Operator":        
        while lexemesList[0][1] == "Operator Delimiter":
            y = getSecondOp(lexemesList)
            x = x or lolToBool(y)
        return boolToLol(x)

    # if it is not a nested operation / reached the root of the nested operation
    else: 
        while operations:                                   # while there are nested operations 
            currOperation = operations.pop(0)               # get current operation to be performed 
            y = getSecondOp(lexemesList)                    # get second operand 

            # and operator ("BOTH OF")
            if currOperation[1] == "And Operator":
                x = x and lolToBool(y)

            # or operator ("EITHER OF")
            elif currOperation[1] == "Or Operator":
                x = x or lolToBool(y)

            # xor operator ("WON OF")
            elif currOperation[1] == "Xor Operator":
                x = x ^ lolToBool(y)

            # not operator ("NOT")   
            elif currOperation[1] == "Boolean Not Operator":
                x = not x

        return boolToLol(x)             # convert from "True"/"False" (python) to "WIN"/"FAIL" (lol)

# function to convert boolean literals from lolcode ("WIN"/"FAIL") to python ("True"/"False")
def lolToBool(x):
    if x == "WIN":
        return True
    elif x == "FAIL": 
        return False

# function to convert boolean literals from python ("True"/"False") to lolcode ("WIN"/"FAIL")
def boolToLol(x):
    if x == True:
        return "WIN"
    elif x == False: 
        return "FAIL"

# function to get operands for relational operations 
def comparisonOperators(lexemesList):
    operations = []

    # for (nested) operations
    while (lexemesList[0][1] in compareKeywords): 
        operations.append(lexemesList.pop(0))
    
    curr = lexemesList.pop(0)               # get current operation 

    # GET FIRST OPERAND
    # if operand is a literal 
    if (curr[1] in ["NUMBR Type Literal", "NUMBAR Type Literal"]):
        firstOp = lexemesList.pop(0)[0]

    # if operand is a variable name, find its value 
    elif (curr[1] == "Variable Identifier"):
        # temp = lexemesList.pop(0)

        # find variable name 
        firstOp = findVar(curr[0])

    # boolean operations 
    elif (curr[1] in boolKeywords):
        firstOp = booleanOperations(lexemesList)

    # arithmetic operations
    elif (curr[1] in arithmeticKeywords):
        firstOp = arithmeticOp(lexemesList)

    # if operand is first typecasted 
    elif (curr[1] == "Typecast Keyword"):
        firstOp = typecast(lexemesList)

    else: 
        return ('Invalid Syntax: "' + str(curr[0]) + '" is not a valid keyword.')

    return compareProcess(operations, firstOp, lexemesList)

# function to perform relational operation
def compareProcess(operations, x, lexemesList):
    # while there arenested operations 
    while operations:

        # equal operator ("BOTH SAEM")
        if operations[0][1] == "Equal Operator":            
            result = (x == getSecondOp(lexemesList))

        # not equal operator ("DIFFRINT")
        elif operations[0][1] == "Not Equal Operator":     
            result = (int(x) != int(getSecondOp(lexemesList)))
        operations.pop(0)

    return boolToLol(result)                # convert result from python ("True"/"False") to lol ("WIN"/"FAIL")   

# function to typecast values 
def typecast(lexemesList):
    value = lexemesList.pop(0)              # get value 
    explicitCast = 0                        # check if it is explicitly typecasted 

    # check if the statement has a form of: "MAEK var1 A NUMBAR"  
    if (value[0] == "MAEK"):
        value = lexemesList.pop(0)
        explicitCast = 1
    
    # CHECK IF IT IS A VARIABLE OR LITERAL
    # if value is a variable name
    if (value[1] == "Variable Identifier"):
        value = findVar(value[0])

    # if value is an integer/numbr, float/numbar, or boolean/troof literal
    elif (value[1] in ["NUMBR Type Literal", "NUMBAR Type Literal", "TROOF Type Literal"]):
        value = lexemesList.pop(0)[0]

    # if value is a string/yarn literal
    elif (value[1] == "String Delimiter"):
        lexemesList.pop(0)              # pop starting double quote 
        value = lexemesList.pop(0)[0]   # pop string literal 
        lexemesList.pop(0)              # pop ending double quote 

    # check keywords for re-casting ("IS NOW A", "A")
    if (lexemesList[0][0] in ["IS NOW A", "A"]):
        lexemesList.pop(0)              # remove keywords 

    # PROCESS TYPECASTING 

    # typecast to int/numbr (allowable from bool/troof, uninit/noob, float/numbar, string/yarn)
    if (lexemesList[0][1] == "NUMBR Type Literal"):
        lexemesList.pop(0)  

        # from boolean 
        if (value == "WIN"):    # "WIN" to 1
            return(1)

        # "FAIL" or NOOB/unitialized to 0
        elif ((value == "FAIL") or ((explicitCast == 1) and (value == "NULL"))):
            return(0)

        # from float/numbar -> truncate decimal values 
        elif ("." in value):
            return(int(value))

        # 
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

    else: 
        return ('Invalid Syntax: "' + str(lexemesList[0][0]) + '" is not a valid keyword.')


def findVar(variableName):
    # print("variable name: " + str(variableName))
    # find variable name 
    print(variablesList)
    print(variableName)
    for variable in variablesList:
        if (variable[0] == variableName):
            value = variable[1]
            break
    # print(str(variableName) + str(value))
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
                return ('Invalid Syntax: "' + str(lexemesList[0][0]) + '" is not a valid keyword.')
        else: 
            return((variableName, "NULL"))

    else:
        return ('Invalid Syntax: "' + str(lexemesList[0][0]) + '" is not a valid keyword.')

def addVariable(variableName, newVal):
    print("NewVal: " + str(newVal))
    temp = 0
    for i in range(len(variablesList)):
        if (variablesList[i][0] == variableName):
            variablesList.pop(i)
            # variablesList[i][1] = newVal[0]
            break
        temp += 1
    variablesList.insert(temp, (variableName, newVal))
    # print(variablesList)

def ifThenState(lexemesList, inputValues):
    isMatch = False
    lexemesList.pop(0)

    while lexemesList: 
        print(lexemesList)
        if lexemesList[0][1] == "If Keyword":               # YA RLY
            lexemesList.pop(0)
            if (findVar("IT") == "WIN"):
                foundCond(lexemesList, inputValues)
                isMatch = True 
            
            else: 
                while lexemesList:
                    lexemesList.pop(0)
                    if(lexemesList[0][1] in ["Else Keyword", "End of If-then"]):
                        break
        
        if ((lexemesList[0][1] == "Else Keyword") and isMatch == False): 
            lexemesList.pop(0)
            foundCond(lexemesList, inputValues)
            isMatch = True 
        
        if isMatch == True:
            while lexemesList[0][1] != "End of If-then":
                lexemesList.pop(0)
            lexemesList.pop(0)
            break                   # exit while loop
        lexemesList.pop(0)

# found the condition that matches the IT variable 
def foundCond(lexemesList, inputValues):
    ifThenStatements = []

    while lexemesList:
        ifThenStatements.append(lexemesList.pop(0))

        if lexemesList[0][1] in ["Else Keyword", "End of If-then"]:
            break
    
    getStatements(ifThenStatements, inputValues)


def switchCase(lexemesList, inputValues):
    caseCond = ""
    isMatch = False 

    # print(lexemesList)
    print("In switchCase with token " + str(lexemesList[0][0]))

    while lexemesList[0][1] != "End of If-then":            # OIC keyword
        if (lexemesList[0][1] == "Case Delimiter"):         # OMG keyword 
            lexemesList.pop(0)                  
        
            # CHECK CONDITION OF EACH CASE (literal or variable)
            if (lexemesList[0][1] in literalKeywords):
                caseCond = lexemesList.pop(0)[0]
                # addVariable("IT", caseCond)
                
            elif (lexemesList[0][1] == "Variable Identifier"):
                temp = lexemesList.pop(0)
                caseCond = findVar(temp[0])
                # addVariable("IT", caseCond)

            print("Casecond: " + str(caseCond))

            # check if IT variable matches case conditon 
            if (str(caseCond) == str(findVar("IT"))):  
                print("i am here!!!")               
                foundCase(lexemesList, inputValues)
                isMatch = True 
            
        elif (lexemesList[0][1] == "Default Case Keyword"):     # OMGWTF
            isMatch = True 
            lexemesList.pop(0)
            foundCase(lexemesList, inputValues)
            

        if isMatch == True:
            while lexemesList[0][1] != "End of If-then":        # OIC
                lexemesList.pop(0)
            lexemesList.pop(0)          # pop "OIC" keyword
            break                       # break while loop
        lexemesList.pop(0)

# found the case that matched with the IT variable 
def foundCase(lexemesList, inputValues):
    caseStatements = []

    print("i am in foundCase!!!")
    while lexemesList:
        caseStatements.append(lexemesList.pop(0))
        if lexemesList[0][1] in ["Case Delimiter", "Default Case Keyword", "End of If-then"]:
            break
    print(caseStatements)
    getStatements(caseStatements, inputValues)

# parse lexemes 
def parse(lexTable, userInput):
    startFlag = False       # flag if the start of the program has been detected 
    cleanLex = []
    printToTerminal.clear()
    variablesList.clear()

    # CHECK FOR COMMENTS (not considered as statements)
    cleanLex = removeComments(lexTable)         # remove comments since it will only be ignored 

    # CHECK FOR "HAI"
    if (cleanLex[0][1] == "Start of Program"):         # if the first element in the list is the "HAI" keyword (start of program)
        cleanLex.remove(cleanLex[0])                                # remove "HAI" from list 
        if (cleanLex[0][1] in ["NUMBR Type Literal", "NUMBAR Type Literal"]):                           # check if "HAI" keyword contains a version number 
            cleanLex.remove(cleanLex[0])                            # remove "HAI" version from list 
    else: 
        return('Invalid Syntax: no "HAI" keyword')

    # CHECK FOR "KTHXBYE"
    if (cleanLex[len(cleanLex) - 1][1] == "End of Program"):        # if the last element in the list is the "KTHXBYE" keyword (end of program) 
        cleanLex.remove(cleanLex[len(cleanLex) - 1])                # remove "KTHXBYE" from list 
    else: 
        return('Invalid Syntax: no "KTHXBYE" keyword')

    return getStatements(cleanLex, userInput), printToTerminal

def getStatements(cleanLex, inputValues):
    # iterate over statements in the code 
    while cleanLex: 
        lexeme = cleanLex.pop(0)
        token = lexeme[0]
        tokenDesc = lexeme[1]

        # print(str(cleanLex) + "\n")

        print("token: " + str(token))

        # VARIABLE DECLARATION ("I HAS A")
        if (tokenDesc == "Variable Declaration"):           # I HAS A
            variablesList.append(variableAssignment(cleanLex))

        # INPUT STATEMENT ("GIMMEH")
        elif (tokenDesc == "Input Keyword"):
            addVariable(cleanLex.pop(0)[0], inputValues.pop(0))

        # PRINT STATEMENT ("VISIBLE")
        elif (tokenDesc == "Output Keyword"):
            printOutput(cleanLex)

        # TYPECAST ("MAEK")
        elif (token == "MAEK"):                             # MAEK
            addVariable("IT", typecast(cleanLex))

        # IF-THEN STATEMENTS  ("O RLY?")
        elif (tokenDesc == "Start of If-then Delimiter"):    # O RLY?
            ifThenState(cleanLex, inputValues)

        # SWITCH CASES ("WTF?")
        elif (tokenDesc == "Start of Switch-case"):         # WTF?
            switchCase(cleanLex, inputValues)

        # GTFO
        elif (token == "Break Keyword"):                              # GTFO
            break
    
        else: 
            if (cleanLex):
                # "R"
                if (cleanLex[0][1] == "Assignment Operation"):          # R
                    assign(cleanLex, token)

                # SUM OF, DIFF OF, PRODUKT OF, QUOSHUNT OF, MOD OF, BIGGR OF, SMALLR OF
                elif (tokenDesc in arithmeticKeywords):              
                    addVariable("IT", arithmeticOp(cleanLex))

                # BOTH OF, EITHER OF, WON OF, NOT, ALL OF, ANY OF 
                elif (tokenDesc in boolKeywords):
                    cleanLex.insert(0, (token, tokenDesc))
                    addVariable("IT", booleanOperations(cleanLex))

                # BOTH SAEM, DIFFRINT
                elif (tokenDesc in compareKeywords): 
                    cleanLex.insert(0, (token, tokenDesc))
                    addVariable("IT", comparisonOperators(cleanLex))

                # "IS NOW A"
                elif (cleanLex[0][0] == "IS NOW A"):
                    addVariable("IT", typecast(cleanLex))

                else: 
                    return ('Invalid Syntax: "' + str(cleanLex[0][0]) + '" is not a valid keyword.')

    # print(variablesList)

    return variablesList