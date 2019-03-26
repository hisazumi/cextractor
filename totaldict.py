import sys
import json
from collections import defaultdict

if __name__ == "__main__":
    names = defaultdict(lambda: 0)

    files = sys.argv[1:]

    for file in files:
        try:
            with open(file) as fd:
                data = json.load(fd)

                for k,v in data.items():
                    names[k] += 1
        except Exception as e:
            print(e)

    print(json.dumps(names))
