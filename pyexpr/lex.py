#coding: u8

from __future__ import print_function
import string


TOKEN_INV   = -1
TOKEN_NONE  = 0
TOKEN_NUM   = 1
TOKEN_PLUS  = 2
TOKEN_MINUS = 3
TOKEN_TIMES = 4
TOKEN_DIV   = 5
TOKEN_POW   = 6
TOKEN_LB    = 8
TOKEN_RB    = 9
TOKEN_VAR   = 10
TOKEN_COMMA = 11

TOKEN_NAMES = {
    TOKEN_INV   : 'TOKEN_INV',
    TOKEN_NONE  : 'TOKEN_NONE',
    TOKEN_NUM   : 'TOKEN_NUM',
    TOKEN_PLUS  : 'TOKEN_PLUS',
    TOKEN_MINUS : 'TOKEN_MINUS',
    TOKEN_TIMES : 'TOKEN_TIMES',
    TOKEN_DIV   : 'TOKEN_DIV',
    TOKEN_POW   : 'TOKEN_POW',
    TOKEN_LB    : 'TOKEN_LB',
    TOKEN_RB    : 'TOKEN_RB',
    TOKEN_VAR   : 'TOKEN_VAR',
    TOKEN_COMMA : 'TOKEN_COMMA',
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
        if ch in string.ascii_letters:
            start = self._offset
            self._offset += 1
            while self.cur in self.var_chars:
                self._offset += 1
            self._cur_token = (TOKEN_VAR, self._es[start:self._offset])
            return True
        if ch == '*':
            self._offset += 1
            if self.cur == '*':
                self._cur_token = (TOKEN_POW, '**')
                self._offset += 1
            else:
                self._cur_token = (TOKEN_TIMES, '*')
            return True
        self._cur_token = (TOKEN_INV, '')
        return False

if __name__ == '__main__':
    l = Lexer('(1+12.3)*pow(2, 3)')
    while l.next():
        ttype, tval = l.cur_token
        print(TOKEN_NAMES[ttype], tval)

