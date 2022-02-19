# Python Programming
* ### [Menu](./README.md)
* ### Basic
    * [Math Operators](#p1)
    * [Operator Precedence](#p2)
    * [Exponential Notation Format](#p3)
    * [Complex Numbers](#p4)
    * [Function Objects vs. Callables](#p5)

<br />

## Math Operators           <a name="p1"></a>
```Python
  " +  "    Addition
  " -  "    Subtraction
  " *  "    Multiplication
  " /  "    Float Division
  " ** "    Exponentiation
  " // "    Floor Division
  " %  "    Modulus (Remainder)
```

## Operator Precedence           <a name="p2"></a>
```Python
  (1)  Parentheses      " () "
  (2)  Exponentiation   " ** "
  (3)  Mul / Div / Mod  " *, /, //, %"
  (4)  Add / Sub        " +, - "
```

## Exponential Notation Format          <a name="p3"></a>
```Python
>>> format(123456.789,    'e')      # '1.234568e+05'
>>> format(123456.789,    '.2e')    # '1.23e+05'
>>> format(0.00000123456, '.4e')    # '1.2346e-06'
>>> format(0.00000123456, '.4E')    # '1.2346E-06'
```

## Complex Numbers          <a name="p4"></a>
```Python
>>> complex(10,   20)       # (10  + 20j)
>>> complex(2.5, -18.2)     # (2.5 - 18.2j)
```

## Function Objects vs. Callables           <a name="p5"></a>
* Function object can only be created with a def statement.
* Callable is any object that can be called like a function.
* An instance object can also be called directly; what that yields depends on whether or not the underlying class provides a definition for the **system-supplied call () method.**

```Python
import random
random.seed(0)

class X:
    def __init__(self, arr): self.arr = arr
    def __call__(self): return self.arr
    def get_num(self, i): return self.arr[i]

xobj = X(random.sample(range(1,10), 5))
print(xobj.get_num(2))  # 1
print(xobj())           # [7, 9, 1, 3, 5]