#!/usr/bin/env python3
class Visitor:
    """Simple visitor wrapper for separating data structure from output
    """
    def __init__(self, f):
        self.f = f
        self.generators = {}

    def generator(self, type1):
        def call(fun):
            self.generators[(type1)] = fun
        return call


    def __call__(self, obj):
        fun = self.generators[type(obj)]
        return fun(obj)
