import sys
import json
from collections import defaultdict

import glob
from pathlib import Path

if __name__ == "__main__":
    names = defaultdict(lambda: 0)

    # files = sys.argv[1:]
    dir = sys.argv[1]
    path = Path(dir)
    files = list(path.glob("**/*.fdict"))

    count = 0
    num = len(files)
    print("make total.fdict...", file=sys.stderr)
    for file_name in files:
        print( count, "/", num, end="\r", file=sys.stderr)
        count += 1
        try:
            with open(file_name) as fd:
                data = json.load(fd)

                for k,v in data.items():
                    names[k] += 1
        except Exception as e:
            print(e, ", fdict file : (", file_name ,")", file=sys.stderr)

    print(json.dumps(names))
