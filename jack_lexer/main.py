import os
from tokenizer import JackTokenizer
from utils import write_xml

input_dir = "input"
output_dir = "output"

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

for file in os.listdir(input_dir):
    if file.endswith(".jack"):
        path = os.path.join(input_dir, file)

        with open(path, "r") as f:
            code = f.read()

        tokenizer = JackTokenizer(code)
        tokens = tokenizer.get_tokens()

        out_name = file.replace(".jack", ".xml")
        out_path = os.path.join(output_dir, out_name)

        write_xml(tokens, out_path)