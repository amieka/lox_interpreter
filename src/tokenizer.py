import os
import ast
import re
from typing import Optional, List
from enum import Enum, auto


class UnsupportedNumberException(BaseException):
    pass


class UnsupportedCharacterException(BaseException):
    pass


class UnsupportedCommentException(BaseException):
    pass


_KEYWORDS = {
    "AND": "&&",
    "CLASS": "class",
    "ELSE": "else",
    "FALSE": "false",
    "FUN": "fun",
    "FOR": "for",
    "IF": "if",
    "NIL": "nil",
    "OR": "||",
    "PRINT": "print",
    "RETURN": "return",
    "SUPER": "super",
    "THIS": "this",
    "TRUE": "true",
    "VAR": "var",
    "WHILE": "while",
}


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


class Tokenizer:
    def __init__(self, source: str):
        self.tokens: Optional[List[Token]] = []
        self.keywords: Optional[List[str]] = []
        self.has_more_tokens: bool = True
        self.current_line: str = ""
        self.source = source
        self.char_idx: int = 0

    def is_digit(self, c):
        return c >= "0" and c <= "9"

    def is_alpha(self, c):
        return c >= "a" and c <= "z" or c >= "A" and c <= "Z"

    def undo_last(self):
        self.char_idx -= 1

    def parse_operators(self, token: str):
        lexem = token
        start_pos = self.char_idx
        next_token = self.get_next_token()
        end_pos = self.char_idx
        lexem += next_token
        if lexem == TokenType.EQUAL_EQUAL.value:
            self.add_token(lexem, start_pos, end_pos, TokenType.EQUAL_EQUAL)
        elif lexem == TokenType.BANG_EQUAL.value:
            self.add_token(lexem, start_pos, end_pos, TokenType.BANG_EQUAL)
        elif lexem == TokenType.GREATER_EQUAL.value:
            self.add_token(lexem, start_pos, end_pos, TokenType.GREATER_EQUAL)
        elif lexem == TokenType.LESS_EQUAL.value:
            self.add_token(lexem, start_pos, end_pos, TokenType.LESS_EQUAL)
        else:
            self.add_token(lexem, start_pos, end_pos, TokenType.LESS_EQUAL)

    def capture_keywords(self, lexem: str, start_pos: int, end_pos: int):
        # token_type: TokenType = None
        # if not TokenType[lexem.upper()]:
        #     self.add_token(lexem, start_pos, end_pos, TokenType.IDENTIFIER)
        # else:
        #     self.add_token(lexem, start_pos, end_pos, TokenType[lexem])
        print(f"possible keyword {lexem}")
        if _KEYWORDS.get(lexem.upper()) is not None:
            self.add_token(lexem, start_pos, end_pos, TokenType.KEYWORDS)
        else:
            self.add_token(lexem, start_pos, end_pos, TokenType.IDENTIFIER)

    def parse_characters(
        self,
        next_token: str,
        has_quotes: bool = False,
        has_digits: bool = False,
    ):
        lexem = next_token
        done = False
        start_pos = self.char_idx
        while not done:
            next_token = self.get_next_token()
            if (
                next_token == TokenType.SPACE.value
                and not has_quotes
                or next_token == TokenType.TAB.value
                and not has_quotes
                or next_token == TokenType.NEWLINE.value
                and not has_quotes
                or not next_token
            ):
                done = True
                # check for keywords here
                end_pos = self.char_idx
                self.capture_keywords(lexem, start_pos, end_pos)
            elif next_token == TokenType.SINGLE_QUOTE.value:
                done = True
                lexem += next_token
                end_pos = self.char_idx
                self.add_token(lexem, start_pos, end_pos, TokenType.STRING)
            else:
                lexem += next_token

    def check_unsupported_number(self):
        if self.is_digit(self.get_next_token()):
            self.undo_last()
            raise UnsupportedNumberException()

    def parse_number(self, token: str):
        lexem = token
        done = False
        decimal_count = 0
        start_pos = self.char_idx
        while not done:
            next_token = self.get_next_token()
            if (
                next_token == TokenType.SPACE.value
                or next_token == TokenType.TAB.value
                or next_token == TokenType.NEWLINE.value
            ):
                raise UnsupportedNumberException()
            elif decimal_count > 1:
                raise UnsupportedNumberException()
            elif self.is_alpha(next_token):
                raise UnsupportedNumberException()
            elif next_token == TokenType.DOT.value:
                lexem += next_token
                decimal_count += 1
                continue
            elif not self.is_digit(next_token):
                self.undo_last()
                done = True
                end_pos = self.char_idx
                self.add_token(lexem, start_pos, end_pos, TokenType.NUMBER)
            else:
                lexem += next_token

    def capture_comments(self):
        done = False
        lexem = ""
        start_pos = self.char_idx
        next_token = self.get_next_token()
        # TODO: capture c style comments
        if not next_token == TokenType.SLASH.value:
            raise UnsupportedCommentException()
        if next_token == TokenType.SLASH.value:
            while not done:
                next_token = self.get_next_token()
                lexem += next_token
                if next_token == TokenType.NEWLINE.value:
                    done = True
                    self.undo_last()
                    end_pos = self.char_idx
                    self.add_token(
                        lexem, start_pos, end_pos, TokenType.SEMICOLON
                    )

    def advance_char(self):
        self.char_idx += 1

    def scan(self):
        start_pos = self.char_idx
        while self.has_more_tokens:
            next_token = self.get_next_token()
            end_pos = self.char_idx
            # skip over space, tabs and new line
            if (
                next_token == TokenType.SPACE.value
                or next_token == TokenType.NEWLINE.value
                or next_token == TokenType.TAB.value
            ):
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
                self.add_token(
                    next_token, start_pos, end_pos, TokenType.SEMICOLON
                )
            elif self.is_alpha(next_token):
                self.parse_characters(next_token)
            elif next_token == TokenType.SINGLE_QUOTE.value:
                self.parse_characters(next_token, True)
            elif self.is_digit(next_token):
                self.parse_number(next_token)
            elif next_token == TokenType.LEFT_BRACE.value:
                self.add_token(
                    next_token, start_pos, end_pos, TokenType.LEFT_BRACE
                )
            elif next_token == TokenType.RIGHT_BRACE.value:
                self.add_token(
                    next_token, start_pos, end_pos, TokenType.RIGHT_BRACE
                )
            elif next_token == TokenType.LEFT_PAREN.value:
                self.add_token(
                    next_token, start_pos, end_pos, TokenType.LEFT_PAREN
                )
            elif next_token == TokenType.RIGHT_PAREN.value:
                self.add_token(
                    next_token, start_pos, end_pos, TokenType.RIGHT_PAREN
                )
            elif next_token == TokenType.DOT.value:
                self.check_unsupported_number()  # there is a better way to handle this ?
            elif next_token == TokenType.SLASH.value:
                self.capture_comments()

    def get_next_token(self):
        if self.char_idx == len(self.source) - 1:
            self.has_more_tokens = False
            return self.source[self.char_idx]
        r = self.source[self.char_idx]
        self.char_idx += 1
        return r

    # def add_token(self, lexem: str):
    #     self.tokens.append(lexem)

    def add_token(
        self, lexem: str, start_pos: int, end_pos: int, token_type: TokenType
    ):
        t_token = Token(token_type, lexem, start_pos, end_pos)
        self.tokens.append(t_token)

    def parse(self):
        self.scan()
        # print(str(self.tokens))
        for t in self.tokens:
            print(f"{t.start_pos}, {t.end_pos}, {t.lexem}, {t.token_type}")
