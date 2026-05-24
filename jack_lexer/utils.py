def convert_symbol(s):

    if s == "<":
        return "&lt;"

    if s == ">":
        return "&gt;"

    if s == "&":
        return "&amp;"

    if s == '"':
        return "&quot;"

    return s