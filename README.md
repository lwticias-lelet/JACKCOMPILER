# 🧠 Jack Parser — Analisador Sintático (Nand2Tetris)

## 📌 Descrição

Este projeto implementa um **analisador sintático (parser)** para a linguagem **Jack**, conforme especificado no projeto **Nand2Tetris (Unidade 1)**.

O parser consome os tokens gerados por um analisador léxico previamente desenvolvido e produz como saída um arquivo **XML** representando a árvore sintática do programa, compatível com o validador oficial do curso.

A implementação segue a abordagem de **Recursive Descent Parsing**, onde cada regra da gramática é representada por uma função.

---

## 🎯 Objetivos

* Implementar a gramática completa da linguagem Jack
* Reutilizar o tokenizer desenvolvido anteriormente
* Validar a estrutura sintática dos programas
* Gerar saída XML conforme padrão oficial do Nand2Tetris

---

## 🏗️ Estrutura do Projeto

```
jack_lexer/
│
├── input/              # Arquivos .jack de entrada
├── output/             # Arquivos XML gerados
├── expected/           # Arquivos XML esperados (referência)
│
├── tokenizer.py        # Analisador léxico
├── parser.py           # Analisador sintático (parser)
├── main.py             # Script principal
└── README.md
```

---

## ⚙️ Tecnologias Utilizadas

* Python 3
* Programação orientada a objetos
* Recursive Descent Parsing

---

## 🔍 Funcionamento

### 1. Tokenizer (Analisador Léxico)

O `tokenizer.py` é responsável por:

* Remover comentários e espaços em branco
* Identificar tokens da linguagem:

  * `keyword`
  * `symbol`
  * `identifier`
  * `integerConstant`
  * `stringConstant`

Exemplo:

```jack
let x = 10;
```

Gera:

```xml
<keyword> let </keyword>
<identifier> x </identifier>
<symbol> = </symbol>
<integerConstant> 10 </integerConstant>
<symbol> ; </symbol>
```

---

### 2. Parser (Analisador Sintático)

O `parser.py` implementa a análise sintática baseada na gramática Jack.

Cada regra da gramática possui um método correspondente, por exemplo:

* `compile_class()`
* `compile_subroutine()`
* `compile_statements()`
* `compile_expression()`
* `compile_term()`

O parser utiliza métodos auxiliares:

* `peek()` → visualiza o próximo token
* `advance()` → consome o token atual

---

### 3. Geração de XML

A saída é gerada no formato XML exigido pelo projeto:

```xml
<class>
  <keyword> class </keyword>
  <identifier> Main </identifier>
  <symbol> { </symbol>
  ...
</class>
```

Características:

* Cada não-terminal da gramática é representado como uma tag XML
* Indentação correta para legibilidade
* Escape de caracteres especiais:

  * `<` → `&lt;`
  * `>` → `&gt;`
  * `&` → `&amp;`
  * `"` → `&quot;`

---

## ▶️ Como Executar

### 1. Navegue até a pasta do projeto

```bash
cd jack_lexer
```

### 2. Execute o programa

```bash
python main.py
```

---

## 📂 Saída Gerada

Após a execução, serão criados arquivos XML na pasta `output/`:

```
output/
├── MainP.xml
├── SquareP.xml
└── SquareGameP.xml
```

---

## ✅ Validação

A validação foi realizada comparando os arquivos gerados com os arquivos oficiais do Nand2Tetris.

### Comando utilizado (PowerShell):

```powershell
Compare-Object (Get-Content output\MainP.xml) (Get-Content expected\MainP.xml)
Compare-Object (Get-Content output\SquareP.xml) (Get-Content expected\SquareP.xml)
Compare-Object (Get-Content output\SquareGameP.xml) (Get-Content expected\SquareGameP.xml)
```

### ✔ Resultado esperado:

* Nenhuma saída no terminal
* Isso indica que os arquivos são **idênticos**

---

## 📌 Requisitos Atendidos

✔ Implementação completa da gramática Jack
✔ Uso de Recursive Descent Parsing
✔ Integração com tokenizer da atividade anterior
✔ Geração correta de XML
✔ Escape de caracteres especiais
✔ Validação com arquivos oficiais

---

## 📚 Conclusão

O analisador sintático foi implementado com sucesso, sendo capaz de:

* Interpretar corretamente programas escritos em Jack
* Validar sua estrutura sintática
* Gerar uma representação XML compatível com o padrão oficial

Este projeto conclui a **Unidade 1 do curso Nand2Tetris**.

---

## 👩‍💻 Autora

Letícia Delfino
Engenharia da Computação

---
