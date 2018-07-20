#coding: u8

from __future__ import print_function

import math
import pyexpr


builtins={
    'abs': abs,
    'sqrt': math.sqrt,
}


def assert_eval(expr, expected, **variables):
    e = pyexpr.parse_expr(expr)
    r = e.result(pyexpr.Context(variables=variables, builtins=builtins))
    if r != expected:
        print(e.display(''))
        raise AssertionError('%s return %s, expected %s' % (expr, r, expected))

# 测试数值计算
assert_eval('1 + 2 * 3', 7)
assert_eval('1 + -2 * 3', -5)
assert_eval('2 * (3 * 5) + 12', 42)
assert_eval('1 + -(3*5) + 3', -11)
assert_eval('1 - 2 + 3', 2)
assert_eval('10 / 2 * 3', 15)
assert_eval('1 / 2', 0.5)
assert_eval('5/2**3', 0.625)
assert_eval('2 ** 2 ** 3', 256)
assert_eval('2 ** -1', 0.5)
assert_eval('2 ** -(3 - 2)', 0.5)
assert_eval('9 ** 0.5', 3)

# 测试带函数的计算
assert_eval('5 + -abs(4-8)**2', -11)
assert_eval('sqrt(9)', 3)
assert_eval('-(5-sqrt(4))', -3)

# 测试带变量的计算
assert_eval('a + 1', 5, a=4)
assert_eval('abs(a)', 10, a=10)
assert_eval('abs(a)', 10, a=-10)
assert_eval('abs(a) + b', 10, a=-3, b=7)

print('All test cases passed!')
