from enum import Enum


class TokenType(Enum):
    LEFT_PAREN = "{"
    RIGHT_PAREN = "}"
    LEFT_BRACE = "("
    RIGHT_BRACE = ")"
    COMMA = ","
    DOT = "."
    MINUS = "-"
    PLUS = "+"
    SEMICOLON = ";"
    SLASH = "/"
    STAR = "*"
    SINGLE_QUOTE = '"'

    # One or two character tokens.
    BANG = "!"
    BANG_EQUAL = "!="
    EQUAL = "="
    EQUAL_EQUAL = "=="
    GREATER = ">"
    GREATER_EQUAL = ">="
    LESS = "<"
    LESS_EQUAL = "<="

    # Literals.
    IDENTIFIER = "IDENTIFIER"
    STRING = "STRING"
    NUMBER = "NUMBER"

    # SPACE, TABS, NEWLINE
    EOF = auto()
    SPACE = " "
    TAB = "\t"
    NEWLINE = "\n"

    # keywords
    KEYWORDS = "KEYWORDS"

    # comments
    COMMENT = "COMMENT"


# Holds additional data for each token
class Token:
    def __init__(
        self, token_type: TokenType, lexem: str, start_pos: int, end_pos: int
    ):
        self.token_type: TokenType = token_type
        self.lexem: str = lexem
        self.start_pos: int = start_pos
        self.end_pos: int = end_pos
        self.length = len(lexem)
