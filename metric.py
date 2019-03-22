import json

if __name__ == "__main__":
    with open("../linux-4.20/index.dict") as file:
        data = json.load(file)
        total = sum(int(i) for i in data.values())
        print(total)
        for k, v in sorted(data.items(), key=lambda x: -x[1]):
            data[k] = float(v) / total
            print("%s: %f" % (k, data[k]))

        
