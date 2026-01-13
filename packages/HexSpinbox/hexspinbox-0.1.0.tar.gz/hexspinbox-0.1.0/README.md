[![PyPi](https://img.shields.io/pypi/v/HexSpinbox)](https://pypi.org/project/HexSpinbox/)
[![Downloads](https://img.shields.io/pypi/dm/HexSpinbox)](https://pypi.org/project/HexSpinbox)

# HexSpinbox
A simple Python Tkinter widget for displaying hexadecimal integers in a spin box.

Since the regular spinbox from tkinter does not support a hexadecimal format specifier (e.g. `'%#x'`), 
I wrote a dedicated class for that.
It turned out to be surprisingly hard to get the built-in button functionality to work properly. 
This implementation uses the `values` property to actually display hexadecimal numbers in the regular spinbox.

## Installation
This has no dependencies other than tkinter/ttk, which are shipped with Python.
You can download and install this widget via
```bash
pip install HexSpinbox
```
or simply copy the class from 
[HexSpinbox.py](https://github.com/sayofan/HexSpinbox/blob/main/HexSpinbox/HexSpinbox.py) 
to wherever you need it. 
It's less than a hundred lines.

## Usage
Use it like any other `ttk.Spinbox`. Except for connecting to a variable.
Use only IntVars. To avoid confusion, I added an argument `integer_var` to use (instead of 
`textvariable`.)  
Also do not try to set a `format`. Only the default with small letters is implemented.  
Lastly, be careful whith changing `validation`, which defaults to `focusout`.

Example:
```python
import tkinter as tk
from HexSpinbox.HexSpinbox import HexSpinbox
root = tk.Tk()
var = tk.IntVar(value=2)
spinbox = HexSpinbox(root, from_=0, to=50, integer_var=var)
spinbox.pack()
root.mainloop()
```

## Features
- shows an integer in hexadecimal form with prefix _0x_ and small letters.
- connection with Tk variables works
- uses spin buttons, up/down arrow key or mouse wheel to change value by 1
- allows typing a hexadecimal number (with or without _0x_ prefix and with small or capital letters)
- themes work

Here's what it looks like with the theme "breeze":  
![HexSpinbox in theme 'breeze'](https://github.com/sayofan/HexSpinbox/blob/main/doc/HexSpinbox_breeze.png?raw=true)


## Known Issues
- After changing the value with something other than the spin buttons (e.g. typing in a value or changing the underlying IntVar by another widget) the up button will go down on the first button press

## Implementation consideration
Q: Why not use a list of all possible values as strings for `values`, like that Stack-Overflow thread suggested?  
A: Because that takes a lot of RAM. I use this spin box to select values from a 32bit integer range. 
That gives 2^31+1 possibilities. Even using only a tenth of that as a list of strings took about 30GB on a test. 
It is therefore simply not viable.
