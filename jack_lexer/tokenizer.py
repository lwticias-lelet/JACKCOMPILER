import re

KEYWORDS = {
    "class","constructor","function","method",
    "field","static","var","int","char","boolean",
    "void","true","false","null","this",
    "let","do","if","else","while","return"
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

            if c == '"':
                j = i + 1
                while j < len(self.code) and self.code[j] != '"':
                    j += 1
                val = self.code[i+1:j]
                self.tokens.append(Token("stringConstant", val))
                i = j + 1
                continue

            if c in SYMBOLS:
                self.tokens.append(Token("symbol", c))
                i += 1
                continue

            if c.isdigit():
                j = i
                while j < len(self.code) and self.code[j].isdigit():
                    j += 1
                val = self.code[i:j]
                self.tokens.append(Token("integerConstant", val))
                i = j
                continue

            if c.isalpha() or c == "_":
                j = i
                while j < len(self.code) and (self.code[j].isalnum() or self.code[j] == "_"):
                    j += 1
                val = self.code[i:j]

                if val in KEYWORDS:
                    self.tokens.append(Token("keyword", val))
                else:
                    self.tokens.append(Token("identifier", val))

                i = j
                continue

            else:
                i += 1

    def get_tokens(self):
        return self.tokens
    