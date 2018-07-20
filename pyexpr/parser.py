#coding: u8

from __future__ import print_function
from __future__ import division

from .lex import *
from .exprast import *


class ParseError(Exception):
    def __init__(self, lexer):
        msg = '%s, ttype: %s, len %d offset %d' % (
            lexer._es,
            TOKEN_NAMES[lexer.cur_ttype],
            lexer._offset,
            lexer._len,
        )
        super(ParseError, self).__init__(msg)

def _parse_valuelist(lexer):
    vs = []
    vs.append(_parse_expr(lexer))
    while lexer.cur_ttype == TOKEN_COMMA:
        print(vs)
        lexer.next()
        vs.append(_parse_expr(lexer))
    if lexer.cur_ttype != TOKEN_RB:
        raise ParseError(lexer)
    return ValueList(*vs)

def _parse_factor(lexer):
    ttype, tval = lexer.cur_token
    if ttype == TOKEN_LB:
        if not lexer.next():
            raise ParseError(lexer)
        factor = _parse_expr(lexer)
        if lexer.cur_ttype != TOKEN_RB:
            raise ParseError(lexer)
        lexer.next()
    elif ttype == TOKEN_NUM:
        factor = Num(tval)
        lexer.next()
    elif ttype == TOKEN_VAR:
        factor = Var(tval)
        lexer.next()
        if lexer.cur_ttype == TOKEN_LB:
            lexer.next()
            vs = _parse_valuelist(lexer)
            factor = FuncCall(factor, vs)
            lexer.next()
    else:
        raise ParseError(lexer)
    return factor

def _parse_atom(lexer):
    if lexer.cur_ttype == TOKEN_MINUS:
        lexer.next()
        return Negative.new(_parse_atom(lexer))
    atom = _parse_factor(lexer)
    ttype, _ = lexer.cur_token
    if ttype == TOKEN_POW:
        if not lexer.next():
            raise ParseError(lexer)
        n1 = atom
        n2 = _parse_atom(lexer)
        atom = Pow(n1, n2)
        ttype, _ = lexer.cur_token
    return atom
    
def _parse_item(lexer):
    item = _parse_atom(lexer)
    ttype, _ = lexer.cur_token
    while ttype in (TOKEN_TIMES, TOKEN_DIV):
        if not lexer.next():
            raise ParseError(lexer)
        n1 = item
        n2 = _parse_atom(lexer)
        item = Times.new(n1, n2) if ttype == TOKEN_TIMES \
                else Division.new(n1, n2)
        ttype, _ = lexer.cur_token
    return item
    

def _parse_expr(lexer):
    expr = _parse_item(lexer)
    ttype, _ = lexer.cur_token
    while ttype in (TOKEN_PLUS, TOKEN_MINUS):
        if not lexer.next():
            raise ParseError(lexer)
        n1 = expr
        n2 = _parse_item(lexer)
        expr = Plus.new(n1, n2) if ttype == TOKEN_PLUS \
                else Minus.new(n1, n2)
        ttype, _ = lexer.cur_token
    return expr


def parse(lexer):
    if not lexer.next():
        return None
    r = _parse_expr(lexer)
    if lexer.cur_ttype != TOKEN_NONE:
        raise ParseError(lexer)
    return r

if __name__ == '__main__':
    ctx = Context(variables=dict(v1=10))
    print(parse(Lexer('v1 + 2 * (3 - 4) - 5')).result(ctx))
