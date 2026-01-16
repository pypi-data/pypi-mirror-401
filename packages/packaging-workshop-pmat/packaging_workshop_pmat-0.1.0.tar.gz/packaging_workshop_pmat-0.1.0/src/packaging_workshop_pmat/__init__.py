def greet(name: str) -> str:
    """Return a friendly greeting.

    Parameters
    ----------
    name:
        Name of the person to greet.

    Returns
    -------
    str
        Greeting message.
    """
    name = name.strip()
    if not name:
        raise ValueError("name must be a non-empty string")
    return f"Hello, {name}!"