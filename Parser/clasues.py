from nltk.tree import *
from Scanner.classes import token_type
from Parser.utils import *
from Parser.body import Body

def Clauses(j, Tokens):
    # Clauses → Fact State2 | Rule State2
    output = dict()
    children=[]
    clauses = Match(token_type.Clause, j, Tokens)
    children.append(clauses["node"])
    if(Is_Rule(clauses['index'],Tokens)):
        out_dict = Rule(clauses['index'], Tokens)
    else:
        out_dict = Facts(clauses['index'], Tokens)
    children.append(out_dict['node'])
    out_dict = State2(out_dict['index'], Tokens)
    children.append(out_dict['node'])
    Node=Tree('Clauses',children)
    output["node"]=Node
    output["index"]=out_dict["index"]
    return output

def State2(j, Tokens):
    # State2 → Fact State2 | Rule State2 | ε
    output = dict()
    children=[]
    if(j < len(Tokens)):
        if(Tokens[j].to_dict()['token_type'] ==token_type.Name):
            if(Is_Rule(j ,Tokens)):
                out_dict = Rule(j, Tokens)
            else:
                out_dict = Facts(j, Tokens)
            children.append(out_dict['node'])
            out_dict = State2(out_dict['index'], Tokens)
            children.append(out_dict['node'])
            Node=Tree('State',children)
            output["node"]=Node
            output["index"]=out_dict["index"]
            return output
        else:
            Node=Tree('State',children)
            output["node"]=Node
            output["index"]=j
            return output
    else:
        Node=Tree('State',children)
        output["node"]= 'error'
        output["index"]=j
        return output

def Facts(j, Tokens):
    # Facts → name (values) . | name .
    output = dict()
    children=[]
    name = Match(token_type.Name, j, Tokens)
    children.append(name["node"])
    if(name["index"] >= len(Tokens)):
        return error(name["index"], "Syntax error : "+Tokens[j].to_dict()['Lex']+", Expected ( or .")
    elif(Tokens[name["index"]].to_dict()['token_type'] != token_type.open_paren):
        dot = Match(token_type.dot, name["index"], Tokens)
        children.append(dot["node"])
        Node=Tree('Facts',children)
        output["node"]=Node
        output["index"]=dot["index"]
        return output
    else:
        open_paren = Match(token_type.open_paren, name["index"], Tokens)
        children.append(open_paren["node"])
        values = Values(open_paren["index"], Tokens)
        children.append(values["node"])
        close_paren = Match(token_type.close_paren, values["index"], Tokens)
        children.append(close_paren["node"])
        dot = Match(token_type.dot, close_paren["index"], Tokens)
        children.append(dot["node"])
        Node=Tree('Facts',children)
        output["node"]=Node
        output["index"]=dot["index"]
        return output

def Values(j, Tokens):
    # Values → value vals
    output = dict()
    children=[]
    value = Match_value(j, Tokens)
    children.append(value["node"])
    vals = Vals(value["index"], Tokens)
    children.append(vals["node"])
    Node=Tree('Values',children)
    output["node"]=Node
    output["index"]=vals["index"]
    return output

def Vals(j, Tokens):
    # Vals → , value vals | ε
    output = dict()
    children=[]
    if(j < len(Tokens)):
        if(Tokens[j].to_dict()['token_type']==token_type.comma):
            comma = Match(token_type.comma, j, Tokens)
            children.append(comma["node"])
            value = Match_value(comma["index"], Tokens)
            children.append(value["node"])
            vals = Vals(value["index"], Tokens)
            children.append(vals["node"])
            Node=Tree('Vals',children)
            output["node"]=Node
            output["index"]=vals['index']
            return output
        else:
            Node=Tree('Vals',children)
            output["node"]=Node
            output["index"]=j
            return output 
    else:
        Node=Tree('Error',children)
        output["node"]=Node
        output["index"]=j
        return output

def Match_value(j, Tokens):
    # value -> Integer | Real | Char | String | Name
    output = dict()
    children=[]
    if(Tokens[j].to_dict()['token_type'] ==token_type.Integer):
        value = Match(token_type.Integer, j, Tokens)
    elif(Tokens[j].to_dict()['token_type'] ==token_type.Real):
        value = Match(token_type.Real, j, Tokens)
    elif(Tokens[j].to_dict()['token_type'] ==token_type.Char):
        value = Match(token_type.Char, j, Tokens)
    elif(Tokens[j].to_dict()['token_type'] ==token_type.String):
        value = Match(token_type.String, j, Tokens)
    elif(Tokens[j].to_dict()['token_type'] ==token_type.Name):
        value = Match(token_type.Name, j, Tokens)
    else:
        return error(j, "Syntax error : "+Tokens[j].to_dict()['Lex']+", Expected value")
    children.append(value["node"])
    Node=Tree('value',children)
    output["node"]=Node
    output["index"]=value["index"]
    return output


