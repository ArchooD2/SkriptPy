from contextlib import contextmanager
from typing import List, Callable

class Node:
    def to_skript(self, indent=0):
        """
        Serializes the node into Skript code.
        
        Args:
            indent: The indentation level for the generated Skript code.
        
        Returns:
            A string containing the Skript code representation of the node.
        
        Raises:
            NotImplementedError: If the method is not implemented in a subclass.
        """
        raise NotImplementedError

class Action(Node):
    pass

class Broadcast(Action):
    def __init__(self, message):
        """
        Initializes the action with the specified message.
        
        Args:
            message: The message to be used by the action.
        """
        self.message = message

    def to_skript(self, indent=0):
        """
        Generates Skript code for broadcasting a message.
        
        Args:
            indent: Number of spaces to indent the generated code.
        
        Returns:
            A string containing the Skript broadcast statement with proper indentation.
        """
        return " " * indent + f'broadcast "{self.message}"'

class Teleport(Action):
    def __init__(self, entity, location):
        """
        Initializes a Teleport action with the specified entity and destination location.
        
        Args:
            entity: The entity to teleport.
            location: The target location to teleport the entity to.
        """
        self.entity = entity
        self.location = location

    def to_skript(self, indent=0):
        """
        Generates Skript code for teleporting an entity to a specified location.
        
        Args:
            indent: Number of spaces to indent the generated code.
        
        Returns:
            A string containing the Skript command for teleporting the entity.
        """
        return " " * indent + f'teleport {self.entity} to {self.location}'

class SetVar(Action):
    def __init__(self, name, value):
        """
        Initializes an action to set a local variable with the specified name and value.
        
        Args:
            name: The name of the local variable to set.
            value: The value to assign to the local variable.
        """
        self.name = name
        self.value = value

    def to_skript(self, indent=0):
        """
        Generates Skript code to set a persistent variable for a player by UUID.
        
        Args:
            indent: Number of spaces to indent the generated code.
        
        Returns:
            A string containing the Skript code for setting the variable.
        """
        return " " * indent + f'set {{{self.name}::%player\'s uuid%}} to {self.value}'

class GetVar(Action):
    def __init__(self, name):
        """
        Initializes the instance with the given name.
        
        Args:
            name: The name to assign to the instance.
        """
        self.name = name

    def to_skript(self, indent=0):
        """
        Returns the Skript code for accessing a persistent variable keyed by the player's UUID.
        
        Args:
            indent: Indentation level (unused).
        
        Returns:
            Skript code string for retrieving the variable.
        """
        return f'{{{self.name}::%player\'s uuid%}}'

class IfBlock(Action):
    def __init__(self, condition):
        """
        Initializes an IfBlock with a condition and an empty body for nested actions.
        
        Args:
            condition: The condition string to evaluate for the if block.
        """
        self.condition = condition
        self.body = []

    def to_skript(self, indent=0):
        """
        Generates Skript code for an if conditional block with proper indentation.
        
        Args:
            indent: The number of spaces to indent the generated code.
        
        Returns:
            A string containing the Skript representation of the if block and its nested actions.
        """
        lines = [" " * indent + f'if {self.condition}:']
        for action in self.body:
            lines.append(action.to_skript(indent + 4))
        return "\n".join(lines)

class ElseBlock(Action):
    def __init__(self):
        """
        Initializes the object with an empty body for storing child actions or nodes.
        """
        self.body = []

    def to_skript(self, indent=0):
        """
        Generates Skript code for an else block with proper indentation.
        
        Args:
            indent: Number of spaces to indent the block.
        
        Returns:
            A string containing the Skript representation of the else block and its actions.
        """
        lines = [" " * indent + 'else:']
        for action in self.body:
            lines.append(action.to_skript(indent + 4))
        return "\n".join(lines)

class LoopTimes(Action):
    def __init__(self, times):
        """
        Initializes a loop block that repeats a specified number of times.
        
        Args:
        	times: The number of iterations for the loop.
        """
        self.times = times
        self.body = []

    def to_skript(self, indent=0):
        """
        Generates Skript code for a loop that repeats a set of actions a specified number of times.
        
        Args:
            indent: Number of spaces to indent each line of the generated code.
        
        Returns:
            A string containing the Skript code for the loop block with proper indentation.
        """
        lines = [" " * indent + f'loop {self.times} times:']
        for action in self.body:
            lines.append(action.to_skript(indent + 4))
        return "\n".join(lines)

