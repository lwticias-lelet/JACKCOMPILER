import os

from tokenizer import JackTokenizer
from compilation_engine import CompilationEngine


INPUT_DIR = "input"
OUTPUT_DIR = "output"

os.makedirs(OUTPUT_DIR, exist_ok=True)


for file_name in os.listdir(INPUT_DIR):

    if file_name.endswith(".jack"):

        input_path = os.path.join(
            INPUT_DIR,
            file_name
        )

        with open(input_path, "r") as f:
            code = f.read()

        tokenizer = JackTokenizer(code)

        engine = CompilationEngine(
            tokenizer.get_tokens()
        )

        engine.compile_class()

        output_name = file_name.replace(
            ".jack",
            ".vm"
        )

        output_path = os.path.join(
            OUTPUT_DIR,
            output_name
        )

        engine.vm.save(output_path)

        print(f"{file_name} compilado ✔")