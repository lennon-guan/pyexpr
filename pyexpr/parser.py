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
            lexer._len,
            lexer._offset,
        )
        super(ParseError, self).__init__(msg)

def _parse_valuelist(lexer):
    vs = []
    if lexer.cur_ttype == TOKEN_RB:
        return ValueList()
    vs.append(_parse_logic_expr(lexer))
    while lexer.cur_ttype == TOKEN_COMMA:
        lexer.next()
        vs.append(_parse_logic_expr(lexer))
    if lexer.cur_ttype != TOKEN_RB:
        raise ParseError(lexer)
    return ValueList(*vs)

def _parse_factor(lexer):
    ttype, tval = lexer.cur_token
    if ttype == TOKEN_LB:
        if not lexer.next():
            raise ParseError(lexer)
        factor = _parse_logic_expr(lexer)
        if lexer.cur_ttype != TOKEN_RB:
            raise ParseError(lexer)
        lexer.next()
    elif ttype == TOKEN_NUM:
        factor = Num(tval)
        lexer.next()
    elif ttype == TOKEN_STR:
        factor = Str(tval)
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


_cmp_ops = {
    TOKEN_EQ: Equal,
    TOKEN_NE: NotEqual,
    TOKEN_GT: GreaterThan,
    TOKEN_GE: GreaterEqual,
    TOKEN_LT: LessThan,
    TOKEN_LE: LessEqual,
}

def _parse_cmp_expr(lexer):
    if lexer.cur_ttype == TOKEN_NOT:
        if not lexer.next():
            raise ParseError(lexer)
        return Not(_parse_cmp_expr(lexer))
    expr = _parse_expr(lexer)
    ttype, _ = lexer.cur_token
    if ttype not in _cmp_ops:
        return expr
    if not lexer.next():
        raise ParseError(lexer)
    n1 = expr
    n2 = _parse_expr(lexer)
    return _cmp_ops[ttype](n1, n2)

_logic_ops = {
    TOKEN_AND: And,
    TOKEN_OR: Or,
}

def _parse_logic_expr(lexer):
    expr = _parse_cmp_expr(lexer)
    ttype, _ = lexer.cur_token
    if ttype not in _logic_ops:
        return expr
    if not lexer.next():
        raise ParseError(lexer)
    n1 = expr
    n2 = _parse_cmp_expr(lexer)
    return _logic_ops[ttype](n1, n2)

def parse(lexer):
    if not lexer.next():
        return None
    r = _parse_logic_expr(lexer)
    if lexer.cur_ttype != TOKEN_NONE:
        raise ParseError(lexer)
    return r

if __name__ == '__main__':
    ctx = Context(variables=dict(v1=10))
    print(parse(Lexer('v1 + 2 * (3 - 4) - 5')).result(ctx))
