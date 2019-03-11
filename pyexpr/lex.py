#coding: u8

from __future__ import print_function
import string


TOKEN_INV   = -1
TOKEN_NONE  = 0
TOKEN_NUM   = 1
TOKEN_STR   = 2
TOKEN_PLUS  = 3
TOKEN_MINUS = 4
TOKEN_TIMES = 5
TOKEN_DIV   = 6
TOKEN_POW   = 7
TOKEN_LB    = 9
TOKEN_RB    = 10
TOKEN_VAR   = 11
TOKEN_COMMA = 12
TOKEN_AND   = 13
TOKEN_OR    = 14
TOKEN_NOT   = 15
TOKEN_EQ    = 16
TOKEN_NE    = 17
TOKEN_GT    = 18
TOKEN_GE    = 19
TOKEN_LT    = 20
TOKEN_LE    = 21

TOKEN_NAMES = {
    TOKEN_INV   : 'TOKEN_INV',
    TOKEN_NONE  : 'TOKEN_NONE',
    TOKEN_NUM   : 'TOKEN_NUM',
    TOKEN_STR   : 'TOKEN_STR',
    TOKEN_PLUS  : 'TOKEN_PLUS',
    TOKEN_MINUS : 'TOKEN_MINUS',
    TOKEN_TIMES : 'TOKEN_TIMES',
    TOKEN_DIV   : 'TOKEN_DIV',
    TOKEN_POW   : 'TOKEN_POW',
    TOKEN_LB    : 'TOKEN_LB',
    TOKEN_RB    : 'TOKEN_RB',
    TOKEN_VAR   : 'TOKEN_VAR',
    TOKEN_COMMA : 'TOKEN_COMMA',
    TOKEN_AND   : 'TOKEN_AND',
    TOKEN_OR    : 'TOKEN_OR',
    TOKEN_NOT   : 'TOKEN_NOT',
    TOKEN_EQ    : 'TOKEN_EQ',
    TOKEN_NE    : 'TOKEN_NE',
    TOKEN_GT    : 'TOKEN_GT',
    TOKEN_GE    : 'TOKEN_GE',
    TOKEN_LT    : 'TOKEN_LT',
    TOKEN_LE    : 'TOKEN_LE',
}

_SPACES = (' ', '\t')
_END_CHAR = chr(255)

class Lexer(object):

    fixed_char_token = {
        '+': TOKEN_PLUS,
        '-': TOKEN_MINUS,
        '/': TOKEN_DIV,
        '(': TOKEN_LB,
        ')': TOKEN_RB,
        ',': TOKEN_COMMA,
    }
    var_chars = string.ascii_letters + string.digits + '_$'

    def __init__(self, expr_str):
        self._es = expr_str
        self._offset = 0
        self._len = len(expr_str)
        self._cur_token = (TOKEN_NONE, None)

    def _skip_spaces(self):
        while self._offset < self._len and self._es[self._offset] in _SPACES:
            self._offset += 1

    @property
    def eof(self):
        return self._offset >= self._len

    @property
    def cur(self):
        return _END_CHAR if self._offset >= self._len else self._es[self._offset]

    @property
    def cur_token(self):
        return self._cur_token

    @property
    def cur_ttype(self):
        return self._cur_token[0]

    @property
    def cur_tval(self):
        return self._cur_token[1]

    @property
    def offset(self):
        return self._offset

    @property
    def rest_expr(self):
        return self._es[self._offset:]

    def next(self):
        self._skip_spaces()
        ch = self.cur
        if ch == _END_CHAR:
            self._cur_token = (TOKEN_NONE, None)
            return False
        if ch in self.fixed_char_token:
            self._offset += 1
            self._cur_token = (self.fixed_char_token[ch], ch)
            return True
        if ch.isdigit():
            start = self._offset
            self._offset += 1
            ntype = int
            while self.cur.isdigit():
                self._offset += 1
            if self.cur == '.':
                self._offset += 1
                while self.cur.isdigit():
                    self._offset += 1
                ntype = float
            self._cur_token = (TOKEN_NUM, ntype(self._es[start:self._offset]))
            return True
        if ch == '"':
            start = self._offset
            while True:
                self._offset += 1
                ch = self.cur
                if ch == '"':
                    self._offset += 1
                    break
                if ch == '\\':
                    self._offset += 1
            self._cur_token = (TOKEN_STR, self._es[start:self._offset])
            return True
        if ch in string.ascii_letters:
            start = self._offset
            self._offset += 1
            while self.cur in self.var_chars:
                self._offset += 1
            token_literal = self._es[start:self._offset]
            if token_literal == 'and':
                self._cur_token = (TOKEN_AND, token_literal)
            elif token_literal == 'or':
                self._cur_token = (TOKEN_OR, token_literal)
            elif token_literal == 'not':
                self._cur_token = (TOKEN_NOT, token_literal)
            else:
                self._cur_token = (TOKEN_VAR, token_literal)
            return True
        if ch == '*':
            self._offset += 1
            if self.cur == '*':
                self._cur_token = (TOKEN_POW, '**')
                self._offset += 1
            else:
                self._cur_token = (TOKEN_TIMES, '*')
            return True
        if ch == '=':
            self._offset += 1
            if self.cur == '=':
                self._cur_token = (TOKEN_EQ, '==')
                self._offset += 1
                return
        if ch == '!':
            self._offset += 1
            if self.cur == '=':
                self._cur_token = (TOKEN_NE, '!=')
                self._offset += 1
                return
        if ch == '>':
            self._offset += 1
            if self.cur == '=':
                self._cur_token = (TOKEN_GE, '>=')
                self._offset += 1
            else:
                self._cur_token = (TOKEN_GT, '>')
            return
        if ch == '<':
            self._offset += 1
            if self.cur == '=':
                self._cur_token = (TOKEN_LE, '<=')
                self._offset += 1
            else:
                self._cur_token = (TOKEN_LT, '<')
            return
        self._cur_token = (TOKEN_INV, '')
        return False

if __name__ == '__main__':
    l = Lexer('(1+12.3)*pow(2, 3)')
    while l.next():
        ttype, tval = l.cur_token
        print(TOKEN_NAMES[ttype], tval)

