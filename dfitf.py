import json
import math
import sys

# dfitf [total.dict] [num] [.c.dict]

if __name__ == "__main__":
    df = {}
    with open(sys.argv[1]) as file:
        df = json.load(file)
    docnum = int(sys.argv[2])

    cdict = {}
    with open(sys.argv[3]) as file:
        cdict = json.load(file)
    
    term_num = sum(int(i) for i in cdict.values())
    metrics = {}
    for k, num in cdict.items():
        itf = term_num / float(num)
        df = cdict[k] / 26415
        #XXX document number should be passed as arg
        dfitf = df * itf
        metrics[k] = (dfitf, itf, df)

    for k, mx in sorted(metrics.items(), key=lambda x: -x[1][0]):
        print("%s: %f %f %f" % (k, mx[0], mx[1], mx[2]))