def Head(j, Tokens):
    # Head → name (terms) | name
    output = dict()
    children=[]
    name = Match(token_type.Name, j, Tokens)
    children.append(name["node"])
    if(name["index"] < len(Tokens)):
        if(Tokens[name["index"]].to_dict()['token_type'] ==token_type.open_paren):
            open_paren = Match(token_type.open_paren, name["index"], Tokens)
            children.append(open_paren["node"])
            terms = Terms(open_paren["index"], Tokens)
            children.append(terms["node"])
            close_paren = Match(token_type.close_paren, terms["index"], Tokens)
            children.append(close_paren["node"])
            Node=Tree('Head',children)
            output["node"]=Node
            output["index"]=close_paren["index"]
            return output
        else:
            Node=Tree('Head',children)
            output["node"]=Node
            output["index"]=name["index"]
            return output
    else:
        Node=Tree('Head',children)
        output["node"]= 'error'
        output["index"]=name["index"]
        return output
    
def Terms(j, Tokens):
    # Terms → value term | variable term | - term
    output = dict()
    children=[]
    if(Tokens[j].to_dict()['token_type'] in [token_type.Integer, token_type.Real, token_type.Char, token_type.String]):
        value = Match_value(j, Tokens)
        children.append(value["node"])
        out_dict = Term(value['index'], Tokens)
        children.append(out_dict["node"])
        Node=Tree('Terms',children)
        output["node"]=Node
        output["index"]=out_dict["index"]
        return output
    elif(Tokens[j].to_dict()['token_type'] ==token_type.variable_name):
        variable = Match(token_type.variable_name, j, Tokens)
        children.append(variable["node"])
        out_dict = Term(variable['index'], Tokens)
        children.append(out_dict["node"])
        Node=Tree('Terms',children)
        output["node"]=Node
        output["index"]=out_dict["index"]
        return output
    else:
        anonymous = Match(token_type.Anonymous, j, Tokens)
        children.append(anonymous["node"])
        out_dict = Term(anonymous['index'], Tokens)
        children.append(out_dict["node"])
        Node=Tree('Terms',children)
        output["node"]=Node
        output["index"]=out_dict["index"]
        return output

def Term(j, Tokens):
    # Terms → , value term | , variable term | , - term | ε
    output = dict()
    children=[]
    if(Tokens[j].to_dict()['token_type']==token_type.comma):
        comma = Match(token_type.comma, j, Tokens)
        children.append(comma["node"])
        if(Tokens[comma["index"]].to_dict()['token_type'] in [token_type.Integer, token_type.Real, token_type.Char, token_type.String]):
            value = Match_value(j, Tokens)
            children.append(value["node"])
            out_dict = Term(value['index'], Tokens)
            children.append(out_dict["node"])
            Node=Tree('Term',children)
            output["node"]=Node
            output["index"]= out_dict['index']
            return output
        elif(Tokens[comma["index"]].to_dict()['token_type'] ==token_type.variable_name):
            variable = Match(token_type.variable_name, comma["index"], Tokens)
            children.append(variable["node"])
            out_dict = Term(variable['index'], Tokens)
            children.append(out_dict["node"])
            Node=Tree('Term',children)
            output["node"]=Node
            output["index"]= out_dict['index']
            return output
        else:
            anonymous = Match(token_type.Anonymous, comma["index"], Tokens)
            children.append(anonymous["node"])
            out_dict = Term(anonymous['index'], Tokens)
            children.append(out_dict["node"])
            Node=Tree('Terms',children)
            output["node"]=Node
            output["index"]= out_dict['index']
            return output
    else:
        Node=Tree('Term',children)
        output["node"]=Node
        output["index"]=j
        return output
 
def Rule(j, Tokens):
    # Rule → head :- body .
    output = dict()
    children=[]
    out_dict = Head(j, Tokens)
    children.append(out_dict['node'])
    colon_dash = Match(token_type.colon_dash, out_dict["index"], Tokens)
    children.append(colon_dash["node"])
    out_dict = Body(colon_dash["index"], Tokens)
    children.append(out_dict['node'])
    Node=Tree('Rule',children)
    output["node"]=Node
    output["index"]=out_dict["index"]
    return output

def Is_Rule(j, Tokens):
    while j < len(Tokens):
        if(Tokens[j].token_type == token_type.colon_dash):
            return True
        elif(Tokens[j].token_type == token_type.dot):
            return False
        j += 1
    return False