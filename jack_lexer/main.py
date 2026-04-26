import os
from tokenizer import JackTokenizer
from parser import Parser

input_dir = "input"
output_dir = "output"

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

for file in sorted(os.listdir(input_dir)):
    if file.endswith(".jack"):
        path = os.path.join(input_dir, file)

        with open(path, "r") as f:
            code = f.read()

        tokenizer = JackTokenizer(code)
        tokens = tokenizer.get_tokens()

        parser = Parser(tokens)
        xml = parser.parse()

        out_name = file.replace(".jack", "P.xml")
        out_path = os.path.join(output_dir, out_name)

        with open(out_path, "w") as f:
            f.write(xml.strip() + "\n")

        print(f"{file} processado com sucesso ✔")