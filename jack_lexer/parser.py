class Parser:

    def __init__(self, tokens):

        self.tokens = tokens
        self.index = 0

    def current(self):

        if self.index < len(self.tokens):
            return self.tokens[self.index]

        return None

    def advance(self):
        self.index += 1

    def parse(self):

        xml = "<class>\n"

        while self.current():

            token = self.current()

            xml += f"<{token.type}> {token.value} </{token.type}>\n"

            self.advance()

        xml += "</class>\n"

        return xml