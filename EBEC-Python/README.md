# Python Programming

### <u>Math Operators</u>
```Python
  " +  "    Addition
  " -  "    Subtraction
  " *  "    Multiplication
  " /  "    Float Division
  " ** "    Exponentiation
  " // "    Floor Division
  " %  "    Modulus (Remainder)
```

### <u>Operator Precedence</u>
```Python
  (1)  Parentheses      " () "
  (2)  Exponentiation   " ** "
  (3)  Mul / Div / Mod  " *, /, //, %"
  (4)  Add / Sub        " +, - "
```

### <u>Exponential Notation Format</u>
```Python
>>> format(123456.789, 'e')         # '1.234568e+05'
>>> format(123456.789, '.2e')       # '1.23e+05'
>>> format(0.00000123456, '.4e')    # '1.2346e-06'
>>> format(0.00000123456, '.4E')    # '1.2346E-06'
```

### <u>Complex Numbers</u>
```Python
>>> complex(10,   20)       # (10  + 20j)
>>> complex(2.5, -18.2)     # (2.5 - 18.2j)
```

### <u>Classes, Instances, and Attributes</u>
* For the purpose of writing code, a class is a data structure with attributes.
* To endow instances with behaviors, a class can be provided with methods.

<br />

* A method that is invoked on an instance is sometimes called an **instance method**.
* You can also invoke a method directly on a class, in which case it is called a **class method or a static method**.
* Attributes that take data values on a **per-instance** basis are frequently referred to as **instance variables**.
* Attributes that take on values on a **per-class** basis are called **class attributes or static attributes or class variables**.

### <u>Encapsulation, Inheritance, and Polymorphism</u>
* **Hiding or controlling access** to the implementation-related attributes and the methods of a class is called encapsulation.
* **Inheritance** in object-oriented code allows a subclass to inherit some or all of the attributes and methods of its superclass(es).
* **Polymorphism** basically means that a given category of objects can exhibit multiple identities at the same time
* **Polymorphism** in a nutshell allows us to manipulate instances belonging to the different classes of a hierarchy through a common interface defined for the root class.
