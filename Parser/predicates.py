
from nltk.tree import *
from Scanner.classes import token_type, token


def Predicates(j, Tokens):
    # Predicates → Predicate  | ε
    output = dict()
    children=[]
    predicates = Match(token_type.Predicate, j, Tokens)
    children.append(predicates["node"])
    statements = Statements(predicates["index"], Tokens)
    children.append(statements["node"])
    Node=Tree('Predicates',children)
    output["node"]=Node
    output["index"]=statements["index"]
    return output

def Statements(j, Tokens):
    # Statements → Statement State
    output = dict()
    children=[]
    statement = Statement(j, Tokens)
    children.append(statement["node"])
    state = State(statement["index"], Tokens)
    children.append(state["node"])
    Node=Tree('Statements',children)
    output["node"]=Node
    output["index"]=state["index"]
    return output

def State(j, Tokens):
    # State  → Statement State | ε
    output = dict()
    children=[]
    if(j < len(Tokens)):
        if(Tokens[j].to_dict()['token_type'] ==token_type.Name):
            statement = Statement(j, Tokens)
            children.append(statement["node"])
            state = State(statement["index"], Tokens)
            children.append(state["node"])
            Node=Tree('State',children)
            output["node"]=Node
            output["index"]=state["index"]
            return output
        else:
            Node=Tree('State',children)
            output["node"]=Node
            output["index"]=j
            return output
    else:
        Node=Tree('State',children)
        output["node"]=Node
        output["index"]=j
        return output
    

def Statement(j, Tokens):
    # Statement → name ( Parameters ) | name 
    output = dict()
    children=[]
    name = Match(token_type.Name, j, Tokens)
    children.append(name["node"])
    if(name["index"] < len(Tokens)):
        if(Tokens[name["index"]].to_dict()['token_type'] ==token_type.open_paren):
            open_paren = Match(token_type.open_paren, name["index"], Tokens)
            children.append(open_paren["node"])
            parameters = Parameters(open_paren["index"], Tokens)
            children.append(parameters["node"])
            close_paren = Match(token_type.close_paren, parameters["index"], Tokens)
            children.append(close_paren["node"])
            Node=Tree('Statement',children)
            output["node"]=Node
            output["index"]=close_paren["index"]
            return output
        else:
            Node=Tree('Statement',children)
            output["node"]=Node
            output["index"]=name["index"]
            return output
    else:
        Node=Tree('Statement',children)
        output["node"]=Node
        output["index"]=name["index"]
        return output

def Parameters(j, Tokens):
    # Parameters → datatype Parametertail
    output = dict()
    children=[]
    datatype = Match(token_type.data_type, j, Tokens)
    children.append(datatype["node"])
    parametertail = Parametertail(datatype["index"], Tokens)
    children.append(parametertail["node"])
    Node=Tree('Parameters',children)
    output["node"]=Node
    output["index"]=parametertail["index"]
    return output

def Parametertail(j, Tokens):
    # Parametertail → , datatype Parametertail | ε
    output = dict()
    children=[]
    if(j < len(Tokens)):
        if(Tokens[j].to_dict()['token_type']==token_type.comma):
            comma = Match(token_type.comma, j, Tokens)
            children.append(comma["node"])
            datatype = Match(token_type.data_type, comma["index"], Tokens)
            children.append(datatype["node"])
            parametertail = Parametertail(datatype["index"], Tokens)
            children.append(parametertail["node"])
            Node=Tree('Parametertail',children)
            output["node"]=Node
            output["index"]=parametertail["index"]
            return output
        else:
            Node=Tree('Parametertail',children)
            output["node"]=Node
            output["index"]=j
            return output  
    else:
        Node=Tree('Parametertail',children)
        output["node"]=Node
        output["index"]=j
        return output
    

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
            #errors.append("Syntax error : "+Temp['Lex']+" Expected dot")
            return output
    else:
        output["node"]=["error"]
        output["index"]=j+1
        return output