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

