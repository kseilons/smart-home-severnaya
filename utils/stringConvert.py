def str_to_bool(s):
    if s == '1':
        return True
    elif s == '0':
        return False
    else:
        raise ValueError("Cannot convert string to bool")
