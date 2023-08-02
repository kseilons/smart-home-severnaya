import os


def listFiles(directory):
    result = []
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.endswith('.json'):
                result.append(os.path.join(root, filename))
    return result


def get_latest_file(path):
    files = os.listdir(path)
    paths = [os.path.join(path, basename) for basename in files if basename.startswith("stream") and basename.endswith(".ts")]
    latest_file_path = max(paths, key=os.path.getctime)
    return os.path.basename(latest_file_path)