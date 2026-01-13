from tkinter import IntVar, ttk

class HexSpinbox(ttk.Spinbox):
    """A ttk.Spinbox that displays integer values as hexadecimal numbers
    """
    def __init__(self, master=None, integer_var: IntVar | None = None, **kwargs):
        try:
            outer_func = kwargs['command']
            def _command():
                self.validate()
                outer_func()
                pass
            kwargs['command'] = _command
        except KeyError:
            kwargs['command'] = self.validate

        try:
            if kwargs['textvariable'] is not None:
                raise TypeError("Use 'integer_var' instead of textvariable")
        except KeyError:  # no textvariable in kwargs
            pass

        try:
            if kwargs['format'] is not None:
                raise TypeError("Formatstring is not supported for HexSpinbox")
        except KeyError:  # no format in kwargs
            pass

        kwargs['values'] = ["0x0"]
        kwargs['validatecommand'] = self._validate_func
        kwargs['validate'] = 'focusout'
        self.integer_var = integer_var
        if self.integer_var:
            self.integer_var.trace_add("write", self._int_var_write_callback)
        self.previous_value = 0
        self.min = kwargs['from_']
        self.max = kwargs['to']
        super().__init__(master, **kwargs)

    def get(self):
        return int(super().get(), 16)

    def _validate_func(self):
        value = self.get()

        if value<self.min or value>self.max:
            self.set(hex(self.previous_value))
            return False
        
        self.set(hex(value))

        if self.integer_var:
            self.integer_var.set(value)

        self.previous_value = value
        if value==self.min:
            self.configure(values = [hex(value), hex(value+1)])
            return True
        if value==self.max:
            self.configure(values = [hex(value-1), hex(value)])
            return True
        self.configure(values = [hex(value-1), hex(value+1)])
        return True
    
    def _int_var_write_callback(self, *args):
        try:
            assert self.integer_var is not None
            value = self.integer_var.get()
            self.set(hex(value))
            self.validate()
        except:
            pass
