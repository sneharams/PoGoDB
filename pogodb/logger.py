
# class logger:

def log(file, line, tag, logs, code=None):
    """
    Prints a flag with the given parameters.
    @params:
        file    - Required  : source file (Str)
        line    - Required  : line number (Int)
        tag     - Required  : log tag (Str)
        logs    - Required  : output messages (List<Str>)
        code    - Optional  : code reference rep (Str)
    """
    trace = '\tFile "' + file + ', line ' + str(line)
    if (code != None):
        trace += '\n\t\t' + code
        trace += '\n\t\t' + ' ' * (len(code)-1) + '^\n'
    print(trace)

    bullet = ' > '
    message = '[' + tag + ']' + bullet + logs[0]
    if (len(logs) > 1):
        indent = ' ' * (len(tag) + 2)
        for log in logs[1:]:
            message += '\n' + indent + bullet + log
    print(message)