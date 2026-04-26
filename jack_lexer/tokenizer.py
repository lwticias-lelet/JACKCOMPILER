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

