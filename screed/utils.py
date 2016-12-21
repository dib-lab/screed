# Copyright (c) 2016, The Regents of the University of California.


def to_str(line):
    try:
        line = line.decode('utf-8')
    except AttributeError:
        pass

    return line