class LoopPlayers(Action):
    def __init__(self):
        """
        Initializes the object with an empty body for storing child actions or nodes.
        """
        self.body = []

    def to_skript(self, indent=0):
        """
        Generates Skript code for looping over all players and executing the contained actions.
        
        Args:
            indent: Number of spaces to indent the generated code.
        
        Returns:
            A string containing the Skript code for the loop block with nested actions.
        """
        lines = [" " * indent + f'loop all players:']
        for action in self.body:
            lines.append(action.to_skript(indent + 4))
        return "\n".join(lines)

class ScriptContext:
    def __init__(self):
        """
        Initializes the script context with empty stacks for managing nesting, commands, and events.
        """
        self.stack = []
        self.commands = []
        self.events = []

    def push(self, ctx):
        """
        Pushes a context object onto the context stack.
        
        Args:
        	ctx: The context object to be added to the stack.
        """
        self.stack.append(ctx)

    def pop(self):
        """
        Removes and returns the top context from the context stack.
        
        Returns:
            The most recently pushed context object.
        """
        return self.stack.pop()

    def current(self):
        """
        Returns the current context from the top of the context stack, or None if the stack is empty.
        """
        return self.stack[-1] if self.stack else None

ctx = ScriptContext()

class Command(Node):
    def __init__(self, name):
        """
        Initializes a command with the given name and an empty list of actions.
        
        Args:
            name: The name of the command to define.
        """
        self.name = name
        self.actions = []

    def to_skript(self):
        """
        Generates the Skript code representation of the command, including its trigger and actions.
        
        Returns:
            A string containing the formatted Skript code for the command.
        """
        lines = [f'command /{self.name}:', '    trigger:']
        for a in self.actions:
            lines.append(a.to_skript(8))
        return "\n".join(lines)

class Send(Action):
    def __init__(self, message):
        """
        Initializes the action with the specified message.
        
        Args:
            message: The message to be used by this action.
        """
        self.message = message

    def to_skript(self, indent=0):
        """
        Generates Skript code to send a message to a player.
        
        Args:
            indent: Number of spaces to indent the generated code.
        
        Returns:
            A string containing the Skript code for sending the message.
        """
        content = self.message if isinstance(self.message, str) else str(self.message)
        return " " * indent + f'send "{content}" to player'

class Event(Node):
    def __init__(self, name, condition=None):
        """
        Initializes an event handler with a name, optional condition, and an empty list of actions.
        
        Args:
            name: The name of the event to handle.
            condition: An optional condition string for the event trigger.
        """
        self.name = name
        self.condition = condition
        self.actions = []

    def to_skript(self):
        """
        Generates Skript code for an event handler, including its condition and actions.
        
        Returns:
            A string containing the formatted Skript code for the event.
        """
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
        """
        Initializes a function definition node with a name, parameters, and an empty action list.
        
        Args:
            name: The name of the function.
            params: A list of parameter names for the function.
        """
        self.name = name
        self.params = params
        self.actions = []

    def to_skript(self):
        """
        Generates the Skript code representation of the function definition.
        
        Returns:
            A string containing the Skript code for the function, including its parameters and indented body actions.
        """
        lines = [f'function {self.name}({", ".join(self.params)}):']
        for action in self.actions:
            lines.append(action.to_skript(4))
        return "\n".join(lines)

class SetLocalVar(Action):
    def __init__(self, name, value):
        """
        Initializes the action with a variable name and value.
        
        Args:
            name: The name of the variable to set.
            value: The value to assign to the variable.
        """
        self.name = name
        self.value = value

    def to_skript(self, indent=0):
        """
        Generates Skript code to set a local variable to a specified value.
        
        Args:
            indent: Number of spaces to indent the generated code.
        
        Returns:
            A string containing the Skript statement for setting a local variable.
        """
        return " " * indent + f"set {{_{self.name}}} to {self.value}"

class GetLocalVar(Action):
    def __init__(self, name):
        """
        Initializes the instance with the given name.
        
        Args:
            name: The name to assign to the instance.
        """
        self.name = name

    def to_skript(self, indent=0):
        """
        Returns a Skript code representation of the variable retrieval.
        
        Args:
            indent: Indentation level for formatting (unused).
        
        Returns:
            The Skript code string for accessing the variable.
        """
        return f"{{_{self.name}}}"

