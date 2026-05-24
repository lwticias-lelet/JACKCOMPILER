from vm_writer import VMWriter
from symbol_table import SymbolTable


class CompilationEngine:

    def __init__(self, tokens):

        self.tokens = tokens
        self.current = 0

        self.vm = VMWriter()
        self.symbol_table = SymbolTable()

        self.class_name = ""

    def peek(self):

        if self.current < len(self.tokens):
            return self.tokens[self.current]

        return None

    def advance(self):

        token = self.peek()

        self.current += 1

        return token

    def compile_class(self):

        self.advance()  # class

        self.class_name = self.advance().value

        self.advance()  # {

        while self.peek().value in ("static", "field"):
            self.compile_class_var_dec()

        while self.peek().value in (
            "constructor",
            "function",
            "method"
        ):
            self.compile_subroutine()

    def compile_class_var_dec(self):

        kind = self.advance().value

        type_name = self.advance().value

        name = self.advance().value

        self.symbol_table.define(
            name,
            type_name,
            kind
        )

        self.advance()  # ;

    def compile_subroutine(self):

        self.symbol_table.start_subroutine()

        subroutine_type = self.advance().value

        self.advance()

        subroutine_name = self.advance().value

        self.advance()

        self.compile_parameter_list()

        self.advance()

        self.advance()

        while self.peek().value == "var":
            self.compile_var_dec()

        n_locals = self.symbol_table.var_count("var")

        self.vm.write_function(
            f"{self.class_name}.{subroutine_name}",
            n_locals
        )

        self.compile_statements()

        self.advance()

    def compile_parameter_list(self):

        while self.peek().value != ")":

            type_name = self.advance().value

            name = self.advance().value

            self.symbol_table.define(
                name,
                type_name,
                "arg"
            )

            if self.peek().value == ",":
                self.advance()

    def compile_var_dec(self):

        self.advance()

        type_name = self.advance().value

        name = self.advance().value

        self.symbol_table.define(
            name,
            type_name,
            "var"
        )

        self.advance()

    def compile_statements(self):

        while self.peek().value in (
            "let",
            "do",
            "while",
            "if",
            "return"
        ):

            token = self.peek().value

            if token == "do":
                self.compile_do()

            elif token == "return":
                self.compile_return()

            else:
                self.advance()

    def compile_do(self):

        self.advance()

        name = self.advance().value

        self.advance()

        subroutine = self.advance().value

        self.advance()

        self.advance()

        self.advance()

        self.vm.write_call(
            f"{name}.{subroutine}",
            0
        )

        self.vm.write_pop("temp", 0)

    def compile_return(self):

        self.advance()

        self.vm.write_push("constant", 0)

        self.vm.write_return()

        self.advance()