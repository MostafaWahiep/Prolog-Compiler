from Scanner.classes import token_type
from nltk.tree import *

errors = []

def Match(a,j, Tokens):
    output=dict()
    if(j<len(Tokens)):
        Temp=Tokens[j].to_dict()
        if(Temp['token_type']==a):
            j+=1
            output["node"]=[Temp['Lex']]
            output["index"]=j
            return output
        else:
            output["node"]=["error"]
            output["index"]=j+1
            errors.append("Syntax error : "+Temp['Lex']+" Expected dot")
            return output
    else:
        output["node"]=["error"]
        output["index"]=j+1
        return output
    
def Statement(j, Tokens):
    # Statement → name ( Terms ) | name
    output = dict()
    children=[]
    name = Match(token_type.Name, j, Tokens)
    children.append(name["node"])
    if(name["index"] >= len(Tokens)):
        return error(name["index"], "Syntax error : "+Tokens[j].to_dict()['Lex']+", Expected (")
        
    elif(Tokens[name["index"]].to_dict()['token_type'] != token_type.open_paren):
        Node=Tree('Statement',children)
        output["node"]=Node
        output["index"]=name["index"]
        return output
    else:
        open_paren = Match(token_type.open_paren, name["index"], Tokens)
        children.append(open_paren["node"])
        terms = Terms(open_paren["index"], Tokens)
        children.append(terms["node"])
        close_paren = Match(token_type.close_paren, terms["index"], Tokens)
        children.append(close_paren["node"])
        Node=Tree('Statement',children)
        output["node"]=Node
        output["index"]=close_paren["index"]
        return output
        
    
def Terms(j, Tokens):
    # Terms → name Term | variable Term | _ term
    output = dict()
    children=[]
    if(Tokens[j].to_dict()['token_type'] ==token_type.Name):
        name = Match(token_type.Name, j, Tokens)
        children.append(name["node"])
        term = Term(name["index"], Tokens)
        children.append(term["node"])
        Node=Tree('Terms',children)
        output["node"]=Node
        output["index"]=term["index"]
    elif(Tokens[j].to_dict()['token_type'] ==token_type.variable_name):
        variable_name = Match(token_type.variable_name, j, Tokens)
        children.append(variable_name["node"])
        term = Term(variable_name["index"], Tokens)
        children.append(term["node"])
        Node=Tree('Terms',children)
        output["node"]=Node
        output["index"]=term["index"]
    elif(Tokens[j].to_dict()['token_type'] ==token_type.Anonymous):
        anonymous = Match(token_type.Anonymous, j, Tokens)
        children.append(anonymous["node"])
        term = Term(anonymous["index"], Tokens)
        children.append(term["node"])
        Node=Tree('Terms',children)
        output["node"]=Node
        output["index"]=term["index"]
    else:
        return error(j, "Syntax error : "+Tokens[j].to_dict()['Lex']+", Expected Name or variable_name or Anonymous")
    return output
    

def Term(j, Tokens):
    # Term → , name Term | , variable Term | , _ term | ε
    output = dict()
    children=[]
    if(j >= len(Tokens)):
        return error(j, "Syntax error : "+Tokens[j].to_dict()['Lex']+", Expected Name or variable_name or Anonymous")
    elif(Tokens[j].to_dict()['token_type'] != token_type.comma):
        Node=Tree('Term',children)
        output["node"]=Node
        output["index"]=j
        return output
    else:
        comma = Match(token_type.comma, j, Tokens)
        children.append(comma["node"])
        if(Tokens[comma["index"]].to_dict()['token_type'] ==token_type.Name):
            name = Match(token_type.Name, comma["index"], Tokens)
            children.append(name["node"])
            term = Term(name["index"], Tokens)
            children.append(term["node"])
            Node=Tree('Term',children)
            output["node"]=Node
            output["index"]=term["index"]
            return output
        elif(Tokens[comma["index"]].to_dict()['token_type'] ==token_type.variable_name):
            variable_name = Match(token_type.variable_name, comma["index"], Tokens)
            children.append(variable_name["node"])
            term = Term(variable_name["index"], Tokens)
            children.append(term["node"])
            Node=Tree('Term',children)
            output["node"]=Node
            output["index"]=term["index"]
            return output
        elif(Tokens[comma["index"]].to_dict()['token_type'] ==token_type.Anonymous):
            anonymous = Match(token_type.Anonymous, comma["index"], Tokens)
            children.append(anonymous["node"])
            term = Term(anonymous["index"], Tokens)
            children.append(term["node"])
            Node=Tree('Term',children)
            output["node"]=Node
            output["index"]=term["index"]
            return output
        else:
            return error(comma["index"], "Syntax error : "+Tokens[j].to_dict()['Lex']+", Expected Name or variable_name or Anonymous")

    
def error(j, error_message):
    error = dict()
    error["node"]=["error"]
    error["index"]= j+1
    errors.append(error_message)
    return error