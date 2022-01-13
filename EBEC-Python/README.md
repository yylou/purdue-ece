# Python Programming

## Math Operators
```Python
  " +  "    Addition
  " -  "    Subtraction
  " *  "    Multiplication
  " /  "    Float Division
  " ** "    Exponentiation
  " // "    Floor Division
  " %  "    Modulus (Remainder)
```

## Operator Precedence
```Python
  (1)  Parentheses      " () "
  (2)  Exponentiation   " ** "
  (3)  Mul / Div / Mod  " *, /, //, %"
  (4)  Add / Sub        " +, - "
```

## Exponential Notation Format
```Python
>>> format(123456.789, 'e')         # '1.234568e+05'
>>> format(123456.789, '.2e')       # '1.23e+05'
>>> format(0.00000123456, '.4e')    # '1.2346e-06'
>>> format(0.00000123456, '.4E')    # '1.2346E-06'
```

## Complex Numbers
```Python
>>> complex(10,   20)       # (10  + 20j)
>>> complex(2.5, -18.2)     # (2.5 - 18.2j)
```

<br />

## Classes, Instances, and Attributes
For the purpose of writing code, **a class is a data structure with attributes.**  
To endow instances with behaviors, **a class can be provided with methods.**
* A method that is invoked on an instance is sometimes called an **instance method**.
* You can also invoke a method directly on a class, in which case it is called a **class method or a static method**.
* Attributes that take data values on a **per-instance** basis are frequently referred to as **instance variables**.
* Attributes that take on values on a **per-class** basis are called **class attributes or static attributes or class variables**.

## Pre-Defined Attributes for a Class
* \_\_name__    : string name of the class
* \_\_doc__     : documentation string for the class
* \_\_bases__   : tuple of parent classes of the class
* \_\_dict__    : dictionary whose keys are the names of the class variables and the methods of the class and whose values are the corresponding bindings
* \_\_module__  : module in which the class is defined

## Pre-Defined Attributes for an Instance
* \_\_class__   : string name of the class from which the instance was constructed
* \_\_dict__    : dictionary whose keys are the names of the instance variables
```Python
# As an alternative to invoking dict on a class name
"""
Returns a list of all the attribute names, for variables and for methods, for the class
(both directly defined for the class and inherited from a class’s superclasses).
"""
dir(MyClass)        # type: list
MyClass.__dict__    # type: mappingproxy
```

```Python
class Person:
    "A very simple class"
    def __init__(self, name, yy):
        self.name = name
        self.age = yy

# Test code
a_person = Person("Zaphod", 114)
print(a_person.name)        # Zaphod
print(a_person.age)         # 114

# Class Attributes
print(Person.__name__)      # Person
print(Person.__doc__)       # A very simple class
print(Person.__module__)    # main
print(Person.__bases__)     # ()
print(Person.__dict__)      # {'__module__':    '__main__',
                            #  '__doc__':       'A very simple class', 
                            #  '__init__':      <function Person.__init__ at 0x107efd940>,
                            #  '__dict__':      <attribute '__dict__' of 'Person' objects>,
                            #  '__weakref__':   <attribute '__weakref__' of 'Person' objects>}

print(dir(Person))          # ['__class__', '__init__', '__dict__', '__dir__', '__doc__',
                            #  '__eq__', '__ge__', '__gt__', '__le__', '__lt__', '__ne__', 
                            #  '__format__', '__sizeof__', '__str__', '__module__', '__getattribute__', '__new__', 
                            #  '__reduce__', '__reduce_ex__', '__repr__', '__delattr__', '__setattr__',
                            #  '__hash__', '__init_subclass__', '__subclasshook__', '__weakref__']

# Instance Attributes
print(a_person.__class__)   # __main__.Person
print(a_person.__dict__)    # {'name': 'Zaphod', 'age': 114}

```

## Encapsulation, Inheritance, and Polymorphism
* **Hiding or controlling access** to the implementation-related attributes and the methods of a class is called encapsulation.
* **Inheritance** in object-oriented code allows a subclass to inherit some or all of the attributes and methods of its superclass(es).
* **Polymorphism** basically means that a given category of objects can exhibit multiple identities at the same time
* **Polymorphism** in a nutshell allows us to manipulate instances belonging to the different classes of a hierarchy through a common interface defined for the root class.

## Function Objects vs. Callables
* Function object can only be created with a def statement.
* Callable is any object that can be called like a function.
* An instance object can also be called directly; what that yields depends on whether or not the underlying class provides a definition for the **system-supplied call () method.**
```Python
import random
random.seed(0)

class X:
    def __init__(self, arr) : self.arr = arr
    def get_num(self, i): return self.arr[i]
    def __call__(self): return self.arr

xobj = X(random.sample(range(1,10), 5))
print(xobj.get_num(2))  # 1
print(xobj())           # [7, 9, 1, 3, 5]
```