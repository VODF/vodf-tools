#!/usr/bin/env python3
class Visitor:
    """Simple visitor wrapper for separating data structure from output
    """
    def __init__(self, f):
        self.f = f
        self.generators = {}

    def generator(self, cls : type):
        def call(fun):
            self.generators[cls] = fun
        return call


    def __call__(self, obj):
        fun = self.generators[type(obj)]
        return fun(obj)
