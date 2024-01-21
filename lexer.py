import re

class Token:
    def __init__(self, token_type, grammar=None):
        self.name = token_type
        self.grammar = re.compile(grammar) if grammar else None

    def match(self, string):
        if self.grammar:
            match = self.grammar.fullmatch(string)
            if match:
                return self.name
        return "ERROR"

class Lexer:
    def __init__(self, tokens_rules):
        self.text = ""
        self.tokens = tokens_rules

    def input(self, text):
        self.text = text

    def tokenize(self):
        self.text = self.text.split()
        token_list = []
        for word in self.text:
            token_type = "ERROR"
            for token in self.tokens:
                token_type = token.match(word)
                if token_type != "ERROR":
                    break
            token_list.append((word, token_type))
        return token_list
