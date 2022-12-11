import re

arithmeticKeywords = ["Addition Operator", "Subtraction Operator", "Multiplication Operator", "Quotient Operator", "Modulo Operator", "Max Operator", "Min Operator"]
boolKeywords = ["And Operator", "Or Operator", "Xor Operator", "Boolean Not Operator", "Infinite Arity And Operator", "Infinite Arity Or Operator"]
compareKeywords = ["Equal Operator", "Not Equal Operator"]

literalKeywords = ["NUMBR Type Literal", "NUMBAR Type Literal", "YARN Type Literal", "TROOF Type Literal"]

keywords = {
    'NUMBR' : "NUMBR Type Literal",
    'NUMBAR' : "NUMBAR Type Literal",
    'YARN' : "YARN Type Literal",
    'TROOF' : "TROOF Type Literal",
    "HAI" : "Start of Program",
    "KTHXBYE" : "End of Program",
    "BTW" : "Single-Line Comment Delimiter",
    "OBTW" : "Multi-Line Comment Delimiter",
    "TLDR" : "Multi-Line Comment Delimiter",
    "ITZ" : "Variable Assignment",
    "R" : "Assignment Operation",
    "SUM OF" : "Addition Operator",
    "DIFF OF" : "Subtraction Operator",
    "PRODUKT OF" : "Multiplication Operator",
    "QUOSHUNT OF" : "Quotient Operator",
    "MOD OF" : "Modulo Operator",
    "BIGGR OF" : "Max Operator",
    "SMALLR OF" : "Min Operator",
    "BOTH OF" : "And Operator",
    "EITHER OF" : "Or Operator",
    "WON OF" : "Xor Operator",
    "NOT" : "Boolean Not Operator",
    "ANY OF" : "Infinite Arity Or Operator",
    "ALL OF" : "Infinite Arity And Operator",
    "BOTH SAEM" : "Equal Operator",
    "DIFFRINT" : "Not Equal Operator",
    "SMOOSH" : "Concatenation Keyword",
    "MAEK" : "Typecast Keyword",
    'A' : "Typecast Keyword",
    "IS NOW A" : "Typecast Keyword",
    "VISIBLE" : "Output Keyword",
    "GIMMEH" : "Input Keyword",
    "O RLY?" : "Start of If-then Delimiter",
    "YA RLY" : "If Keyword",
    "MEBBE" : "Else-if Keyword",
    "NO WAI" : "Else Keyword",
    "OIC" : "End of If-then",
    "WTF?" : "Start of Switch-case",
    "OMG" : "Case Delimiter",
    "OMGWTF" : "Default Case Keyword",
    "IM IN YR" : "Loop Delimiter",
    "UPPIN" : "Increment Keyword",
    "NERFIN" : "Decrement Keyword",
    "YR" : "Loop Operator-Variable Delimiter",
    "TIL" : "Loop Until Keyword",
    "WILE" : "Loop While Keyword",
    "IM OUTTA YR" : "Loop Delimiter",
    'NOOB' : "Type Literal",
    "AN" : "Operator Delimiter",
    "I HAS A" : "Variable Declaration",
    "GTFO": "Break Keyword",
    "MKAY": "Operation End"
}

