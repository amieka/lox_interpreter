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
    def __init__(self, scan_lines: Optional[List]):
        self.tokens: Optional[List[str]] = []
        self.has_more_tokens: bool = False
        self.scan_lines: Optional[List] = scan_lines
        self.lines_to_scan: int = len(scan_lines)
        self.line_cursor: int = 0
        self.current_line: str = ""

    def _scan_next(self):
        pass

    def _stop_scan(self):
        pass

    def _parse_operators(self, token: str):
        lexem = token
        line = self.current_line
        next_token = self._get_next_token(line)
        lexem += next_token
        if lexem == TokenType.EQUAL_EQUAL.value:
            self._add_token(lexem)
        elif lexem == TokenType.BANG_EQUAL.value:
            self._add_token(lexem)
        elif lexem == TokenType.GREATER_EQUAL.value:
            self._add_token(lexem)
        elif lexem == TokenType.LESS_EQUAL.value:
            self._add_token(lexem)
        else:
            self._add_token(token)

    def _parse_characters(self, next_token: str, has_quotes: bool = False):
        lexem = next_token
        done = False
        line = self.current_line
        while not done:
            next_token = self._get_next_token(line)
            if (
                next_token == " "
                and not has_quotes
                or next_token == "\t"
                and not has_quotes
                or next_token == "\n"
                and not has_quotes
                or self.line_cursor == len(line)
            ):
                done = True
                self._add_token(lexem)
            elif next_token == '"':
                done = True
                lexem += next_token
                self._add_token(lexem)
            else:
                lexem += next_token

    def _parse_number(self, token: str):
        pass

    def _parse_line(self, line: str):
        self.line_cursor = 0
        self.current_line = line
        while self.line_cursor < len(line):
            next_token = self._get_next_token(line)
            if next_token == " " or next_token == "\n" or next_token == "\t":
                continue
            if next_token == TokenType.EQUAL.value:
                self._parse_operators(next_token)
            elif next_token == TokenType.BANG.value:
                self._parse_operators(next_token)
            elif next_token == TokenType.GREATER.value:
                self._parse_operators(next_token)
            elif next_token == TokenType.LESS.value:
                self._parse_operators(next_token)
            elif next_token == TokenType.SEMICOLON.value:
                self._add_token(next_token)
            elif next_token >= "a" and next_token <= "z":
                self._parse_characters(next_token)
            elif next_token == '"':
                self._parse_characters(next_token, True)
            elif next_token >= "0" and next_token <= "9":
                self._parse_characters(next_token)
            elif next_token == TokenType.LEFT_BRACE.value:
                self._add_token(next_token)
            elif next_token == TokenType.RIGHT_BRACE.value:
                self._add_token(next_token)
            elif next_token == TokenType.LEFT_PAREN.value:
                self._add_token(next_token)
            elif next_token == TokenType.RIGHT_PAREN.value:
                self._add_token(next_token)

                # parse a begining of a double quoted string

    def _get_next_token(self, line: str):
        if self.line_cursor == len(line):
            return line[self.line_cursor]
        r = line[self.line_cursor]
        self.line_cursor += 1
        return r

    def _add_token(self, lexem: str):
        self.tokens.append(lexem)

    def _parse(self):
        for line in self.scan_lines:
            self._parse_line(line)
        print(self.tokens)

    # def __call__(self):
    #     # start parsing
    #     self._parse()


def parse():
    with open("second.lox") as code_file:
        lines = code_file.readlines()
        tokenizer = Tokenizer(scan_lines=lines)
        tokenizer._parse()


if __name__ == "__main__":
    parse()
