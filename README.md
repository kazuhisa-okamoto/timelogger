
# timelogger
Measure execution time tracking nesting structure and number of calls.

## Usage
```py
from timelogger import Timer, output_result

def nestedfunc1():
    timer = Timer("nestedfunc1")
    #...
    timer.stop()

def func1():
    timer = Timer("func1")
    nestedfunc1()
    timer.stop()

output_result("path")
```

## Output example
```py
func1: 2.013594 (95.239%), 1
    nestedfunc1: 1.008603 (47.705%), 10
    nestedfunc2: 1.004991 (47.534%), 10
func2: 0.100669 (4.761%), 1
```