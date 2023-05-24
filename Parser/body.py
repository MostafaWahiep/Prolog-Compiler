from nltk.tree import *
from Scanner.classes import token_type
from Parser.utils import *

def Body(j, Tokens):
    # Body → body_predcate body_tail .
    output = dict()
    children=[]
    body_predcate = Body_Predcate(j, Tokens)
    children.append(body_predcate["node"])
    body_tail = Body_Tail(body_predcate["index"], Tokens)
    children.append(body_tail["node"])
    dot = Match(token_type.dot, body_tail["index"], Tokens)
    children.append(dot["node"])
    Node=Tree('Body',children)
    output["node"]=Node
    output["index"]=dot["index"]
    return output

def Body_Tail(j, Tokens):
    # Body_Tail → , Body_Predcate Body_Tail | ; Body_Predcate Body_Tail | ε
    output = dict()
    children=[]
    if(j >= len(Tokens)):
        Node=Tree('Body_Tail',children)
        output["node"]=Node
        output["index"]=j
        return output
    if(Tokens[j].to_dict()['token_type'] == token_type.comma):
        comma = Match(token_type.comma, j, Tokens)
        children.append(comma["node"])
        body_predcate = Body_Predcate(comma["index"], Tokens)
        children.append(body_predcate["node"])
        body_tail = Body_Tail(body_predcate["index"], Tokens)
        children.append(body_tail["node"])
        Node=Tree('Body_Tail',children)
        output["node"]=Node
        output["index"]=body_tail["index"]
        return output
    elif(Tokens[j].to_dict()['token_type'] == token_type.semicolon):
        semicolon = Match(token_type.semicolon, j, Tokens)
        children.append(semicolon["node"])
        body_predcate = Body_Predcate(semicolon["index"], Tokens)
        children.append(body_predcate["node"])
        body_tail = Body_Tail(body_predcate["index"], Tokens)
        children.append(body_tail["node"])
        Node=Tree('Body_Tail',children)
        output["node"]=Node
        output["index"]=body_tail["index"]
        return output
    else:
        Node=Tree('Body_Tail',children)
        output["node"]=Node
        output["index"]=j
        return output


def Body_Predcate(j, Tokens):
    # Body_Predcate → write_predicate | read_predicate | Condition | predicate
    output = dict()
    children=[]
    if(Tokens[j].to_dict()['token_type'] == token_type.write):
        write_predicate = Write_Predicate(j, Tokens)
        children.append(write_predicate["node"])
        Node=Tree('Body_Predcate',children)
        output["node"]=Node
        output["index"]=write_predicate["index"]
        return output
    elif(Tokens[j].to_dict()['token_type'] in [token_type.readchar, token_type.readln, token_type.readint]):
        read_predicate = Read_Predicate(j, Tokens)
        children.append(read_predicate["node"])
        Node=Tree('Body_Predcate',children)
        output["node"]=Node
        output["index"]=read_predicate["index"]
        return output
    elif is_condition(j, Tokens):
        condition = Condition(j, Tokens)
        children.append(condition["node"])
        Node=Tree('Body_Predcate',children)
        output["node"]=Node
        output["index"]=condition["index"]
        return output
    else:
        predicate = Predicate(j, Tokens)
        children.append(predicate["node"])
        Node=Tree('Body_Predcate',children)
        output["node"]=Node
        output["index"]=predicate["index"]
        return output

def is_condition(j, Tokens):
    while j < len(Tokens):
        if Tokens[j].to_dict()['token_type'] == token_type.dot:
            return False
        elif Tokens[j].to_dict()['token_type'] == token_type.semicolon:
            return False
        elif Tokens[j].to_dict()['token_type'] == token_type.comma:
            return False
        elif Tokens[j].to_dict()['token_type'] in [token_type.equal, token_type.not_equal,
             token_type.less_than, token_type.greater_than, token_type.less_equal, token_type.greater_equal]:
            return True
        j += 1

def Write_Predicate(j, Tokens):
    # write_predicate → write ( string write_list | variable write_list) 
    output = dict()
    children=[]
    write = Match(token_type.write, j, Tokens)
    children.append(write["node"])
    open_paren = Match(token_type.open_paren, write["index"], Tokens)
    children.append(open_paren["node"])
    if(Tokens[open_paren["index"]].to_dict()['token_type'] == token_type.String):
        write_item = Match(token_type.String, open_paren["index"], Tokens)
        children.append(write_item["node"])
    elif(Tokens[open_paren["index"]].to_dict()['token_type'] == token_type.variable_name):
        write_item = Match(token_type.variable_name, open_paren["index"], Tokens)
        children.append(write_item["node"])
    else:
        return error(open_paren["index"], "Syntax error : "+Tokens[j].to_dict()['Lex']+", Expected string or variable")
    write_list = Write_List(write_item["index"], Tokens)
    children.append(write_list["node"])
    close_paren = Match(token_type.close_paren, write_list["index"], Tokens)
    children.append(close_paren["node"])
    Node=Tree('Write_predicate',children)
    output["node"]=Node
    output["index"]=close_paren["index"]
    return output


