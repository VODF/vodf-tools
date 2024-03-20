#!/usr/bin/env python3


class visitor:
    """Simple visitor wrapper for separating data structure from output."""

    def __init__(self, f):
        self.f = f
        self.generators = {}

    def generator(self, cls: type):
        def call(fun):
            self.generators[cls] = fun

        return call

    def __call__(self, obj):
        try:
            fun = self.generators[type(obj)]
            return fun(obj)
        except KeyError:
            raise NotImplementedError(
                f"No implementation was found to convert object of type '{type(obj)}'"
            )
