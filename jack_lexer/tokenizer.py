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
    def __init__(self, t, v):
        self.type = t
        self.value = v


class JackTokenizer:

    def __init__(self, code):
        self.code = self.clean(code)
        self.tokens = []
        self.tokenize()

    def clean(self, code):

        # remove comentários simples
        code = re.sub(r"//.*", "", code)

        # remove comentários multilinha
        code = re.sub(r"/\*.*?\*/", "", code, flags=re.DOTALL)

        return code

    def tokenize(self):

        i = 0
        n = len(self.code)

        while i < n:

            c = self.code[i]

            # espaços
            if c.isspace():
                i += 1
                continue

            # string
            if c == '"':

                j = i + 1

                while self.code[j] != '"':
                    j += 1

                value = self.code[i + 1:j]

                self.tokens.append(Token("stringConstant", value))

                i = j + 1
                continue

            # símbolos
            if c in SYMBOLS:
                self.tokens.append(Token("symbol", c))
                i += 1
                continue

            # números
            if c.isdigit():

                j = i

                while j < n and self.code[j].isdigit():
                    j += 1

                value = self.code[i:j]

                self.tokens.append(Token("integerConstant", value))

                i = j
                continue

            # identificadores
            if c.isalpha() or c == "_":

                j = i

                while j < n and (
                    self.code[j].isalnum()
                    or self.code[j] == "_"
                ):
                    j += 1

                value = self.code[i:j]

                if value in KEYWORDS:
                    self.tokens.append(Token("keyword", value))
                else:
                    self.tokens.append(Token("identifier", value))

                i = j
                continue

            i += 1

    def get_tokens(self):
        return self.tokens