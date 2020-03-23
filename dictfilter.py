import json
import sys

if __name__ == "__main__":
    with open(sys.argv[1]) as file:
        data = json.load(file)
        filtered = {key:value for (key,value) in data.items() if value > 200}
        print(json.dumps(filtered))
