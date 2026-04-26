from utils import convert_symbol

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.i = 0
        self.out = []

    def parse(self):
        self.compileClass()
        return "\n".join(self.out)

    def current(self):
        return self.tokens[self.i]

    def advance(self):
        self.i += 1

    def write(self, line):
        self.out.append(line)

    def write_token(self):
        t = self.current()
        val = convert_symbol(t.value) if t.type == "symbol" else t.value
        self.write(f"<{t.type}> {val} </{t.type}>")
        self.advance()

    def open(self, tag):
        self.write(f"<{tag}>")

    def close(self, tag):
        self.write(f"</{tag}>")

    def compileClass(self):
        self.open("class")

        self.write_token()
        self.write_token()
        self.write_token()

        while self.current().value in ("static", "field"):
            self.compileClassVarDec()

        while self.current().value in ("constructor", "function", "method"):
            self.compileSubroutine()

        self.write_token()

        self.close("class")

    def compileClassVarDec(self):
        self.open("classVarDec")
        while self.current().value != ";":
            self.write_token()
        self.write_token()
        self.close("classVarDec")

    def compileSubroutine(self):
        self.open("subroutineDec")

        self.write_token()
        self.write_token()
        self.write_token()
        self.write_token()

        self.compileParameterList()

        self.write_token()

        self.compileSubroutineBody()

        self.close("subroutineDec")

    def compileParameterList(self):
        self.open("parameterList")
        while self.current().value != ")":
            self.write_token()
        self.close("parameterList")

    def compileSubroutineBody(self):
        self.open("subroutineBody")

        self.write_token()

        while self.current().value == "var":
            self.compileVarDec()

        self.compileStatements()

        self.write_token()

        self.close("subroutineBody")

    def compileVarDec(self):
        self.open("varDec")
        while self.current().value != ";":
            self.write_token()
        self.write_token()
        self.close("varDec")

    def compileStatements(self):
        self.open("statements")

        while self.current().value in ("let", "if", "while", "do", "return"):
            if self.current().value == "let":
                self.compileLet()
            elif self.current().value == "if":
                self.compileIf()
            elif self.current().value == "while":
                self.compileWhile()
            elif self.current().value == "do":
                self.compileDo()
            elif self.current().value == "return":
                self.compileReturn()

        self.close("statements")

    def compileLet(self):
        self.open("letStatement")

        self.write_token()
        self.write_token()

        if self.current().value == "[":
            self.write_token()
            self.compileExpression()
            self.write_token()

        self.write_token()
        self.compileExpression()
        self.write_token()

        self.close("letStatement")

    def compileIf(self):
        self.open("ifStatement")

        self.write_token()
        self.write_token()
        self.compileExpression()
        self.write_token()

        self.write_token()
        self.compileStatements()
        self.write_token()

        if self.current().value == "else":
            self.write_token()
            self.write_token()
            self.compileStatements()
            self.write_token()

        self.close("ifStatement")

    def compileWhile(self):
        self.open("whileStatement")

        self.write_token()
        self.write_token()
        self.compileExpression()
        self.write_token()

        self.write_token()
        self.compileStatements()
        self.write_token()

        self.close("whileStatement")

    def compileDo(self):
        self.open("doStatement")

        while self.current().value != ";":
            self.write_token()

        self.write_token()

        self.close("doStatement")

    def compileReturn(self):
        self.open("returnStatement")

        self.write_token()

        if self.current().value != ";":
            self.compileExpression()

        self.write_token()

        self.close("returnStatement")

    def compileExpression(self):
        self.open("expression")

        self.compileTerm()

        while self.current().value in "+-*/&|<>=~":
            self.write_token()
            self.compileTerm()

        self.close("expression")

    def compileTerm(self):
        self.open("term")
        self.write_token()
        self.close("term")