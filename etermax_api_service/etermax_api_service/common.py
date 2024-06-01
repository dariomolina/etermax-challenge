
def convert_to_float(value):
    """
    Convert a value to float.

    Args:
        value (str): The value to be converted.

    Returns:
        float: The converted value as a float.

    Raises:
        ValueError: If the value cannot be converted to float.
    """
    try:
        value = float(value)
    except ValueError:
        raise Exception("Value must be valid 'numeric strings'.")
    return value
