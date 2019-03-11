from .lex import Lexer
from .exprast import Context
from .parser import parse


__all__ = ['parse_expr', 'evaluate', 'Context']

def parse_expr(expr):
    l = Lexer(expr)
    return parse(l)

def evaluate(expr, ctx=None, variables=None, builtins=None):
    e = parse_expr(expr)
    if ctx is None:
        ctx = Context(variables=variables, builtins=builtins)
    return e.result(ctx)

def simple_eval(expr, **vars):
    return evaluate(expr, variables=vars)