def Write_List(j, Tokens):
    # write_list → , write_item write_list | ε
    output = dict()
    children=[]
    if(Tokens[j].to_dict()['token_type'] == token_type.comma):
        comma = Match(token_type.comma, j, Tokens)
        children.append(comma["node"])
        if(Tokens[comma["index"]].to_dict()['token_type'] == token_type.String):
            write_item = Match(token_type.String, comma["index"], Tokens)
            children.append(write_item["node"])
        elif(Tokens[comma["index"]].to_dict()['token_type'] == token_type.variable_name):
            write_item = Match(token_type.variable_name, comma["index"], Tokens)
            children.append(write_item["node"])
        else:
            return error(comma["index"], "Syntax error : "+Tokens[j].to_dict()['Lex']+", Expected string or variable")
        write_list = Write_List(write_item["index"], Tokens)
        write_list = Write_List(write_item["index"], Tokens)
        children.append(write_list["node"])
        Node=Tree('Write_List',children)
        output["node"]=Node
        output["index"]=write_list["index"]
        return output
    else:
        Node=Tree('Write_List',children)
        output["node"]=Node
        output["index"]=j
        return output
    
def Read_Predicate(j, Tokens):
    # read_predicate → readln ( variable ) | readint( variable ) | readchar ( variable )
    output = dict()
    children=[]
    if(Tokens[j].to_dict()['token_type'] == token_type.readln):
        read = Match(token_type.readln, j, Tokens)
        children.append(read["node"])
    elif(Tokens[j].to_dict()['token_type'] == token_type.readint):
        read = Match(token_type.readint, j, Tokens)
        children.append(read["node"])
    else:
        read = Match(token_type.readchar, j, Tokens)
        children.append(read["node"])
    open_paren = Match(token_type.open_paren, read["index"], Tokens)
    children.append(open_paren["node"])
    variable = Match(token_type.variable_name, open_paren["index"], Tokens)
    children.append(variable["node"])
    close_paren = Match(token_type.close_paren, variable["index"], Tokens)
    children.append(close_paren["node"])
    Node=Tree('Read_Predicate',children)
    output["node"]=Node
    output["index"]=close_paren["index"]
    return output

def Condition(j, Tokens):
    # Condition → Expression RelationalOP Expression
    output = dict()
    children=[]
    expression = Expression(j, Tokens)
    children.append(expression["node"])
    relational_op = RelationalOP(expression["index"], Tokens)
    children.append(relational_op["node"])
    expression = Expression(relational_op["index"], Tokens)
    children.append(expression["node"])
    Node=Tree('Condition',children)
    output["node"]=Node
    output["index"]=expression["index"]
    return output

def RelationalOP(j, Tokens):
    # RelationalOP → < | <= | > | >= | = | <>
    output = dict()
    children=[]
    if(Tokens[j].to_dict()['token_type'] in [token_type.less_than, token_type.less_equal, 
                                             token_type.greater_than, token_type.greater_equal, token_type.equal, token_type.not_equal]):
        relational_op = Match(Tokens[j].to_dict()['token_type'], j, Tokens)
        children.append(relational_op["node"])
        Node=Tree('RelationalOP',children)
        output["node"]=Node
        output["index"]=relational_op["index"]
        return output
    else:
        return error(j, "Syntax error : "+Tokens[j].to_dict()['Lex']+", Expected relational operator")

def Expression(j, Tokens):
    # Expression → Term Expression_Tail
    output = dict()
    children=[]
    term = Term(j, Tokens)
    children.append(term["node"])
    expression_tail = Expression_Tail(term["index"], Tokens)
    children.append(expression_tail["node"])
    Node=Tree('Expression',children)
    output["node"]=Node
    output["index"]=expression_tail["index"]
    return output

def Expression_Tail(j, Tokens):
    # Expression_Tail → + Term Expression_Tail | - Term Expression_Tail | ε
    output = dict()
    children=[]
    if(Tokens[j].to_dict()['token_type'] == token_type.add):
        Operator = Match(token_type.add, j, Tokens)
        children.append(Operator["node"])
    elif(Tokens[j].to_dict()['token_type'] == token_type.subtract):
        Operator = Match(token_type.subtract, j, Tokens)
        children.append(Operator["node"])
    else:
        Node=Tree('Expression_Tail',children)
        output["node"]=Node
        output["index"]=j
        return output
    term = Term(Operator["index"], Tokens)
    children.append(term["node"])
    expression_tail = Expression_Tail(term["index"], Tokens)
    children.append(expression_tail["node"])
    Node=Tree('Expression_Tail',children)
    output["node"]=Node
    output["index"]=expression_tail["index"]
    return output

def Term(j, Tokens):
    # Term → Factor Term_Tail
    output = dict()
    children=[]
    factor = Factor(j, Tokens)
    children.append(factor["node"])
    term_tail = Term_Tail(factor["index"], Tokens)
    children.append(term_tail["node"])
    Node=Tree('Term',children)
    output["node"]=Node
    output["index"]=term_tail["index"]
    return output

