class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.i = 0
        self.output = []

    def peek(self):
        return self.tokens[self.i]

    def advance(self):
        token = self.tokens[self.i]
        self.i += 1
        return token

    def eat(self, ttype=None, val=None):
        token = self.advance()
        if ttype and token.type != ttype:
            raise Exception("Erro de tipo")
        if val and token.value != val:
            raise Exception("Erro de valor")
        self.write_token(token)

    def write(self, text):
        self.output.append(text)

    def write_token(self, token):
        val = token.value
        if val == "<":
            val = "&lt;"
        elif val == ">":
            val = "&gt;"
        elif val == "&":
            val = "&amp;"
        elif val == '"':
            val = "&quot;"
        self.write(f"<{token.type}> {val} </{token.type}>")

    def parse(self):
        self.compile_class()
        return "\n".join(self.output)

    def compile_class(self):
        self.write("<class>")
        self.eat("keyword", "class")
        self.eat("identifier")
        self.eat("symbol", "{")

        while self.peek().value in ["static", "field"]:
            self.compile_class_var_dec()

        while self.peek().value in ["constructor", "function", "method"]:
            self.compile_subroutine()

        self.eat("symbol", "}")
        self.write("</class>")

    def compile_class_var_dec(self):
        self.write("<classVarDec>")
        self.eat("keyword")
        self.eat()
        self.eat("identifier")

        while self.peek().value == ",":
            self.eat("symbol", ",")
            self.eat("identifier")

        self.eat("symbol", ";")
        self.write("</classVarDec>")

    def compile_subroutine(self):
        self.write("<subroutineDec>")
        self.eat("keyword")
        self.eat()
        self.eat("identifier")
        self.eat("symbol", "(")
        self.compile_parameter_list()
        self.eat("symbol", ")")
        self.compile_subroutine_body()
        self.write("</subroutineDec>")

    def compile_parameter_list(self):
        self.write("<parameterList>")
        if self.peek().value != ")":
            self.eat()
            self.eat("identifier")
            while self.peek().value == ",":
                self.eat("symbol", ",")
                self.eat()
                self.eat("identifier")
        self.write("</parameterList>")

    def compile_subroutine_body(self):
        self.write("<subroutineBody>")
        self.eat("symbol", "{")

        while self.peek().value == "var":
            self.compile_var_dec()

        self.compile_statements()
        self.eat("symbol", "}")
        self.write("</subroutineBody>")

    def compile_var_dec(self):
        self.write("<varDec>")
        self.eat("keyword", "var")
        self.eat()
        self.eat("identifier")

        while self.peek().value == ",":
            self.eat("symbol", ",")
            self.eat("identifier")

        self.eat("symbol", ";")
        self.write("</varDec>")

    def compile_statements(self):
        self.write("<statements>")
        while self.peek().value in ["let", "if", "while", "do", "return"]:
            if self.peek().value == "let":
                self.compile_let()
            elif self.peek().value == "if":
                self.compile_if()
            elif self.peek().value == "while":
                self.compile_while()
            elif self.peek().value == "do":
                self.compile_do()
            elif self.peek().value == "return":
                self.compile_return()
        self.write("</statements>")

    def compile_let(self):
        self.write("<letStatement>")
        self.eat("keyword", "let")
        self.eat("identifier")

        if self.peek().value == "[":
            self.eat("symbol", "[")
            self.compile_expression()
            self.eat("symbol", "]")

        self.eat("symbol", "=")
        self.compile_expression()
        self.eat("symbol", ";")
        self.write("</letStatement>")

    def compile_if(self):
        self.write("<ifStatement>")
        self.eat("keyword", "if")
        self.eat("symbol", "(")
        self.compile_expression()
        self.eat("symbol", ")")
        self.eat("symbol", "{")
        self.compile_statements()
        self.eat("symbol", "}")

        if self.peek().value == "else":
            self.eat("keyword", "else")
            self.eat("symbol", "{")
            self.compile_statements()
            self.eat("symbol", "}")

        self.write("</ifStatement>")

    def compile_while(self):
        self.write("<whileStatement>")
        self.eat("keyword", "while")
        self.eat("symbol", "(")
        self.compile_expression()
        self.eat("symbol", ")")
        self.eat("symbol", "{")
        self.compile_statements()
        self.eat("symbol", "}")
        self.write("</whileStatement>")

    def compile_do(self):
        self.write("<doStatement>")
        self.eat("keyword", "do")
        self.compile_subroutine_call()
        self.eat("symbol", ";")
        self.write("</doStatement>")

    def compile_return(self):
        self.write("<returnStatement>")
        self.eat("keyword", "return")

        if self.peek().value != ";":
            self.compile_expression()

        self.eat("symbol", ";")
        self.write("</returnStatement>")

    def compile_expression(self):
        self.write("<expression>")
        self.compile_term()

        while self.peek().value in ["+", "-", "*", "/", "&", "|", "<", ">", "="]:
            self.eat("symbol")
            self.compile_term()

        self.write("</expression>")

    def compile_term(self):
        self.write("<term>")
        token = self.peek()

        if token.type == "integerConstant":
            self.eat("integerConstant")

        elif token.type == "stringConstant":
            self.eat("stringConstant")

        elif token.type == "keyword":
            self.eat("keyword")

        elif token.value == "(":
            self.eat("symbol", "(")
            self.compile_expression()
            self.eat("symbol", ")")

        elif token.value in ["-", "~"]:
            self.eat("symbol")
            self.compile_term()

        elif token.type == "identifier":
            self.eat("identifier")

            if self.peek().value == "[":
                self.eat("symbol", "[")
                self.compile_expression()
                self.eat("symbol", "]")

            elif self.peek().value in ["(", "."]:
                self.compile_subroutine_call_rest()

        self.write("</term>")

    def compile_subroutine_call(self):
        self.eat("identifier")
        self.compile_subroutine_call_rest()

    def compile_subroutine_call_rest(self):
        if self.peek().value == ".":
            self.eat("symbol", ".")
            self.eat("identifier")

        self.eat("symbol", "(")
        self.compile_expression_list()
        self.eat("symbol", ")")

    def compile_expression_list(self):
        self.write("<expressionList>")
        if self.peek().value != ")":
            self.compile_expression()
            while self.peek().value == ",":
                self.eat("symbol", ",")
                self.compile_expression()
        self.write("</expressionList>")