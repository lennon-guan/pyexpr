# A python expression evaluate library

## Installation

```
pip install pyexpr
```

## Usage

* Simple evaluation

```python
assert pyexpr.evaluate('1 + 2 * (3 - 4) **2') == 3
```

* With functions
```python
assert pyexpr.evaluate('1 + 2 * (3 - 4) ** sqrt(4)', builtins=dict(sqrt=math.sqrt)) == 3
```

* With variables
```python
assert pyexpr.evaluate('1 + 2 * (3 - 4) ** X', variables=dict(X=4)) == 3
```

You can find more examples in test.py
