import json

def readFromFile(pathname: str) -> str:
    with open(pathname, 'r') as fp:
        data = fp.read()
        fp.close()
    return data

def writeToFile(pathname: str, contents: str) -> None:
    with open(pathname, 'w') as fp:
        fp.write(contents)
        fp.close()

def readJsonFile(pathname: str) -> str:
    return json.loads(readFromFile(pathname))

def writeJsonFile(pathname: str, contents: str) -> None:
    writeToFile(pathname, json.dumps(contents))
