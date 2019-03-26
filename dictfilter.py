import json

if __name__ == "__main__":
    with open("../linux-4.20/index.dict") as file:
        data = json.load(file)
        filtered = {key:value for (key,value) in data.items() if value > 200}
        print(json.dumps(filtered))

