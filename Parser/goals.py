from nltk.tree import *
from Scanner.classes import token_type
from Parser.utils import *


def Goal(j, Tokens):
    # Goal → goal statement .
    output = dict()
    children=[]
    goal = Match(token_type.Goal, j, Tokens)
    children.append(goal["node"])
    statement = Statement(goal["index"], Tokens)
    children.append(statement["node"])
    dot = Match(token_type.dot, statement["index"], Tokens)
    children.append(dot["node"])
    Node=Tree('Goal',children)
    output["node"]=Node
    output["index"]=dot["index"]
    return output

def Statement(j, Tokens):
    # Statement → name ( Arguments ) | name
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
        arguments = Arguments(open_paren["index"], Tokens)
        children.append(arguments["node"])
        close_paren = Match(token_type.close_paren, arguments["index"], Tokens)
        children.append(close_paren["node"])
        Node=Tree('Statement',children)
        output["node"]=Node
        output["index"]=close_paren["index"]
        return output
        
    
def Arguments(j, Tokens):
    # Arguments → name Argument | variable Argument | _ Argument
    output = dict()
    children=[]
    if(Tokens[j].to_dict()['token_type'] ==token_type.Name):
        name = Match(token_type.Name, j, Tokens)
        children.append(name["node"])
        term = Term(name["index"], Tokens)
        children.append(term["node"])
        Node=Tree('Arguments',children)
        output["node"]=Node
        output["index"]=term["index"]
    elif(Tokens[j].to_dict()['token_type'] ==token_type.variable_name):
        variable_name = Match(token_type.variable_name, j, Tokens)
        children.append(variable_name["node"])
        term = Term(variable_name["index"], Tokens)
        children.append(term["node"])
        Node=Tree('Arguments',children)
        output["node"]=Node
        output["index"]=term["index"]
    elif(Tokens[j].to_dict()['token_type'] ==token_type.Anonymous):
        anonymous = Match(token_type.Anonymous, j, Tokens)
        children.append(anonymous["node"])
        term = Term(anonymous["index"], Tokens)
        children.append(term["node"])
        Node=Tree('Arguments',children)
        output["node"]=Node
        output["index"]=term["index"]
    else:
        return error(j, "Syntax error : "+Tokens[j].to_dict()['Lex']+", Expected Name or variable_name or Anonymous")
    return output
    

def Term(j, Tokens):
    # Argument → , name Argument | , variable Argument | , _ Argument | ε
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
            Node=Tree('Argument',children)
            output["node"]=Node
            output["index"]=term["index"]
            return output
        elif(Tokens[comma["index"]].to_dict()['token_type'] ==token_type.variable_name):
            variable_name = Match(token_type.variable_name, comma["index"], Tokens)
            children.append(variable_name["node"])
            term = Term(variable_name["index"], Tokens)
            children.append(term["node"])
            Node=Tree('Argument',children)
            output["node"]=Node
            output["index"]=term["index"]
            return output
        elif(Tokens[comma["index"]].to_dict()['token_type'] ==token_type.Anonymous):
            anonymous = Match(token_type.Anonymous, comma["index"], Tokens)
            children.append(anonymous["node"])
            term = Term(anonymous["index"], Tokens)
            children.append(term["node"])
            Node=Tree('Argument',children)
            output["node"]=Node
            output["index"]=term["index"]
            return output
        else:
            return error(comma["index"], "Syntax error : "+Tokens[j].to_dict()['Lex']+", Expected Name or variable_name or Anonymous")

    
def error(j, error_message):
    error = dict()
    error["node"]=["error"]
    error["index"]= j
    errors.append(error_message)
    return error