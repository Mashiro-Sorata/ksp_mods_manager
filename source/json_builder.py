import json

def saveJson(path, data):
    js = json.dumps(data, sort_keys=True, indent=4, ensure_ascii=False)
    with open(path,'w') as f:
        f.write(js)

def loadJson(path):
    try:
        with open(path,'r') as f:
            data = json.loads(f.read())
        return data
    except FileNotFoundError:
        return dict()

