import sys
import json
from collections import defaultdict

if __name__ == "__main__":
    cfdict = sys.argv[1]
    totalfdict = sys.argv[2]

    names = defaultdict(lambda: 0)

    with open(totalfdict) as tfd:
        names.update(json.load(tfd))

    with open(cfdict) as cfd:
        data = json.load(cfd)

        for k,v in data.items():
            names[k] += 1

    print(json.dumps(names))
