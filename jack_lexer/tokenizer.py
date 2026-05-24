import re

KEYWORDS = {
    "class", "constructor", "function", "method",
    "field", "static", "var", "int", "char",
    "boolean", "void", "true", "false",
    "null", "this", "let", "do", "if",
    "else", "while", "return"
}

SYMBOLS = set("{}()[].,;+-*/&|<>=~")


class Token:
    def __init__(self, token_type, value):
        self.type = token_type
        self.value = value


class JackTokenizer:

    def __init__(self, code):
        self.code = self.remove_comments(code)
        self.tokens = []
        self.current = 0
        self.tokenize()

    def remove_comments(self, code):
        code = re.sub(r"//.*", "", code)
        code = re.sub(r"/\*.*?\*/", "", code, flags=re.DOTALL)
        return code

    def tokenize(self):

        i = 0

        while i < len(self.code):

            c = self.code[i]

            if c.isspace():
                i += 1
                continue

            # STRING
            if c == '"':
                j = i + 1

                while self.code[j] != '"':
                    j += 1

                value = self.code[i + 1:j]

                self.tokens.append(
                    Token("stringConstant", value)
                )

                i = j + 1
                continue

            # SYMBOL
            if c in SYMBOLS:
                self.tokens.append(
                    Token("symbol", c)
                )

                i += 1
                continue

            # INTEGER
            if c.isdigit():

                j = i

                while j < len(self.code) and self.code[j].isdigit():
                    j += 1

                value = self.code[i:j]

                self.tokens.append(
                    Token("integerConstant", value)
                )

                i = j
                continue

            # IDENTIFIER / KEYWORD
            if c.isalpha() or c == "_":

                j = i

                while (
                    j < len(self.code)
                    and (
                        self.code[j].isalnum()
                        or self.code[j] == "_"
                    )
                ):
                    j += 1

                value = self.code[i:j]

                if value in KEYWORDS:
                    token_type = "keyword"
                else:
                    token_type = "identifier"

                self.tokens.append(
                    Token(token_type, value)
                )

                i = j
                continue

            i += 1

    def get_tokens(self):
        return self.tokens