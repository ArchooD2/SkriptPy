
--- a/skriptpy/core.py
+++ b/skriptpy/core.py
@@ -2 +2
-from typing import List, Callable
+from typing import List, Callable, Optional, Any, Union, TypeVar, Type, cast, Dict
@@ -395 +395
-def command(name):
+def command(name: str) -> Callable[[Callable[[], None]], Callable[[], None]]:
@@ -410 +410
-def event(name, condition=None):
+def event(name: str, condition: Optional[str] = None) -> Callable[[Callable[[], None]], Callable[[], None]]:
@@ -430 +430
-def set_local(name, value):
+def set_local(name: str, value: Any) -> None:
@@ -440 +440
-def get_local(name):
+def get_local(name: str) -> GetLocalVar:
@@ -452 +452
-def function(name, *params):
+def function(name: str, *params: str) -> Callable[[Callable[[], None]], Callable[[], None]]:
@@ -473 +473
-def send(msg):
+def send(msg: Any) -> None:
@@ -482 +482
-def broadcast(msg):
+def broadcast(msg: Any) -> None:
@@ -491 +491
-def teleport(entity, location):
+def teleport(entity: str, location: str) -> None:
@@ -501 +501
-def set_var(name, value):
+def set_var(name: str, value: Any) -> None:
@@ -511 +511
-def get_var(name):
+def get_var(name: str) -> GetVar:

def teleport(entity: str, location: str) -> None:
    """
    Adds a teleport action for the specified entity to the given location in the current script context.
    
    Args:
        entity: The entity to teleport (e.g., a player or variable representing an entity).
        location: The destination location for the teleport action.
    """
    ctx.current().actions.append(Teleport(entity, location))

def set_var(name: str, value: Any) -> None:
    """
    Adds an action to set a persistent variable keyed by player UUID to the specified value.
    
    Args:
        name: The name of the variable to set.
        value: The value to assign to the variable.
    """
    ctx.current().actions.append(SetVar(name, value))

def get_var(name: str) -> GetVar:
    """
    Returns a node representing retrieval of a persistent variable by name.
    
    Args:
        name: The name of the persistent variable to retrieve.
    
    Returns:
        A GetVar instance for use in Skript code generation.
    """
    return GetVar(name)

player = "player"
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