# DSL API
def command(name):
    """
    Decorator to define a Skript command with the given name.
    
    The decorated function should contain DSL statements that specify the command's actions.
    """
    def decorator(func):
        cmd = Command(name)
        ctx.commands.append(cmd)
        ctx.push(cmd)
        func()
        ctx.pop()
        return func
    return decorator

def event(name, condition=None):
    """
    Decorator to define a Skript event handler with optional condition.
    
    Args:
        name: The name of the Skript event to handle.
        condition: An optional condition string for the event trigger.
    
    Returns:
        A decorator that registers the decorated function as the event's body.
    """
    def decorator(func):
        evt = Event(name, condition=condition)
        ctx.events.append(evt)
        ctx.push(evt)
        func()
        ctx.pop()
        return func
    return decorator

def set_local(name, value):
    """
    Sets a local variable to the specified value in the current script context.
    
    Args:
    	name: The name of the local variable.
    	value: The value to assign to the local variable.
    """
    ctx.current().actions.append(SetLocalVar(name, value))

def get_local(name):
    """
    Returns a node representing retrieval of a local variable by name.
    
    Args:
        name: The name of the local variable to retrieve.
    
    Returns:
        A GetLocalVar instance for use in Skript code generation.
    """
    return GetLocalVar(name)

def function(name, *params):
    """
    Decorator to define a Skript function with the given name and parameters.
    
    Adds a function definition to the script context, executes the decorated function
    to populate its body with actions, and registers it for inclusion in the generated
    Skript code.
    
    Args:
        name: The name of the Skript function.
        *params: Parameter names for the function.
    """
    def decorator(func):
        fn = Function(name, params)
        ctx.commands.append(fn)  # Reuse the same storage or make `ctx.functions`
        ctx.push(fn)
        func()
        ctx.pop()
        return func
    return decorator

def send(msg):
    """
    Adds a send message action to the current script context.
    
    Args:
        msg: The message to send to the player.
    """
    ctx.current().actions.append(Send(msg))

def broadcast(msg):
    """
    Adds a broadcast action with the specified message to the current script context.
    
    Args:
        msg: The message to broadcast to all players.
    """
    ctx.current().actions.append(Broadcast(msg))

def teleport(entity, location):
    """
    Adds a teleport action for the specified entity to the given location in the current script context.
    
    Args:
        entity: The entity to teleport (e.g., a player or variable representing an entity).
        location: The destination location for the teleport action.
    """
    ctx.current().actions.append(Teleport(entity, location))

def set_var(name, value):
    """
    Adds an action to set a persistent variable keyed by player UUID to the specified value.
    
    Args:
        name: The name of the variable to set.
        value: The value to assign to the variable.
    """
    ctx.current().actions.append(SetVar(name, value))

def get_var(name):
    """
    Returns a node representing retrieval of a persistent variable by name.
    
    Args:
        name: The name of the persistent variable to retrieve.
    
    Returns:
        A GetVar instance for use in Skript code generation.
    """
    return GetVar(name)

player = "player"

@contextmanager
def If(condition):
    """
    Context manager for creating an if block with the specified condition.
    
    Adds an IfBlock to the current context's actions, allowing nested actions to be defined within the if block.
    """
    block = IfBlock(condition)
    ctx.current().actions.append(block)
    ctx.push(block)
    yield
    ctx.pop()

@contextmanager
def Else():
    """
    Context manager for defining an else block in a Skript script.
    
    Appends an ElseBlock to the current context's actions and yields control for nested actions within the else block.
    """
    block = ElseBlock()
    ctx.current().actions.append(block)
    ctx.push(block)
    yield
    ctx.pop()

@contextmanager
def loop_times(n):
    """
    Context manager for repeating a block of actions a specified number of times.
    
    Args:
        n: The number of times to repeat the nested actions.
    
    Example:
        with loop_times(5):
            send("Hello!")
    """
    loop = LoopTimes(n)
    ctx.current().actions.append(loop)
    ctx.push(loop)
    yield
    ctx.pop()

@contextmanager
def loop_players():
    """
    Context manager for creating a loop block that iterates over all players.
    
    Appends a LoopPlayers block to the current context's actions and yields control
    for nested actions within the loop.
    """
    loop = LoopPlayers()
    ctx.current().actions.append(loop)
    ctx.push(loop)
    yield
    ctx.pop()