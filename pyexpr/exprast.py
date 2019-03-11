#coding: u8

from __future__ import print_function
from __future__ import division
import ast


class Context(object):
    def __init__(self, variables=None, builtins=None):
        self.variables = variables or {}
        self.builtins = builtins or {}


class Node(object):
    pass


class Num(Node):
    def __init__(self, num):
        self._num = num

    def result(self, ctx):
        return self._num

    def display(self, indent):
        return '%s%s' % (indent, self._num)

class Str(Node):
    def __init__(self, s):
        self._s = ast.literal_eval(s)

    def result(self, ctx):
        return self._s

    def display(self, indent):
        return '%s%s' % (indent, self._s)

class Var(Node):
    def __init__(self, var):
        self._var = var

    def result(self, ctx):
        return ctx.variables.get(self._var, ctx.builtins.get(self._var))

    def display(self, indent):
        return '%s%s' % (indent, self._var)


class Negative(Node):
    @classmethod
    def new(cls, e):
        if isinstance(e, Num):
            return Num(-e.result(None))
        if isinstance(e, Minus):
            return Minus(e._n2, e._n1)
        return cls(e)

    def __init__(self, expr):
        self._expr = expr

    def result(self, ctx):
        return -self._expr.result(ctx)

    def display(self, indent):
        return '%s(negative\n%s\n%s),' % (indent, self._expr.display(indent + '  '), indent)


class _BinOp(Node):
    @classmethod
    def new(cls, n1, n2):
        if isinstance(n1, Num) and isinstance(n2, Num):
            return Num(cls.op(n1.result(None), n2.result(None)))
        return cls(n1, n2)

    def __init__(self, n1, n2):
        self._n1 = n1
        self._n2 = n2

    def result(self, ctx):
        return self.op(self._n1.result(ctx), self._n2.result(ctx))

    def display(self, indent):
        return '%s%s(\n%s\n%s\n%s),' % (
            indent,
            type(self).__name__,
            self._n1.display(indent + '  '),
            self._n2.display(indent + '  '),
            indent,
        )
        

class Plus(_BinOp):
    op = classmethod(lambda cls, a, b: a + b)


class Minus(_BinOp):
    op = classmethod(lambda cls, a, b: a - b)


class Times(_BinOp):
    op = classmethod(lambda cls, a, b: a * b)


class Division(_BinOp):
    op = classmethod(lambda cls, a, b: a / b)


class Pow(_BinOp):
    op = classmethod(lambda cls, a, b: a ** b)

class And(_BinOp):
    op = classmethod(lambda cls, a, b: a and b)

class Or(_BinOp):
    op = classmethod(lambda cls, a, b: a or b)

class Equal(_BinOp):
    op = classmethod(lambda cls, a, b: a == b)

class NotEqual(_BinOp):
    op = classmethod(lambda cls, a, b: a != b)

class GreaterThan(_BinOp):
    op = classmethod(lambda cls, a, b: a > b)

class GreaterEqual(_BinOp):
    op = classmethod(lambda cls, a, b: a >= b)

class LessThan(_BinOp):
    op = classmethod(lambda cls, a, b: a < b)

class LessEqual(_BinOp):
    op = classmethod(lambda cls, a, b: a <= b)

class Not(Node):
    def __init__(self, expr):
        self._expr = expr

    def result(self, ctx):
        return not self._expr.result(ctx)

    def display(self, indent):
        return '%s(not\n%s\n%s),' % (indent, self._expr.display(indent + '  '), indent)
        
 
class ValueList(Node):
    def __init__(self, *vs):
        self._vs = vs

    def result(self, ctx):
        return [v.result(ctx) for v in self._vs]

    def display(self, indent):
        return '\n'.join(v.display(indent) for v in self._vs)
        

class FuncCall(Node):
    def __init__(self, fn, vs):
        self._fn = fn
        self._vs = vs

    def result(self, ctx):
        return self._fn.result(ctx)(*self._vs.result(ctx))

    def display(self, indent):
        return '%s%s(\n%s\n%s)' % (
            indent,
            self._fn._var,
            self._vs.display(indent + '  '),
            indent,
        )
    
if __name__ == '__main__':
    expr = Plus(
        FuncCall(
            Var('abs'),
            ValueList(Num(-2)),
        ),
        Var('age'),
    )
    ctx = Context()
    ctx.variables['age'] = 13
    ctx.builtins['abs'] = abs
    print(expr.result(ctx))
