import os


def find_all(name, path):
    result = []
    for root, dirs, files in os.walk(path):
        if name in files:
            result.append(os.path.join(root, name))
    return result


def find_up(name, path):
    directory = os.path.abspath(path)
    while directory:
        filename = os.path.join(directory, name)
        if os.path.isfile(filename):
            return filename
        directory = os.path.dirname(directory)
    return None
