from types import FunctionType

class State():
    def __init__(self, operation:FunctionType) -> None:
        self.operation = operation

    def do_operation(self, region):
        self.operation(region)

