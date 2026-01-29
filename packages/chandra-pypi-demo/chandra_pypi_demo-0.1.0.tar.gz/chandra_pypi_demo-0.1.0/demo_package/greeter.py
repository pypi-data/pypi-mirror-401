"""
Greeter module - Provides greeting functions.
"""


def greet(name: str, greeting: str = "Hello") -> str:
    """
    Greet a person with a custom message.
    
    Args:
        name: Name of the person to greet
        greeting: Greeting message (default: "Hello")
        
    Returns:
        Formatted greeting string
        
    Examples:
        >>> greet("Alice")
        'Hello, Alice!'
        >>> greet("Bob", "Hi")
        'Hi, Bob!'
    """
    return f"{greeting}, {name}!"


def greet_multiple(names: list, greeting: str = "Hello") -> str:
    """
    Greet multiple people.
    
    Args:
        names: List of names to greet
        greeting: Greeting message (default: "Hello")
        
    Returns:
        Formatted greeting string for all names
        
    Examples:
        >>> greet_multiple(["Alice", "Bob"])
        'Hello, Alice and Bob!'
        >>> greet_multiple(["Alice", "Bob", "Charlie"])
        'Hello, Alice, Bob, and Charlie!'
    """
    if not names:
        return f"{greeting}!"
    
    if len(names) == 1:
        return greet(names[0], greeting)
    
    if len(names) == 2:
        return f"{greeting}, {names[0]} and {names[1]}!"
    
    # For 3+ names, use Oxford comma
    all_but_last = ", ".join(names[:-1])
    return f"{greeting}, {all_but_last}, and {names[-1]}!"
