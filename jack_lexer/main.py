import os
import sys

from tokenizer import JackTokenizer
from parser import Parser
from code_generator import CodeGenerator


def compile_file(path):
    with open(path, "r") as f:
        code = f.read()

    # tokenizer
    tokenizer = JackTokenizer(code)
    tokens = tokenizer.get_tokens()

    # parser
    parser = Parser(tokens)

    # nome do arquivo vm
    vm_path = path.replace(".jack", ".vm")

    # code generator
    generator = CodeGenerator(parser, vm_path)

    generator.compile()

    print(f"{os.path.basename(path)} compilado ✔")


def compile_directory(directory):
    for file in os.listdir(directory):
        if file.endswith(".jack"):
            full_path = os.path.join(directory, file)
            compile_file(full_path)


if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("Uso:")
        print("python main.py input/Square")
        sys.exit(1)

    target = sys.argv[1]

    if os.path.isdir(target):
        compile_directory(target)

    elif target.endswith(".jack"):
        compile_file(target)

    else:
        print("Entrada inválida")