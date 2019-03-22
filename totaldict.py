import sys
import json
from collections import defaultdict

if __name__ == "__main__":
    names = defaultdict(lambda: 0)

    files = sys.argv[1:]

    for file in files:
        with open(file) as fd:
            data = json.load(fd)

            for k,v in data.items():
                names[k] += v

    print(json.dumps(names))