def tokenize(string):
    lexTable = []
    lineNum = 1
    comment = False                         # comment flag 
    
    for line in string.split("\n"):                 # iterate per line 
        token = ""                                  # stores words in line 
        if line == "" or line.isspace():            # if end of line is reached
            lineNum += 1
            continue
        for word in line.split():                   # iterate over each word per line 
            if word == "TLDR":                      # check if it is the end of a multi-line comment               
                comment = False             
            if (comment):                                   # if line is a mult-line comment 
                lexTable.append((line, "Comment Literal"))           # add comment as comment string to lexeme table 
                lineNum += 1
                break
            elif word == "BTW":                             # single-line comment
                lexTable.append((word, keywords[word]))   # add comment as comment string to lexeme table 
                singleLineComment = 0
                for temp in line.split():
                    if (temp == "BTW"):
                        singleLineComment = 1
                    elif (singleLineComment == 1):
                        token += temp
                        token += " "
                lexTable.append((token, "Comment Literal"))
                break                                       # ignore whole line 
            elif (word.isspace() or word == '') and token == "":   # if line is an empty string, move to the next line (ignore)
                continue

            # at the start of the line 
            if token == "":                         
                if word in keywords.keys():         # check if first word in the line is a keyword 
                    lexTable.append((word, keywords[word]))     # if it is a keyword, add to lexeme table 

                # else, check if current word is at the first part of a keyword that is composed of 2 or more words (e.g. I HAS A, SUM OF, etc.)
                elif word in ['I', "SUM", "DIFF", "PRODUKT", "QUOSHUNT", "MOD",         
                            "BIGGR", "SMALLR", "BOTH", "EITHER", "WON", "ANY", "ALL",
                            "BOTH", "IS", "O", "YA", "NO", "IM"]:
                    token += word                   # if it is a part of a multi-word keyword, store current word in token 
                
                # else, current word is not a part of any keyword  
                else:                               
                    # check if word is a boolean value
                    if word == "WIN" or word == "FAIL":                               
                        lexTable.append((word, keywords["TROOF"]))
                    
                    elif bool(re.match("^\-?[0-9]+$", word)):
                        lexTable.append((word, keywords["NUMBR"]))

                    # check if word is a float or integer
                    elif bool(re.match("^\-?[0-9]+\.[0-9]+$", word)):             
                        lexTable.append((word, keywords["NUMBAR"]))  
                    
                    # else, check if word has the form "literal" (for strings)
                    elif bool(re.match("\".*\"", word)):                             
                        lexTable.append((word[0], "String Delimiter"))              # extract double quote at the start of the string
                        lexTable.append((word[1:(len(word)-1)], keywords["YARN"]))         # extract string literal (words inside double quotes)
                        lexTable.append((word[len(word)-1], "String Delimiter"))    # extact double quote at the end of the string 
                    
                    # else, check if word is a double quote
                    elif bool(re.match("\"\.*", word)):                             
                        token += word                                               # store double quote to token 
                        token += ' '                                                # add space after the double quote in token 

                    # else, check if word is a variable 
                    elif bool(re.match("^[A-Za-z]+[A-Za-z0-9_]*$", word)):           
                        lexTable.append((word, "Variable Identifier"))

                    # else, check if word is a space or is empty (end of line)
                    elif word.isspace() == False and word != '':
                        return ("Line " + str(lineNum) + ": unidentified token " + word)    # invalid token 
            
            # not at the start of the line and the word is a double quote 
            elif token[0] == '\"':                  
                token += word                                               
                if token[len(token)-1] == '\"':
                    lexTable.append((token[0], "String Delimiter"))
                    lexTable.append((token[1:len(token)-1], "Literal"))
                    lexTable.append(
                        (token[len(token)-1], "String Delimiter"))
                    token = ''
                else:
                    token += ' '
            
            # else, if it is not at the start of the line and word is not a double quote
            else:
                # else, check if current word is a part of a keyword that is composed of 2 or more words (e.g. I HAS A, SUM OF, etc.)
                if word in ["HAS", "OF", "SAEM", "NOW", "RLY?", "RLY",
                            "WAI", "IN", "OUTTA", 'A', "YR"]:
                    token += " "                                        # add space between first part of the keyword stored in token 
                    token += word                                       # if it is a part of a multi-word keyword, store current word in token 
                    if token in keywords.keys():                        # check if multi-worded token is a keyword 
                        lexTable.append((token, keywords[token]))       # if it is a keyword, add to lexical table 
                        token = ""                                      # reset value of token 

                # else, check if word is an identifier 
                elif bool(re.match("^[A-Za-z]+[A-Za-z0-9_]*$", word)):
                    lexTable.append((token, "identifier"))
                    lexTable.append((word, "identifier"))
                    token = ''
                else:
                    return ("Line "+str(lineNum)+": unidentified token "+token)     # invalid token

            # check if word is a comment identifier 
            if word == "OBTW":                              # multi-line comment
                comment = True                      # set comment flag to true 
        lineNum += 1                                        # increment line number 
    # print(lexTable)

    # CHECKING PURPOSES ONLY
    # put lexical table in a text file 
    f = open("lexical_table.txt", "w")
    f.write("LEXEME\t\t\tCLASSIFICATION\n")
    for k in lexTable:
        f.write("{: <10}\t\t{: <10}\n".format(k[0], k[1]))
    f.close()

    return lexTable