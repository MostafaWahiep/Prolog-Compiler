from enum import Enum


#prolog valid tokens
class token_type(Enum):
    # Predicates, clauses, and goals
    Predicate = 1
    Clause = 2
    Goal = 3

    # Data types
    Integer = 4  # 25
    Real = 5  # 3.14
    Name = 6  # a, b
    Char = 7  # 'a'
    String = 8  # "ahjgj"
    Anonymous = 9  # _
    variable_name = 10
    data_type = 11  #integer , char , string , symbol , real

    # Comparison operators
    equal = 12
    not_equal = 13
    less_than = 14
    greater_than = 15
    less_equal = 16
    greater_equal = 17

    # Arithmetic operators
    add = 18
    subtract = 19
    multiply = 20
    divide = 21

    # Comments and I/O statements
    Comment = 22
    write = 23
    readln = 24
    readint = 25
    readchar = 26

    # Punctuation
    double_quote = 27  # single quote
    colon_dash = 28  # :-
    dot = 29
    open_paren = 30
    close_paren = 31
    comma = 32  # and , ","
    semicolon = 33  # or
    line_comment = 34  # %
    mline_comment = 35  # /* */
    '''# Names
    predicate_name = 35
    clause_name = 37
    goal_name = 38'''
    # Errors
    Error = 36


class token:
    def __init__(self, lex, token_type):
        self.lex = lex
        self.token_type = token_type

    def to_dict(self):
        return {'Lex': self.lex, 'token_type': self.token_type}


reserved_words = {
    # Data types
    "integer": token_type.data_type,
    "char": token_type.data_type,
    "string": token_type.data_type,
    "symbol": token_type.data_type,
    "real": token_type.data_type,
    "_": token_type.Anonymous,

    # Predicates, clauses, and goals
    "predicates": token_type.Predicate,
    "clauses": token_type.Clause,
    "goal": token_type.Goal,

    # I/O statements
    "readln": token_type.readln,
    "readint": token_type.readint,
    "readchar": token_type.readchar,
    "write": token_type.write
}

reserved_operators = {
    # Comparison operators
    "=": token_type.equal,
    "<>": token_type.not_equal,
    "<": token_type.less_than,
    ">": token_type.greater_than,
    "<=": token_type.less_equal,
    ">=": token_type.greater_equal,

    # Arithmetic operators
    "+": token_type.add,
    "-": token_type.subtract,
    "*": token_type.multiply,
    "/": token_type.divide,

    # Punctuation
    ":-": token_type.colon_dash,
    ".": token_type.dot,
    "(": token_type.open_paren,
    ")": token_type.close_paren,
    "\"": token_type.double_quote,  # single quote
    ",": token_type.comma,
    ";": token_type.semicolon,
    "%": token_type.line_comment,
    "/*": token_type.mline_comment,
    "*/": token_type.mline_comment,
}
