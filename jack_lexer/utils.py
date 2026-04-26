def escape_xml(s):
    return (
        s.replace("&", "&amp;")
         .replace("<", "&lt;")
         .replace(">", "&gt;")
         .replace('"', "&quot;")
    )


def write_xml(tokens, path):
    with open(path, "w") as f:
        f.write("<tokens>\n")

        for t in tokens:
            val = escape_xml(t.value)
            f.write(f"  <{t.type}> {val} </{t.type}>\n")

        f.write("</tokens>\n")