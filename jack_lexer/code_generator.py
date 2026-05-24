from vm_writer import VMWriter
import os


class CodeGenerator:

    def __init__(self, parser, output_path):

        self.parser = parser
        self.output_path = output_path

        self.vm = VMWriter(output_path)

        self.class_name = os.path.basename(output_path).replace(".vm", "")

    def compile(self):

        # função principal
        self.vm.write_function(f"{self.class_name}.main", 0)

        # exemplo de operações reais
        self.vm.write_push("constant", 10)
        self.vm.write_push("constant", 20)

        self.vm.write_arithmetic("add")

        self.vm.write_pop("temp", 0)

        # loop infinito para não encerrar imediatamente
        self.vm.write_label("END")
        self.vm.write_goto("END")

        self.vm.close()