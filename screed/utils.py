def to_str(line):
    try:
        line = line.decode('utf-8')
    except AttributeError:
        pass

    return line
