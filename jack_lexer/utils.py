def convert_symbol(s):
    if s == "<":
        return "&lt;"
    if s == ">":
        return "&gt;"
    if s == "&":
        return "&amp;"
    return s

def write_xml(tokens, path):
    with open(path, "w") as f:
        f.write("<tokens>\n")

        for t in tokens:
            val = t.value
            if t.type == "symbol":
                val = convert_symbol(val)

            f.write(f"<{t.type}> {val} </{t.type}>\n")

        f.write("</tokens>\n")