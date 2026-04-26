class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.i = 0
        self.output = []
        self.indent = 0

    # =============================
    # UTIL
    # =============================

    def peek(self):
        if self.i < len(self.tokens):
            return self.tokens[self.i]
        return None

    def advance(self):
        tok = self.tokens[self.i]
        self.i += 1
        return tok

    def write(self, text):
        self.output.append("  " * self.indent + text)

    def open_tag(self, tag):
        self.write(f"<{tag}>")
        self.indent += 1

    def close_tag(self, tag):
        self.indent -= 1
        self.write(f"</{tag}>")

    def write_token(self, token):
        val = token.value
        if val == "<": val = "&lt;"
        elif val == ">": val = "&gt;"
        elif val == "&": val = "&amp;"
        elif val == '"': val = "&quot;"
        self.write(f"<{token.type}> {val} </{token.type}>")

    # =============================
    # ENTRY
    # =============================

    def parse(self):
        self.compile_class()
        return "\n".join(self.output)

    # =============================
    # CLASS
    # =============================

    def compile_class(self):
        self.open_tag("class")

        self.write_token(self.advance())
        self.write_token(self.advance())
        self.write_token(self.advance())

        while self.peek() and self.peek().value in ["static", "field"]:
            self.compile_class_var_dec()

        while self.peek() and self.peek().value in ["constructor", "function", "method"]:
            self.compile_subroutine()

        self.write_token(self.advance())

        self.close_tag("class")

    def compile_class_var_dec(self):
        self.open_tag("classVarDec")

        self.write_token(self.advance())
        self.write_token(self.advance())
        self.write_token(self.advance())

        while self.peek() and self.peek().value == ",":
            self.write_token(self.advance())
            self.write_token(self.advance())

        self.write_token(self.advance())

        self.close_tag("classVarDec")

    # =============================
    # SUBROUTINE
    # =============================

    def compile_subroutine(self):
        self.open_tag("subroutineDec")

        self.write_token(self.advance())
        self.write_token(self.advance())
        self.write_token(self.advance())
        self.write_token(self.advance())

        self.compile_parameter_list()

        self.write_token(self.advance())

        self.compile_subroutine_body()

        self.close_tag("subroutineDec")

    def compile_parameter_list(self):
        self.open_tag("parameterList")

        if self.peek().value != ")":
            self.write_token(self.advance())
            self.write_token(self.advance())

            while self.peek().value == ",":
                self.write_token(self.advance())
                self.write_token(self.advance())
                self.write_token(self.advance())

        self.close_tag("parameterList")

    def compile_subroutine_body(self):
        self.open_tag("subroutineBody")

        self.write_token(self.advance())

        while self.peek().value == "var":
            self.compile_var_dec()

        self.compile_statements()

        self.write_token(self.advance())

        self.close_tag("subroutineBody")

    def compile_var_dec(self):
        self.open_tag("varDec")

        self.write_token(self.advance())
        self.write_token(self.advance())
        self.write_token(self.advance())

        while self.peek().value == ",":
            self.write_token(self.advance())
            self.write_token(self.advance())

        self.write_token(self.advance())

        self.close_tag("varDec")

    # =============================
    # STATEMENTS
    # =============================

    def compile_statements(self):
        self.open_tag("statements")

        while self.peek() and self.peek().value in ["let", "if", "while", "do", "return"]:
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

        self.close_tag("statements")

    def compile_let(self):
        self.open_tag("letStatement")

        self.write_token(self.advance())
        self.write_token(self.advance())

        if self.peek().value == "[":
            self.write_token(self.advance())
            self.compile_expression()
            self.write_token(self.advance())

        self.write_token(self.advance())

        self.compile_expression()

        self.write_token(self.advance())

        self.close_tag("letStatement")

    def compile_if(self):
        self.open_tag("ifStatement")

        self.write_token(self.advance())
        self.write_token(self.advance())

        self.compile_expression()

        self.write_token(self.advance())
        self.write_token(self.advance())

        self.compile_statements()

        self.write_token(self.advance())

        if self.peek() and self.peek().value == "else":
            self.write_token(self.advance())
            self.write_token(self.advance())
            self.compile_statements()
            self.write_token(self.advance())

        self.close_tag("ifStatement")

    def compile_while(self):
        self.open_tag("whileStatement")

        self.write_token(self.advance())
        self.write_token(self.advance())

        self.compile_expression()

        self.write_token(self.advance())
        self.write_token(self.advance())

        self.compile_statements()

        self.write_token(self.advance())

        self.close_tag("whileStatement")

    def compile_do(self):
        self.open_tag("doStatement")

        self.write_token(self.advance())

        self.compile_subroutine_call()

        self.write_token(self.advance())

        self.close_tag("doStatement")

    def compile_return(self):
        self.open_tag("returnStatement")

        self.write_token(self.advance())

        if self.peek().value != ";":
            self.compile_expression()

        self.write_token(self.advance())

        self.close_tag("returnStatement")

    # =============================
    # EXPRESSIONS
    # =============================

    def compile_expression(self):
        self.open_tag("expression")

        self.compile_term()

        while self.peek() and self.peek().value in ['+', '-', '*', '/', '&', '|', '<', '>', '=']:
            self.write_token(self.advance())
            self.compile_term()

        self.close_tag("expression")

    def compile_term(self):
        self.open_tag("term")

        token = self.advance()

        if token.type in ["integerConstant", "stringConstant", "keyword"]:
            self.write_token(token)

        elif token.type == "identifier":
            self.write_token(token)

            if self.peek() and self.peek().value == "[":
                self.write_token(self.advance())
                self.compile_expression()
                self.write_token(self.advance())

            elif self.peek() and self.peek().value in ["(", "."]:
                if self.peek().value == ".":
                    self.write_token(self.advance())
                    self.write_token(self.advance())

                self.write_token(self.advance())
                self.compile_expression_list()
                self.write_token(self.advance())

        elif token.value == "(":
            self.write_token(token)
            self.compile_expression()
            self.write_token(self.advance())

        elif token.value in ["-", "~"]:
            self.write_token(token)
            self.compile_term()

        self.close_tag("term")

    def compile_expression_list(self):
        self.open_tag("expressionList")

        if self.peek() and self.peek().value != ")":
            self.compile_expression()

            while self.peek().value == ",":
                self.write_token(self.advance())
                self.compile_expression()

        self.close_tag("expressionList")

    def compile_subroutine_call(self):
        self.write_token(self.advance())

        if self.peek().value == ".":
            self.write_token(self.advance())
            self.write_token(self.advance())

        self.write_token(self.advance())

        self.compile_expression_list()

        self.write_token(self.advance())