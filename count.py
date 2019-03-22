f = open('test.csv')
data = f.read()

# counting
words = {}
for word in data.split():
    words[word] = words.get(word, 0) + 1

# sort by count
d = [(v,k) for k,v in words.items()]
d.sort()
d.reverse()
for count, word in d[:1000]:
	print count, word