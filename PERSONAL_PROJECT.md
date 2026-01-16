# Personal Project 1

While wrapping my head around the BOOT.DEV static site generator
project, I heard the voices of ancestors calling. They were using
strange words like Yacc, and Lex, and Backus-Naur Form.

Then they said a word I recognized: grammar!

## Project Goals:

1. Choose a lexer and parser toolkit
2. Find or (stretch goal) create a markdown grammar
3. Create a parser and from there an AST
4. Render a DIV from the AST
5. Introduce templating with Jinja2
6. Render whole HTML pages with markdown elements in a DIV

### Variations:

1. Golang instead of Python (perhaps for capstone)
2. Plugins (to demonstrate architectural thinking)

## Details

Grammar toolkit candidate: [Lark](https://github.com/lark-parser/lark)

Search the `grammar` topic on GitHub (lang: Python):

```
https://github.com/topics/grammar?l=python
```

Template languages:

- [Genshi](https://genshi.edgewall.org/)
- [Jinja](https://jinja.palletsprojects.com/en/stable/)
