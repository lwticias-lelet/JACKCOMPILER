# Analisador Léxico da Linguagem Jack

## Aluna

Letícia Delfino
Curso: Engenharia de Computação
Disciplina: Compiladores

## Linguagem utilizada

Python

## Descrição

Este projeto tem como objetivo implementar um analisador léxico para a linguagem Jack, conforme proposto na atividade prática da disciplina.

O programa lê arquivos `.jack`, remove comentários e espaços desnecessários e identifica os tokens da linguagem, gerando como saída um arquivo em formato XML.

## Requisitos implementados

### Reconhecimento de tokens

O analisador reconhece os seguintes tipos:

* keyword (palavras reservadas)
* symbol (símbolos da linguagem)
* integerConstant (números inteiros)
* stringConstant (strings entre aspas)
* identifier (nomes de variáveis, funções, etc.)

### Tratamento de ruído

* ignora espaços em branco
* ignora tabs e quebras de linha
* remove comentários de linha (//)
* remove comentários de bloco (/* */)

### Saída XML

* gera arquivo no padrão do nand2tetris
* tokens no formato: `<keyword> class </keyword>`
* caracteres especiais tratados:

  * `<` → `&lt;`
  * `>` → `&gt;`
  * `&` → `&amp;`
* arquivo envolto por `<tokens>` e `</tokens>`
* não possui token EOF

## Estrutura do projeto

jack_lexer/
main.py
tokenizer.py
utils.py
input/
output/

## Como executar

1. Colocar os arquivos `.jack` dentro da pasta `input`
2. Abrir o terminal na pasta do projeto
3. Executar:

python main.py ( lemnre-se de estar dentro da pasta jack_lexer)

4. Os arquivos `.xml` serão gerados na pasta `output`

## Testes

Para testar o funcionamento, foram utilizados arquivos `.jack` simples e também os exemplos do nand2tetris:

* Main.jack
* Square.jack
* SquareGame.jack