def Factor(j, Tokens):
    # Factor → variable | number | ( Expression )
    output = dict()
    children=[]
    if(Tokens[j].to_dict()['token_type'] == token_type.variable_name):
        variable = Match(token_type.variable_name, j, Tokens)
        children.append(variable["node"])
        Node=Tree('Factor',children)
        output["node"]=Node
        output["index"]=variable["index"]
        return output
    elif(Tokens[j].to_dict()['token_type'] == token_type.Integer):
        number = Match(token_type.Integer, j, Tokens)
        children.append(number["node"])
        Node=Tree('Factor',children)
        output["node"]=Node
        output["index"]=number["index"]
        return output
    elif(Tokens[j].to_dict()['token_type'] == token_type.Real):
        number = Match(token_type.Real, j, Tokens)
        children.append(number["node"])
        Node=Tree('Factor',children)
        output["node"]=Node
        output["index"]=number["index"]
        return output
    elif(Tokens[j].to_dict()['token_type'] == token_type.open_paren):
        open_paren = Match(token_type.open_paren, j, Tokens)
        children.append(open_paren["node"])
        expression = Expression(open_paren["index"], Tokens)
        children.append(expression["node"])
        close_paren = Match(token_type.close_paren, expression["index"], Tokens)
        children.append(close_paren["node"])
        Node=Tree('Factor',children)
        output["node"]=Node
        output["index"]=close_paren["index"]
        return output
    else:
        return error(j, "Syntax error : "+Tokens[j].to_dict()['Lex']+", Expected variable or number")
    
def Term_Tail(j, Tokens):
    # Term_Tail → * Factor Term_Tail | / Factor Term_Tail | ε
    output = dict()
    children=[]
    if(Tokens[j].to_dict()['token_type'] == token_type.multiply):
        Operator = Match(token_type.multiply, j, Tokens)
        children.append(Operator["node"])
    elif(Tokens[j].to_dict()['token_type'] == token_type.divide):
        Operator = Match(token_type.divide, j, Tokens)
        children.append(Operator["node"])
    else:
        Node=Tree('Term_Tail',children)
        output["node"]=Node
        output["index"]=j
        return output
    factor = Factor(Operator["index"], Tokens)
    children.append(factor["node"])
    term_tail = Term_Tail(factor["index"], Tokens)
    children.append(term_tail["node"])
    Node=Tree('Term_Tail',children)
    output["node"]=Node
    output["index"]=term_tail["index"]
    return output

def Predicate(j, Tokens):
    # Predicate → name ( Variables ) | name
    output = dict()
    children=[]
    name = Match(token_type.Name, j, Tokens)
    children.append(name["node"])
    if(name["index"] >= len(Tokens)):
        return error(name["index"], "Syntax error : "+Tokens[j].to_dict()['Lex']+", Expected .")
    elif(Tokens[name["index"]].to_dict()['token_type'] != token_type.open_paren):
        Node=Tree('Predicate',children)
        output["node"]=Node
        output["index"]=name["index"]
        return output
    else:
        open_paren = Match(token_type.open_paren, name["index"], Tokens)
        children.append(open_paren["node"])
        variables = Variables(open_paren["index"], Tokens)
        children.append(variables["node"])
        close_paren = Match(token_type.close_paren, variables["index"], Tokens)
        children.append(close_paren["node"])
        Node=Tree('Predicate',children)
        output["node"]=Node
        output["index"]=close_paren["index"]
        return output

def Variables(j, Tokens):
    # Variables → variable Variable_Tail | ε
    output = dict()
    children=[]
    if(Tokens[j].to_dict()['token_type'] in [token_type.variable_name, token_type.Anonymous]):
        if(Tokens[j].to_dict()['token_type'] == token_type.Anonymous):
            variable = Match(token_type.Anonymous, j, Tokens)
        else:
            variable = Match(token_type.variable_name, j, Tokens)
        children.append(variable["node"])
        variable_tail = Variable_Tail(variable["index"], Tokens)
        children.append(variable_tail["node"])
        Node=Tree('Variables',children)
        output["node"]=Node
        output["index"]=variable_tail["index"]
        return output
    else:
        Node=Tree('error',children)
        output["node"]=Node
        output["index"]=j
        return output
    
def Variable_Tail(j, Tokens):
    # Variable_Tail → , variable Variable_Tail | ε
    output = dict()
    children=[]
    if(Tokens[j].to_dict()['token_type'] == token_type.comma):
        comma = Match(token_type.comma, j, Tokens)
        children.append(comma["node"])
        if(Tokens[comma["index"]].to_dict()['token_type'] == token_type.Anonymous):
            variable = Match(token_type.Anonymous, comma["index"], Tokens)
        else:
            variable = Match(token_type.variable_name, comma["index"], Tokens)
        children.append(variable["node"])
        variable_tail = Variable_Tail(variable["index"], Tokens)
        children.append(variable_tail["node"])
        Node=Tree('Variable_Tail',children)
        output["node"]=Node
        output["index"]=variable_tail["index"]
        return output
    else:
        Node=Tree('Variable_Tail',children)
        output["node"]=Node
        output["index"]=j
        return output


