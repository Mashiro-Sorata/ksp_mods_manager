import json

def saveJson(path, data):
    js = json.dumps(data, sort_keys=True,indent=4)
    with open(path,'w') as f:
        f.write(js)

def loadJson(path):
    with open(path,'r') as f:
        data = json.loads(f.read())
    return data

if __name__ == '__main__':
    data = loadJson('paths.json')

