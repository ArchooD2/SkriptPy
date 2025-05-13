from contextlib import contextmanager
from typing import List, Callable

class Node:
    def to_skript(self, indent=0):
        raise NotImplementedError

class Action(Node):
    pass

class Broadcast(Action):
    def __init__(self, message):
        self.message = message

    def to_skript(self, indent=0):
        return " " * indent + f'broadcast "{self.message}"'

class Teleport(Action):
    def __init__(self, entity, location):
        self.entity = entity
        self.location = location

    def to_skript(self, indent=0):
        return " " * indent + f'teleport {self.entity} to {self.location}'

class SetVar(Action):
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def to_skript(self, indent=0):
        return " " * indent + f'set {{{self.name}::%player\'s uuid%}} to {self.value}'

class GetVar(Action):
    def __init__(self, name):
        self.name = name

    def to_skript(self, indent=0):
        return f'{{{self.name}::%player\'s uuid%}}'

class IfBlock(Action):
    def __init__(self, condition):
        self.condition = condition
        self.body = []

    def to_skript(self, indent=0):
        lines = [" " * indent + f'if {self.condition}:']
        for action in self.body:
            lines.append(action.to_skript(indent + 4))
        return "\n".join(lines)

class ElseBlock(Action):
    def __init__(self):
        self.body = []

    def to_skript(self, indent=0):
        lines = [" " * indent + 'else:']
        for action in self.body:
            lines.append(action.to_skript(indent + 4))
        return "\n".join(lines)

class LoopTimes(Action):
    def __init__(self, times):
        self.times = times
        self.body = []

    def to_skript(self, indent=0):
        lines = [" " * indent + f'loop {self.times} times:']
        for action in self.body:
            lines.append(action.to_skript(indent + 4))
        return "\n".join(lines)

class LoopPlayers(Action):
    def __init__(self):
        self.body = []

    def to_skript(self, indent=0):
        lines = [" " * indent + f'loop all players:']
        for action in self.body:
            lines.append(action.to_skript(indent + 4))
        return "\n".join(lines)

class ScriptContext:
    def __init__(self):
        self.stack = []
        self.commands = []
        self.events = []

    def push(self, ctx):
        self.stack.append(ctx)

    def pop(self):
        return self.stack.pop()

    def current(self):
        return self.stack[-1] if self.stack else None

ctx = ScriptContext()

class Command(Node):
    def __init__(self, name):
        self.name = name
        self.actions = []

    def to_skript(self):
        lines = [f'command /{self.name}:', '    trigger:']
        for a in self.actions:
            lines.append(a.to_skript(8))
        return "\n".join(lines)

class Send(Action):
    def __init__(self, message):
        self.message = message

    def to_skript(self, indent=0):
        content = self.message if isinstance(self.message, str) else str(self.message)
        return " " * indent + f'send "{content}" to player'

class Event(Node):
    def __init__(self, name, condition=None):
        self.name = name
        self.condition = condition
        self.actions = []

    def to_skript(self):
        header = f'on {self.name}:'
        lines = [header]
        if self.condition:
            lines.append("    if " + self.condition + ":")
            for a in self.actions:
                lines.append(a.to_skript(8))
        else:
            for a in self.actions:
                lines.append(a.to_skript(4))
        return "\n".join(lines)

class Function(Node):
    def __init__(self, name, params):
        self.name = name
        self.params = params
        self.actions = []

    def to_skript(self):
        lines = [f'function {self.name}({", ".join(self.params)}):']
        for action in self.actions:
            lines.append(action.to_skript(4))
        return "\n".join(lines)

class SetLocalVar(Action):
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def to_skript(self, indent=0):
        return " " * indent + f"set {{_{self.name}}} to {self.value}"

class GetLocalVar(Action):
    def __init__(self, name):
        self.name = name

    def to_skript(self, indent=0):
        return f"{{_{self.name}}}"

# DSL API
def command(name):
    def decorator(func):
        cmd = Command(name)
        ctx.commands.append(cmd)
        ctx.push(cmd)
        func()
        ctx.pop()
        return func
    return decorator

def event(name, condition=None):
    def decorator(func):
        evt = Event(name, condition=condition)
        ctx.events.append(evt)
        ctx.push(evt)
        func()
        ctx.pop()
        return func
    return decorator

def set_local(name, value):
    ctx.current().actions.append(SetLocalVar(name, value))

def get_local(name):
    return GetLocalVar(name)

def function(name, *params):
    def decorator(func):
        fn = Function(name, params)
        ctx.commands.append(fn)  # Reuse the same storage or make `ctx.functions`
        ctx.push(fn)
        func()
        ctx.pop()
        return func
    return decorator

def send(msg):
    ctx.current().actions.append(Send(msg))

def broadcast(msg):
    ctx.current().actions.append(Broadcast(msg))

def teleport(entity, location):
    ctx.current().actions.append(Teleport(entity, location))

def set_var(name, value):
    ctx.current().actions.append(SetVar(name, value))

def get_var(name):
    return GetVar(name)

player = "player"

@contextmanager
def If(condition):
    block = IfBlock(condition)
    ctx.current().actions.append(block)
    ctx.push(block)
    yield
    ctx.pop()

@contextmanager
def Else():
    block = ElseBlock()
    ctx.current().actions.append(block)
    ctx.push(block)
    yield
    ctx.pop()

@contextmanager
def loop_times(n):
    loop = LoopTimes(n)
    ctx.current().actions.append(loop)
    ctx.push(loop)
    yield
    ctx.pop()

@contextmanager
def loop_players():
    loop = LoopPlayers()
    ctx.current().actions.append(loop)
    ctx.push(loop)
    yield
    ctx.pop()