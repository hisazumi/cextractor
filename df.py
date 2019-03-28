import json
import math
import sys

if __name__ == "__main__":
    with open(sys.argv[1]) as file:
        data = json.load(file)
        total = int(sys.argv[2])
        for k, v in sorted(data.items(), key=lambda x: -x[1]):
            data[k] = float(v) / total
            print("%s: %f" % (k, data[k]))

        
