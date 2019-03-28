import json
import math
import sys

if __name__ == "__main__":
    with open(sys.argv[1]) as file:
        data = json.load(file)
        term_num = sum(int(i) for i in data.values())
        for k, v in sorted(data.items(), key=lambda x: -x[1]):
            print("%s: %f" % (k, math.log10(term_num / float(v))))
