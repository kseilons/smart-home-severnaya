import os


def listFiles(directory):
    result = []
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.endswith('.json'):
                result.append(os.path.join(root, filename))
    return result
