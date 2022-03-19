import os
import ast
import re
from typing import Optional, List
from enum import Enum, auto


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
    SLASH = "\/"
    STAR = "*"

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
    IDENTIFIER = auto()
    STRING = auto()
    NUMBER = auto()

    # Keywords.
    AND = "&&"
    CLASS = "class"
    ELSE = "else"
    FALSE = "false"
    FUN = "fun"
    FOR = "for"
    IF = "if"
    NIL = "nil"
    OR = "||"
    PRINT = "print"
    RETURN = "return"
    SUPER = "super"
    THIS = "this"
    TRUE = "true"
    VAR = "var"
    WHILE = "while"

    EOF = auto()


# Holds additional data for each token
class Token:
    def __init__(self, token_type: TokenType, lexem: str, cursor: int):
        self.token_type: TokenType = token_type
        self.lexem: str = lexem
        self.cursor: int = 0
        self.length = len(lexem)


class Tokenizer:
    def __init__(self, source: str):
        self.tokens: Optional[List[str]] = []
        self.has_more_tokens: bool = True
        self.current_line: str = ""
        self.source = source
        self.char_idx: int = 0

    def is_digit(self, c):
        return c >= "0" and c <= "9"

    def undo_last(self):
        self.char_idx -= 1

    def parse_operators(self, token: str):
        lexem = token
        next_token = self.get_next_token()
        lexem += next_token
        if lexem == TokenType.EQUAL_EQUAL.value:
            self.add_token(lexem)
        elif lexem == TokenType.BANG_EQUAL.value:
            self.add_token(lexem)
        elif lexem == TokenType.GREATER_EQUAL.value:
            self.add_token(lexem)
        elif lexem == TokenType.LESS_EQUAL.value:
            self.add_token(lexem)
        else:
            self.add_token(token)

    def parse_characters(
        self,
        next_token: str,
        has_quotes: bool = False,
        has_digits: bool = False,
    ):
        lexem = next_token
        done = False
        while not done:
            next_token = self.get_next_token()
            if (
                next_token == " "
                and not has_quotes
                or next_token == "\t"
                and not has_quotes
                or next_token == "\n"
                and not has_quotes
                or not next_token
            ):
                done = True
                self.add_token(lexem)
            elif next_token == '"':
                done = True
                lexem += next_token
                self.add_token(lexem)
            elif has_digits and not self.is_digit(next_token):
                done = True
                self.undo_last()
                self.add_token(lexem)
            else:
                lexem += next_token

    def parse_number(self, token: str):
        pass

    def scan(self):
        while self.has_more_tokens:
            next_token = self.get_next_token()
            if next_token == " " or next_token == "\n" or next_token == "\t":
                continue
            if next_token == TokenType.EQUAL.value:
                self.parse_operators(next_token)
            elif next_token == TokenType.BANG.value:
                self.parse_operators(next_token)
            elif next_token == TokenType.GREATER.value:
                self.parse_operators(next_token)
            elif next_token == TokenType.LESS.value:
                self.parse_operators(next_token)
            elif next_token == TokenType.SEMICOLON.value:
                self.add_token(next_token)
            elif next_token >= "a" and next_token <= "z":
                self.parse_characters(next_token)
            elif next_token == '"':
                self.parse_characters(next_token, True)
            elif self.is_digit(next_token):
                self.parse_characters(next_token, False, True)
            elif next_token == TokenType.LEFT_BRACE.value:
                self.add_token(next_token)
            elif next_token == TokenType.RIGHT_BRACE.value:
                self.add_token(next_token)
            elif next_token == TokenType.LEFT_PAREN.value:
                self.add_token(next_token)
            elif next_token == TokenType.RIGHT_PAREN.value:
                self.add_token(next_token)

    def get_next_token(self):
        if self.char_idx == len(self.source) - 1:
            self.has_more_tokens = False
            return self.source[self.char_idx]
        r = self.source[self.char_idx]
        self.char_idx += 1
        return r

    def add_token(self, lexem: str):
        self.tokens.append(lexem)

    def parse(self):
        self.scan()
        print(self.tokens)
